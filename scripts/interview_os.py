#!/usr/bin/env python
"""Local workspace and deterministic aggregates for PM Interview Review OS."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.1"
SUPPORTED_SCHEMA_VERSIONS = {"1.0", "1.1"}
OUTCOMES = {"advanced", "rejected", "offer", "withdrew", "unknown"}
CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.7, "low": 0.4}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def as_path(value: str | os.PathLike[str]) -> Path:
    """Accept native Windows paths and MSYS /c/... paths."""
    text = str(value)
    if os.name == "nt" and len(text) >= 3 and text[0] == "/" and text[1].isalpha() and text[2] == "/":
        text = f"{text[1].upper()}:{text[2:]}"
    return Path(text).expanduser()


def default_root() -> Path:
    configured = os.environ.get("PM_INTERVIEW_REVIEW_HOME")
    return as_path(configured) if configured else Path.home() / ".pm-interview-review-os"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def init_workspace(root: Path) -> None:
    for d in ("interviews", "aggregates"):
        (root / d).mkdir(parents=True, exist_ok=True)
    config = root / "config.json"
    if not config.exists():
        atomic_json(config, {
            "schema_version": SCHEMA_VERSION,
            "created_at": now_iso(),
            "privacy": "local-only",
            "aggregation": "rebuild-from-records"
        })
    events = root / "calibration-events.jsonl"
    events.touch(exist_ok=True)


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "schema_version", "interview_id", "metadata", "source_manifest", "transcript",
        "questions", "key_answer_reviews", "competency_observations", "shortcoming_cards",
        "anti_patterns", "projects", "reverse_interview", "shadow_jd", "verdict"
    ]
    if record.get("schema_version") == "1.1":
        required.extend(["question_transcript", "answer_suggestions"])
    for key in required:
        if key not in record:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors
    if record["schema_version"] not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(f"schema_version must be one of {sorted(SUPPORTED_SCHEMA_VERSIONS)}")
    iid = record["interview_id"]
    if not isinstance(iid, str) or not iid or any(c in iid for c in '<>:"/\\|?*'):
        errors.append("interview_id is empty or contains unsafe path characters")

    questions = record.get("questions", [])
    ids = [q.get("id") for q in questions]
    if None in ids or len(ids) != len(set(ids)):
        errors.append("question IDs must be present and unique")
    id_set = set(ids)
    for q in questions:
        parent = q.get("parent_id")
        if parent is not None and parent not in id_set:
            errors.append(f"{q.get('id')}: parent_id {parent!r} does not exist")
        if parent == q.get("id"):
            errors.append(f"{q.get('id')}: question cannot parent itself")
        if len(q.get("competencies", [])) > 3:
            errors.append(f"{q.get('id')}: at most 3 primary competencies")

    if record.get("schema_version") == "1.1":
        eligible_id_order = [
            q.get("id") for q in questions if q.get("type") in {"root", "follow-up"}
        ]
        eligible_ids = set(eligible_id_order)
        reverse_ids = {
            q.get("id") for q in questions if q.get("type") == "candidate-reverse-question"
        }
        transcript_rows = record.get("question_transcript", [])
        transcript_ids = [row.get("question_id") for row in transcript_rows]
        if len(transcript_ids) != len(set(transcript_ids)):
            errors.append("question_transcript question_ids must be unique")
        if set(transcript_ids) != eligible_ids:
            errors.append("question_transcript must cover every root/follow-up exactly once")
        elif transcript_ids != eligible_id_order:
            errors.append("question_transcript must preserve question order")
        captured_ids: set[str] = set()
        questions_by_id = {q.get("id"): q for q in questions}
        for row in transcript_rows:
            qid = row.get("question_id")
            question = row.get("question", {})
            answer = row.get("answer", {})
            source_question = questions_by_id.get(qid, {})
            if row.get("parent_id") != source_question.get("parent_id"):
                errors.append(f"{qid}: question_transcript parent_id disagrees with questions")
            if row.get("type") != source_question.get("type"):
                errors.append(f"{qid}: question_transcript type disagrees with questions")
            if not question.get("raw_text") or not question.get("anchor"):
                errors.append(f"{qid}: missing raw question text or anchor")
            status = answer.get("status")
            if status == "captured":
                captured_ids.add(qid)
                if not answer.get("raw_text") or not answer.get("anchor") or not answer.get("speaker"):
                    errors.append(f"{qid}: captured answer needs speaker, raw_text and anchor")
            elif status == "no-answer":
                if answer.get("raw_text") is not None:
                    errors.append(f"{qid}: no-answer must not contain raw_text")
            elif status != "uncertain":
                errors.append(f"{qid}: invalid answer status {status!r}")

        suggestions = record.get("answer_suggestions", [])
        suggestion_ids = [item.get("question_id") for item in suggestions]
        if len(suggestion_ids) != len(set(suggestion_ids)):
            errors.append("answer_suggestions question_ids must be unique")
        if set(suggestion_ids) != captured_ids:
            errors.append("answer_suggestions must cover every captured root/follow-up exactly once")
        expected_suggestion_order = [qid for qid in transcript_ids if qid in captured_ids]
        if suggestion_ids != expected_suggestion_order:
            errors.append("answer_suggestions must preserve captured question order")
        if set(suggestion_ids) & reverse_ids:
            errors.append("candidate reverse questions must not have Better Answers")
        for item in suggestions:
            qid = item.get("question_id")
            if not item.get("recommended_structure"):
                errors.append(f"{qid}: answer suggestion lacks recommended_structure")
            if not item.get("suggested_answer"):
                errors.append(f"{qid}: answer suggestion lacks suggested_answer")
            if not item.get("provenance"):
                errors.append(f"{qid}: answer suggestion lacks provenance")

        exchanges = record.get("reverse_interview", {}).get("exchanges", [])
        exchange_qids = [item.get("question_id") for item in exchanges]
        if len(exchange_qids) != len(set(exchange_qids)):
            errors.append("reverse_interview exchange question_ids must be unique")
        if set(exchange_qids) != reverse_ids:
            errors.append("reverse_interview exchanges must cover every candidate reverse question")
        for item in exchanges:
            rqid = item.get("exchange_id")
            candidate_question = item.get("candidate_question", {})
            interviewer_answer = item.get("interviewer_answer", {})
            if not candidate_question.get("raw_text") or not candidate_question.get("anchor"):
                errors.append(f"{rqid}: missing candidate question raw text or anchor")
            if interviewer_answer.get("status") == "captured" and (
                not interviewer_answer.get("raw_text") or not interviewer_answer.get("anchor")
            ):
                errors.append(f"{rqid}: captured interviewer answer needs raw_text and anchor")

    valid_q = set(ids)
    dims = {"substance", "structure", "relevance", "credibility", "differentiation"}
    for review in record.get("key_answer_reviews", []):
        qid = review.get("question_id")
        if qid not in valid_q:
            errors.append(f"key answer review references unknown question: {qid}")
        if not review.get("evidence"):
            errors.append(f"{qid}: key answer review has no evidence")
        scores = review.get("scores", {})
        if set(scores) != dims:
            errors.append(f"{qid}: scores must contain exactly {sorted(dims)}")
        for name, score in scores.items():
            if not isinstance(score, (int, float)) or not 1 <= score <= 10:
                errors.append(f"{qid}: score {name} out of range 1..10")
        overall = review.get("overall_score")
        if not isinstance(overall, (int, float)) or not 1 <= overall <= 10:
            errors.append(f"{qid}: overall_score out of range 1..10")
        if not review.get("weight_profile"):
            errors.append(f"{qid}: missing weight_profile")
        if record.get("schema_version") == "1.0":
            if "suggested_answer" not in review:
                errors.append(f"{qid}: missing suggested_answer (placeholders are allowed)")
        elif review.get("answer_suggestion_ref") != qid:
            errors.append(f"{qid}: answer_suggestion_ref must point to the same Q ID")

    mode = record.get("metadata", {}).get("mode")
    card_count = len(record.get("shortcoming_cards", []))
    if mode == "full" and questions and not 3 <= card_count <= 7:
        errors.append("full review must contain 3-7 shortcoming cards")
    for card in record.get("shortcoming_cards", []):
        if not card.get("evidence"):
            errors.append(f"shortcoming card {card.get('name')!r} has no evidence")
    for item in record.get("shadow_jd", []):
        if item.get("label") != "inference":
            errors.append("shadow_jd items must be labeled inference")
        if not item.get("evidence_anchors"):
            errors.append(f"shadow_jd {item.get('statement')!r} has no evidence")
    for ap in record.get("anti_patterns", []):
        count, eligible = ap.get("count", -1), ap.get("eligible_answers", -1)
        if not isinstance(count, int) or not isinstance(eligible, int) or min(count, eligible) < 0:
            errors.append(f"anti-pattern {ap.get('name')!r}: invalid counts")
        if eligible and count > eligible:
            errors.append(f"anti-pattern {ap.get('name')!r}: count exceeds eligible_answers")
    return errors


def load_records(root: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted((root / "interviews").glob("*/record.json")):
        try:
            record = read_json(path)
            record["_record_path"] = str(path)
            records.append(record)
        except Exception as exc:
            print(f"WARN: cannot read {path}: {exc}", file=sys.stderr)
    return records


def date_key(record: dict[str, Any]) -> tuple[str, str]:
    return (str(record.get("metadata", {}).get("date", "")), str(record.get("interview_id", "")))


def weighted_current(observations: list[dict[str, Any]]) -> tuple[float | None, int]:
    recent = sorted(observations, key=lambda x: (x["date"], x["interview_id"]))[-3:]
    total_w = sum(CONFIDENCE_WEIGHT.get(str(x.get("confidence", "low")).lower(), 0.4) for x in recent)
    if not recent or total_w == 0:
        return None, 0
    value = sum(float(x["score"]) * CONFIDENCE_WEIGHT.get(str(x.get("confidence", "low")).lower(), 0.4) for x in recent) / total_w
    return round(value, 2), len(recent)


def competency_trend(obs: list[dict[str, Any]]) -> str:
    ordered = sorted(obs, key=lambda x: (x["date"], x["interview_id"]))
    if len(ordered) < 4:
        return "Insufficient history"
    recent, prior = ordered[-3:], ordered[-6:-3]
    if len(prior) < 2:
        return "Insufficient history"
    r, _ = weighted_current(recent)
    p, _ = weighted_current(prior)
    if r is None or p is None:
        return "Insufficient history"
    if r - p >= 0.5:
        return "Improving"
    if p - r >= 0.5:
        return "Worsening"
    return "Stable"


def rate(items: list[dict[str, Any]]) -> float | None:
    eligible = sum(int(x.get("eligible_answers", 0)) for x in items)
    return round(sum(int(x.get("count", 0)) for x in items) / eligible, 4) if eligible else None


def anti_pattern_trend(items: list[dict[str, Any]]) -> str:
    ordered = sorted(items, key=lambda x: (x["date"], x["interview_id"]))
    if len(ordered) < 4:
        return "Insufficient history"
    recent, prior = ordered[-3:], ordered[-6:-3]
    if len(prior) < 1:
        return "Insufficient history"
    rr, pr = rate(recent), rate(prior)
    if rr is None or pr is None:
        return "Insufficient history"
    abs_delta = rr - pr
    relative = abs_delta / pr if pr else (1.0 if rr else 0.0)
    if abs_delta <= -0.10 and relative <= -0.20:
        return "Improving"
    if abs_delta >= 0.10 and (pr == 0 or relative >= 0.20):
        return "Worsening"
    return "Stable"


def rebuild(root: Path) -> dict[str, Any]:
    init_workspace(root)
    records = sorted(load_records(root), key=date_key)
    questions: dict[str, dict[str, Any]] = {}
    competency_obs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    anti_obs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    project_obs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    stories: list[dict[str, Any]] = []
    calibration: list[dict[str, Any]] = []

    for r in records:
        iid = r["interview_id"]
        meta = r.get("metadata", {})
        date, company = str(meta.get("date", "")), str(meta.get("company", "unknown"))
        review_by_q = {x.get("question_id"): x for x in r.get("key_answer_reviews", [])}
        for q in r.get("questions", []):
            if q.get("type") in {"administrative", "candidate-reverse-question"}:
                continue
            canonical = (q.get("canonical_question") or q.get("surface_question") or "").strip()
            if not canonical:
                continue
            key = canonical.casefold()
            item = questions.setdefault(key, {
                "question": canonical, "category": q.get("competencies", []), "occurrence_count": 0,
                "interviews": [], "companies": [], "last_asked": "", "best_answer": None
            })
            item["occurrence_count"] += 1
            if iid not in item["interviews"]:
                item["interviews"].append(iid)
            if company not in item["companies"]:
                item["companies"].append(company)
            if date >= item["last_asked"]:
                item["last_asked"] = date
            review = review_by_q.get(q.get("id"))
            if review and (not item["best_answer"] or review.get("overall_score", 0) > item["best_answer"]["score"]):
                item["best_answer"] = {"interview_id": iid, "question_id": q.get("id"), "score": review.get("overall_score")}
        for obs in r.get("competency_observations", []):
            competency_obs[obs["competency"]].append({**obs, "interview_id": iid, "date": date})
        for ap in r.get("anti_patterns", []):
            anti_obs[ap["name"]].append({**ap, "interview_id": iid, "date": date})
        for project in r.get("projects", []):
            project_obs[project["project_id"]].append({**project, "interview_id": iid, "date": date})
        for story in r.get("story_candidates", []):
            stories.append({**story, "source_interview_id": iid})
        if r.get("outcome"):
            calibration.append({"interview_id": iid, "verdict": r.get("verdict"), "outcome": r.get("outcome")})

    qbank = []
    for item in questions.values():
        item["interview_count"] = len(item.pop("interviews"))
        item["companies"].sort()
        qbank.append(item)
    qbank.sort(key=lambda x: (-x["interview_count"], -x["occurrence_count"], x["question"]))

    matrix = []
    for competency, obs in sorted(competency_obs.items()):
        current, sample = weighted_current(obs)
        matrix.append({"competency": competency, "current": current, "trend": competency_trend(obs), "sample_size": sample, "observations": obs})

    anti = []
    for name, obs in sorted(anti_obs.items()):
        anti.append({
            "name": name,
            "total_count": sum(x.get("count", 0) for x in obs),
            "total_eligible": sum(x.get("eligible_answers", 0) for x in obs),
            "recent_3_rate": rate(sorted(obs, key=lambda x: (x["date"], x["interview_id"]))[-3:]),
            "recent_5_rate": rate(sorted(obs, key=lambda x: (x["date"], x["interview_id"]))[-5:]),
            "trend": anti_pattern_trend(obs),
            "observations": obs
        })

    projects = []
    for pid, obs in sorted(project_obs.items()):
        ordered = sorted(obs, key=lambda x: (x["date"], x["interview_id"]))
        latest = ordered[-1]
        projects.append({
            "project_id": pid,
            "name": latest.get("name"),
            "current_probe_depth": latest.get("current_probe_depth"),
            "historical_max_evidenced_depth": max(x.get("current_probe_depth", 0) for x in ordered),
            "latest_first_weak_layer": latest.get("first_weak_layer"),
            "observations": ordered
        })

    outputs = {
        "question-bank.json": qbank,
        "competency-matrix.json": matrix,
        "anti-patterns.json": anti,
        "project-probe-depth.json": projects,
        "story-bank.json": stories,
        "calibration.json": calibration
    }
    for filename, data in outputs.items():
        atomic_json(root / "aggregates" / filename, data)
    summary = {"interviews": len(records), "questions": len(qbank), "competencies": len(matrix), "anti_patterns": len(anti), "projects": len(projects), "stories": len(stories), "outcomes": len(calibration), "rebuilt_at": now_iso()}
    atomic_json(root / "aggregates" / "summary.json", summary)
    return summary


def cmd_save(args: argparse.Namespace) -> None:
    root = as_path(args.root)
    init_workspace(root)
    record_path = as_path(args.record)
    record = read_json(record_path)
    errors = validate_record(record)
    if errors:
        print("RECORD INVALID", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        raise SystemExit(2)
    target = root / "interviews" / record["interview_id"]
    if target.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite existing interview {record['interview_id']}; use --overwrite")
    target.mkdir(parents=True, exist_ok=True)
    atomic_json(target / "record.json", record)
    for source, name in ((args.review, "review.md"), (args.transcript, "transcript.normalized.md"), (args.manifest, "source-manifest.json")):
        if source:
            src = as_path(source)
            if not src.exists():
                raise SystemExit(f"missing input file: {src}")
            shutil.copy2(src, target / name)
    summary = rebuild(root)
    print(json.dumps({"saved": str(target), "summary": summary}, ensure_ascii=False, indent=2))


def cmd_outcome(args: argparse.Namespace) -> None:
    root = as_path(args.root)
    record_path = root / "interviews" / args.id / "record.json"
    if not record_path.exists():
        raise SystemExit(f"unknown interview_id: {args.id}")
    if args.status not in OUTCOMES:
        raise SystemExit(f"invalid outcome: {args.status}")
    record = read_json(record_path)
    if args.feedback and args.feedback_file:
        raise SystemExit("Use either --feedback or --feedback-file, not both")
    feedback = args.feedback
    if args.feedback_file:
        feedback = as_path(args.feedback_file).read_text(encoding="utf-8-sig")
    outcome = {"status": args.status, "date": args.date or now_iso(), "feedback": feedback, "source": args.source}
    previous = record.get("outcome")
    record["outcome"] = outcome
    atomic_json(record_path, record)
    event = {
        "event_id": f"{args.id}:{now_iso()}", "interview_id": args.id, "recorded_at": now_iso(),
        "original_verdict": record.get("verdict"), "previous_outcome": previous, "actual_outcome": outcome,
        "prediction_error_hypotheses": []
    }
    with (root / "calibration-events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(json.dumps({"updated": str(record_path), "event": event, "summary": rebuild(root)}, ensure_ascii=False, indent=2))


def cmd_delete(args: argparse.Namespace) -> None:
    if not args.yes:
        raise SystemExit("Deletion requires --yes")
    root = as_path(args.root)
    target = root / "interviews" / args.id
    if not target.exists() or target.parent != root / "interviews":
        raise SystemExit(f"unknown interview_id: {args.id}")
    shutil.rmtree(target)
    print(json.dumps({"deleted": args.id, "summary": rebuild(root)}, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PM Interview Review OS local history manager")
    p.add_argument("--root", default=str(default_root()), help="workspace root")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    sub.add_parser("rebuild")
    v = sub.add_parser("validate-record")
    v.add_argument("record")
    s = sub.add_parser("save")
    s.add_argument("--record", required=True)
    s.add_argument("--review")
    s.add_argument("--transcript")
    s.add_argument("--manifest")
    s.add_argument("--overwrite", action="store_true")
    o = sub.add_parser("outcome")
    o.add_argument("--id", required=True)
    o.add_argument("--status", required=True, choices=sorted(OUTCOMES))
    o.add_argument("--date")
    o.add_argument("--feedback", help="inline recruiter/interviewer feedback text")
    o.add_argument("--feedback-file", help="UTF-8 text file containing feedback")
    o.add_argument("--source")
    d = sub.add_parser("delete")
    d.add_argument("--id", required=True)
    d.add_argument("--yes", action="store_true")
    return p


def main() -> None:
    args = build_parser().parse_args()
    root = as_path(args.root)
    if args.command == "init":
        init_workspace(root)
        print(json.dumps({"initialized": str(root)}, ensure_ascii=False))
    elif args.command == "status":
        init_workspace(root)
        summary_path = root / "aggregates" / "summary.json"
        summary = read_json(summary_path) if summary_path.exists() else rebuild(root)
        print(json.dumps({"root": str(root), **summary}, ensure_ascii=False, indent=2))
    elif args.command == "rebuild":
        print(json.dumps(rebuild(root), ensure_ascii=False, indent=2))
    elif args.command == "validate-record":
        errors = validate_record(read_json(as_path(args.record)))
        if errors:
            print("\n".join(errors), file=sys.stderr)
            raise SystemExit(2)
        print("VALID")
    elif args.command == "save":
        cmd_save(args)
    elif args.command == "outcome":
        cmd_outcome(args)
    elif args.command == "delete":
        cmd_delete(args)


if __name__ == "__main__":
    main()
