from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import types
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_feishu_review import build_feishu_review, validate_feishu_review  # noqa: E402
from codex_feishu_bridge import (  # noqa: E402
    find_codex,
    job_id,
    personal_codex_env,
    process_downloaded,
    run_bridge,
)
from feishu_common import (  # noqa: E402
    FIXED_TENANT_DOMAIN,
    FIXED_WIKI_SPACE_ID,
    ConfigurationError,
    FeishuAPI,
    feishu_config,
    load_config,
    wiki_url,
)
from publish_feishu_wiki import (  # noqa: E402
    append_blocks,
    create_wiki_node,
    delete_direct_children,
    markdown_to_blocks,
    publish,
    replace_blocks,
    verify_blocks,
)
from validate_review import validate  # noqa: E402


class FakeAPI:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, object]] = []

    def request(self, method: str, path: str, body=None):
        self.calls.append((method, path, body))
        if method == "POST" and path.endswith("/nodes"):
            return {"code": 0, "data": {"node": {"node_token": "wikcn_node", "obj_token": "doccn_obj"}}}
        if method == "GET" and path.endswith("blocks?page_size=50"):
            return {"code": 0, "data": {"items": [{"block_id": "root"}, {"block_id": "child"}]}}
        return {"code": 0, "data": {}}


class PaginatedBlocksAPI:
    def __init__(self) -> None:
        self.paths: list[str] = []

    def request(self, method: str, path: str, body=None):
        if method != "GET" or body is not None:
            raise AssertionError("unexpected request")
        self.paths.append(path)
        if "page_token=next%20page" in path:
            return {
                "code": 0,
                "data": {"items": [{"block_id": "child-2"}], "has_more": False},
            }
        return {
            "code": 0,
            "data": {
                "items": [{"block_id": "root"}, {"block_id": "child-1"}],
                "has_more": True,
                "page_token": "next page",
            },
        }


class MutableDocumentAPI:
    def __init__(self, child_count: int) -> None:
        self.children = [
            {"block_id": f"child-{index}", "text": {"elements": []}}
            for index in range(child_count)
        ]
        self.calls: list[tuple[str, str, object]] = []

    def request(self, method: str, path: str, body=None):
        self.calls.append((method, path, body))
        if method == "GET" and "/children?" in path:
            return {"code": 0, "data": {"items": list(self.children)}}
        if method == "DELETE" and path.endswith("batch_delete?document_revision_id=-1"):
            start = body["start_index"]
            end = body["end_index"]
            del self.children[start:end]
            return {"code": 0, "data": {}}
        if method == "POST" and path.endswith("/children"):
            self.children.extend(body["children"])
            return {"code": 0, "data": {}}
        if method == "GET" and path.endswith("blocks?page_size=50"):
            return {
                "code": 0,
                "data": {"items": [{"block_id": "root"}, *self.children]},
            }
        raise AssertionError(f"unexpected request: {method} {path}")


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode("utf-8")
        self.headers: dict[str, str] = {}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self) -> bytes:
        return self._raw


class FeishuAutomationTests(unittest.TestCase):
    def test_feishu_edition_removes_candidate_answers_and_private_diagnostics(self) -> None:
        private = """# 0. 面试实录与回答建议

## 0.1 面试官提问与候选人回复

### Q01 — Root
- 问题 anchor：[00:01–00:02]
**面试官原文**
> 请介绍项目
- 回答 anchor：[00:02–00:10]
- 状态：captured
- Speaker：Candidate
**候选人原回复**
> PRIVATE ANSWER

## 0.2 回答建议

### Q01
> 建议先讲目标，再讲决策。

## 0.3 候选人反问

### RQ01
- 候选人反问原文：团队目标是什么？
- 面试官回答原文：关注创作工具增长。

# 1. Executive Summary
- Overall Performance: 4/10
# 6. Key Answer Reviews
### Candidate Answer — Clean Version
PRIVATE DIAGNOSIS
"""
        public = build_feishu_review(private)
        self.assertEqual(validate_feishu_review(public), [])
        self.assertIn("请介绍项目", public)
        self.assertIn("建议先讲目标", public)
        self.assertIn("团队目标是什么", public)
        self.assertIn("关注创作工具增长", public)
        self.assertNotIn("PRIVATE ANSWER", public)
        self.assertNotIn("PRIVATE DIAGNOSIS", public)
        self.assertNotIn("Overall Performance", public)
        self.assertNotIn("候选人原回复", public)

    def test_publisher_rejects_private_full_review_and_accepts_sanitized_dry_run(self) -> None:
        private = (ROOT / "examples/test-run-output.md").read_text(encoding="utf-8-sig")
        public = build_feishu_review(private)
        with tempfile.TemporaryDirectory() as folder:
            private_path = Path(folder) / "review.private.md"
            public_path = Path(folder) / "review.feishu.md"
            private_path.write_text(private, encoding="utf-8")
            public_path.write_text(public, encoding="utf-8")
            with self.assertRaises(ValueError):
                publish(private_path, "private must fail", dry_run=True)
            result = publish(public_path, "public", dry_run=True)
            self.assertEqual(result["status"], "dry-run")
            self.assertTrue(result["privacy_safe"])

    def test_bridge_keeps_private_review_and_publishes_only_feishu_edition(self) -> None:
        fixture = (ROOT / "examples/test-run-output.md").read_text(encoding="utf-8-sig")
        with tempfile.TemporaryDirectory() as folder:
            job_dir = Path(folder)
            transcript = job_dir / "transcript.txt"
            transcript.write_text("test transcript", encoding="utf-8")

            def fake_codex(*_args, **_kwargs):
                (job_dir / "review.private.md").write_text(fixture, encoding="utf-8")

            with (
                patch("codex_feishu_bridge.run_checked", side_effect=fake_codex),
                patch(
                    "codex_feishu_bridge.publish",
                    return_value={"status": "verified", "url": "https://example.invalid/wiki/node"},
                ) as publish_mock,
            ):
                process_downloaded(
                    transcript,
                    job_dir=job_dir,
                    codex="codex",
                    config_file=None,
                    title="privacy test",
                )

            self.assertTrue((job_dir / "review.private.md").is_file())
            public = (job_dir / "review.feishu.md").read_text(encoding="utf-8")
            self.assertEqual(validate_feishu_review(public), [])
            published_path = publish_mock.call_args.args[0]
            self.assertEqual(published_path, job_dir / "review.feishu.md")
            self.assertTrue(publish_mock.call_args.kwargs["privacy_safe"])

    def test_windows_codex_lookup_falls_back_to_user_npm_directory(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            npm = Path(folder) / "npm"
            npm.mkdir()
            expected = npm / "codex.cmd"
            expected.write_text("@echo off\n", encoding="ascii")
            with (
                patch("codex_feishu_bridge.shutil.which", return_value=None),
                patch.dict(os.environ, {"APPDATA": folder}),
            ):
                self.assertEqual(find_codex(), str(expected))

    def test_bridge_starts_channel_without_nesting_an_event_loop(self) -> None:
        calls: list[object] = []

        class FakePolicyConfig:
            def __init__(self, **kwargs):
                calls.append(("policy", kwargs))

        class FakeChannel:
            def __init__(self, **kwargs):
                calls.append(("channel", kwargs))

            def on(self, name, handler):
                calls.append(("on", name, callable(handler)))

            def start(self):
                calls.append("start")

        fake_sdk = types.SimpleNamespace(
            FeishuChannel=FakeChannel,
            PolicyConfig=FakePolicyConfig,
        )
        config = {"feishu": {"dm_enabled": True, "allowed_chat_ids": []}}
        with (
            patch.dict(sys.modules, {"lark_channel": fake_sdk}),
            patch("codex_feishu_bridge.load_config", return_value=config),
            patch("codex_feishu_bridge.feishu_config", return_value=config["feishu"]),
            patch("codex_feishu_bridge.require_feishu_credentials", return_value=("app", "secret")),
            patch("codex_feishu_bridge.ensure_personal_codex", return_value=Path("codex")),
        ):
            run_bridge(None)

        self.assertEqual(calls[-1], "start")
        self.assertIn(("on", "message", True), calls)

    def test_markdown_conversion_uses_expected_block_types(self) -> None:
        blocks = markdown_to_blocks("# 标题\n\n- 列表\n\n1. 顺序\n\n> 引用\n\n```\ncode\n```\n")
        self.assertEqual([x["block_type"] for x in blocks], [3, 12, 13, 15, 14])

    def test_wiki_create_append_and_verify_contract(self) -> None:
        api = FakeAPI()
        node, obj = create_wiki_node(
            api,
            {"space_id": "spc 1", "parent_node_token": "wikcn_parent"},
            "测试复盘",
        )
        self.assertEqual((node, obj), ("wikcn_node", "doccn_obj"))
        blocks = markdown_to_blocks("\n\n".join(f"段落 {i}" for i in range(55)))
        append_blocks(api, obj, blocks)
        self.assertEqual(sum(1 for method, path, _ in api.calls if method == "POST" and path.endswith("/children")), 2)
        self.assertEqual(verify_blocks(api, obj), 2)
        self.assertIn("spaces/spc%201/nodes", api.calls[0][1])

    def test_block_verification_reads_every_page_and_checks_expected_count(self) -> None:
        api = PaginatedBlocksAPI()
        self.assertEqual(
            verify_blocks(api, "doc id", expected_content_blocks=2),
            3,
        )
        self.assertEqual(len(api.paths), 2)
        self.assertIn("page_token=next%20page", api.paths[1])

    def test_existing_document_replacement_deletes_tail_batches_and_verifies_text(self) -> None:
        api = MutableDocumentAPI(121)
        replacement = markdown_to_blocks("# 脱敏版\n\n保留面试官原文和回答建议。")
        removed, verified = replace_blocks(api, "doc id", replacement)
        self.assertEqual(removed, 121)
        self.assertEqual(verified, len(replacement) + 1)
        delete_bodies = [
            body for method, _, body in api.calls if method == "DELETE"
        ]
        self.assertEqual(
            delete_bodies,
            [
                {"start_index": 71, "end_index": 121},
                {"start_index": 21, "end_index": 71},
                {"start_index": 0, "end_index": 21},
            ],
        )

    def test_delete_rejects_unsafe_batch_size(self) -> None:
        with self.assertRaises(ValueError):
            delete_direct_children(MutableDocumentAPI(1), "doc", batch_size=51)

    def test_config_rejects_persisted_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            path.write_text(json.dumps({"app_secret": "must-not-persist"}), encoding="utf-8")
            with self.assertRaises(ConfigurationError):
                load_config(path)

    def test_child_codex_environment_strips_api_routing(self) -> None:
        old = {key: os.environ.get(key) for key in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_API_BASE")}
        try:
            for key in old:
                os.environ[key] = "must-not-leak"
            child = personal_codex_env()
            for key in old:
                self.assertNotIn(key, child)
        finally:
            for key, value in old.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_idempotency_key_is_stable_and_scoped(self) -> None:
        self.assertEqual(job_id("om_1", "file_1"), job_id("om_1", "file_1"))
        self.assertNotEqual(job_id("om_1", "file_1"), job_id("om_1", "file_2"))

    def test_combined_fixture_passes_automated_contract(self) -> None:
        text = (ROOT / "examples/test-run-output.md").read_text(encoding="utf-8-sig")
        self.assertEqual(validate(text, automated=True), [])

    def test_wiki_url_requires_real_tenant_domain_input(self) -> None:
        self.assertEqual(wiki_url("example.feishu.cn", "wikcn_node"), "https://example.feishu.cn/wiki/wikcn_node")

    def test_feishu_target_is_locked_to_the_organization_wiki(self) -> None:
        expected = {
            "tenant_domain": FIXED_TENANT_DOMAIN,
            "space_id": FIXED_WIKI_SPACE_ID,
        }
        self.assertEqual(feishu_config({"feishu": expected}), expected)
        with self.assertRaises(ConfigurationError):
            feishu_config(
                {
                    "feishu": {
                        "tenant_domain": FIXED_TENANT_DOMAIN,
                        "space_id": "another-space",
                    }
                }
            )
        with self.assertRaises(ConfigurationError):
            feishu_config(
                {
                    "feishu": {
                        **expected,
                        "publish_candidate_answers": True,
                    }
                }
            )

    @patch("feishu_common.time.sleep", return_value=None)
    def test_feishu_client_retries_rate_limit(self, _sleep) -> None:
        attempts = 0

        def urlopen(_request, timeout):
            nonlocal attempts
            self.assertEqual(timeout, 30)
            attempts += 1
            if attempts == 1:
                raise urllib.error.HTTPError(
                    "https://open.feishu.cn/open-apis/token",
                    429,
                    "rate limited",
                    {},
                    io.BytesIO(b'{"code": 429}'),
                )
            return FakeResponse({"code": 0, "tenant_access_token": "tenant-token"})

        api = FeishuAPI("app-id", "app-secret", urlopen=urlopen)
        self.assertEqual(api.tenant_token(), "tenant-token")
        self.assertEqual(attempts, 2)


if __name__ == "__main__":
    unittest.main()
