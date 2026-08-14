#!/usr/bin/env python
"""Transcribe local interview audio/video with ffmpeg + faster-whisper."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTENSIONS = {".md", ".txt", ".vtt", ".srt"}


def as_path(value: str) -> Path:
    if os.name == "nt" and len(value) >= 3 and value[0] == "/" and value[1].isalpha() and value[2] == "/":
        value = f"{value[1].upper()}:{value[2:]}"
    return Path(value).expanduser()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def duration_seconds(path: Path) -> float | None:
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path)
        ], text=True, encoding="utf-8", errors="replace").strip()
        return round(float(out), 3)
    except Exception:
        return None


def vtt_time(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{milli:03d}"


def md_time(seconds: float) -> str:
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main() -> None:
    p = argparse.ArgumentParser(description="Local timestamped ASR for interview media")
    p.add_argument("input")
    p.add_argument("--output-dir", required=True)
    p.add_argument("--model", default="small")
    p.add_argument("--language", default="zh", help="language code; use auto for detection")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--compute-type", default="auto")
    p.add_argument("--beam-size", type=int, default=5)
    p.add_argument("--no-vad", action="store_true")
    args = p.parse_args()

    source = as_path(args.input).resolve()
    if not source.exists():
        raise SystemExit(f"input not found: {source}")
    if source.suffix.lower() in TEXT_EXTENSIONS:
        raise SystemExit("Input is already a transcript; preserve it and normalize without ASR.")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg/ffprobe not found")
    try:
        from faster_whisper import WhisperModel
        import ctranslate2
    except Exception as exc:
        raise SystemExit(f"faster-whisper unavailable: {exc}")

    output = as_path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    wav = output / "audio.16k.mono.wav"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])

    if args.device == "auto":
        device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
    else:
        device = args.device
    compute = args.compute_type
    if compute == "auto":
        compute = "float16" if device == "cuda" else "int8"

    model = WhisperModel(args.model, device=device, compute_type=compute)
    language = None if args.language.lower() == "auto" else args.language
    segments_iter, info = model.transcribe(
        str(wav), language=language, beam_size=args.beam_size,
        vad_filter=not args.no_vad, condition_on_previous_text=True
    )
    segments = []
    for i, seg in enumerate(segments_iter, start=1):
        text = seg.text.strip()
        if text:
            segments.append({"id": i, "start": round(seg.start, 3), "end": round(seg.end, 3), "speaker": "Unknown Speaker", "text": text})
    if not segments:
        raise SystemExit("ASR returned no speech segments")

    (output / "transcript.segments.json").write_text(json.dumps(segments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "transcript.txt").write_text("\n".join(x["text"] for x in segments) + "\n", encoding="utf-8")
    vtt = ["WEBVTT", ""]
    md = ["# Timestamped Transcript", "", "> Speaker labels are unresolved ASR placeholders; verify before analysis.", ""]
    for x in segments:
        vtt.extend([str(x["id"]), f"{vtt_time(x['start'])} --> {vtt_time(x['end'])}", x["text"], ""])
        md.append(f"[{md_time(x['start'])}–{md_time(x['end'])}] Unknown Speaker: {x['text']}")
    (output / "transcript.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (output / "transcript.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    metadata = {
        "created_at": now_iso(), "source": str(source), "source_sha256": sha256(source),
        "source_duration_seconds": duration_seconds(source), "wav": str(wav),
        "model": args.model, "device": device, "compute_type": compute,
        "requested_language": args.language, "detected_language": getattr(info, "language", None),
        "language_probability": getattr(info, "language_probability", None),
        "segment_count": len(segments), "speaker_diarization": False,
        "privacy": "local processing; model download may access model host on first use"
    }
    (output / "transcription-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": str(output), **metadata}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"media processing failed: {exc}", file=sys.stderr)
        raise SystemExit(exc.returncode or 2)
