from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from codex_feishu_bridge import job_id, personal_codex_env  # noqa: E402
from feishu_common import ConfigurationError, FeishuAPI, load_config, wiki_url  # noqa: E402
from publish_feishu_wiki import (  # noqa: E402
    append_blocks,
    create_wiki_node,
    markdown_to_blocks,
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
