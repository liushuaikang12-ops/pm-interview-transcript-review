#!/usr/bin/env python
"""Shared configuration and Feishu OpenAPI helpers."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

DEFAULT_HOME = Path.home() / ".pm-interview-review-os"
CONFIG_ENV = "PM_INTERVIEW_REVIEW_CONFIG"
FIXED_TENANT_DOMAIN = "vcnvx4cwol1n.feishu.cn"
FIXED_WIKI_SPACE_ID = "7677796340709133492"


class ConfigurationError(RuntimeError):
    pass


class FeishuAPIError(RuntimeError):
    def __init__(self, message: str, *, code: Any = None, log_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.log_id = log_id


def runtime_home() -> Path:
    value = os.environ.get("PM_INTERVIEW_REVIEW_HOME")
    return Path(value).expanduser() if value else DEFAULT_HOME


def config_path(explicit: str | Path | None = None) -> Path:
    value = explicit or os.environ.get(CONFIG_ENV)
    return Path(value).expanduser() if value else runtime_home() / "config.json"


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_config(explicit: str | Path | None = None) -> dict[str, Any]:
    path = config_path(explicit)
    if not path.exists():
        raise ConfigurationError(
            f"configuration not found: {path}; run scripts/setup_codex_feishu.py first"
        )
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ConfigurationError("configuration root must be an object")
    forbidden = {"app_secret", "openai_api_key", "api_key"}
    serialized = json.dumps(data, ensure_ascii=False).lower()
    present = [name for name in forbidden if f'"{name}"' in serialized]
    if present:
        raise ConfigurationError(
            "secrets must not be stored in config: " + ", ".join(sorted(present))
        )
    return data


def require_feishu_credentials() -> tuple[str, str]:
    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    if os.name == "nt" and (not app_id or not app_secret):
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                if not app_id:
                    app_id = str(winreg.QueryValueEx(key, "FEISHU_APP_ID")[0]).strip()
                if not app_secret:
                    app_secret = str(winreg.QueryValueEx(key, "FEISHU_APP_SECRET")[0]).strip()
        except FileNotFoundError:
            pass
    if not app_id or not app_secret:
        raise ConfigurationError(
            "FEISHU_APP_ID and FEISHU_APP_SECRET must be set for the current user"
        )
    return app_id, app_secret


def feishu_config(config: dict[str, Any]) -> dict[str, Any]:
    value = config.get("feishu")
    if not isinstance(value, dict):
        raise ConfigurationError("missing feishu configuration")
    for key in ("space_id", "tenant_domain"):
        if not str(value.get(key, "")).strip():
            raise ConfigurationError(f"missing feishu.{key}")
    if str(value["tenant_domain"]).strip() != FIXED_TENANT_DOMAIN:
        raise ConfigurationError(
            f"feishu.tenant_domain must be the fixed organization domain {FIXED_TENANT_DOMAIN}"
        )
    if str(value["space_id"]).strip() != FIXED_WIKI_SPACE_ID:
        raise ConfigurationError(
            f"feishu.space_id must be the fixed organization Wiki {FIXED_WIKI_SPACE_ID}"
        )
    if value.get("publish_candidate_answers") is True:
        raise ConfigurationError(
            "feishu.publish_candidate_answers must remain false for the shared Wiki"
        )
    return value


class FeishuAPI:
    def __init__(
        self,
        app_id: str,
        app_secret: str,
        *,
        base_url: str = "https://open.feishu.cn/open-apis",
        timeout: int = 30,
        max_attempts: int = 3,
        urlopen: Callable[..., Any] = urllib.request.urlopen,
    ) -> None:
        self.app_id = app_id
        self._app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_attempts = max(1, max_attempts)
        self._urlopen = urlopen
        self._tenant_token: str | None = None

    def tenant_token(self) -> str:
        if self._tenant_token:
            return self._tenant_token
        payload = self._request_raw(
            "POST",
            "/auth/v3/tenant_access_token/internal",
            {"app_id": self.app_id, "app_secret": self._app_secret},
            authenticated=False,
        )
        token = str(payload.get("tenant_access_token", "")).strip()
        if not token:
            raise FeishuAPIError("tenant token response did not contain tenant_access_token")
        self._tenant_token = token
        return token

    def request(self, method: str, path: str, body: Any = None) -> dict[str, Any]:
        return self._request_raw(method, path, body, authenticated=True)

    def _request_raw(
        self, method: str, path: str, body: Any, *, authenticated: bool
    ) -> dict[str, Any]:
        url = self.base_url + (path if path.startswith("/") else "/" + path)
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if authenticated:
            headers["Authorization"] = f"Bearer {self.tenant_token()}"
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        for attempt in range(1, self.max_attempts + 1):
            try:
                with self._urlopen(request, timeout=self.timeout) as response:
                    raw = response.read()
                    log_id = response.headers.get("X-Tt-Logid")
                break
            except urllib.error.HTTPError as exc:
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if retryable and attempt < self.max_attempts:
                    time.sleep(min(2 ** (attempt - 1), 4))
                    continue
                raw = exc.read()
                log_id = exc.headers.get("X-Tt-Logid") if exc.headers else None
                message = raw.decode("utf-8", errors="replace")[:1000]
                raise FeishuAPIError(
                    f"Feishu HTTP {exc.code}: {message}", code=exc.code, log_id=log_id
                ) from exc
            except urllib.error.URLError as exc:
                if attempt < self.max_attempts:
                    time.sleep(min(2 ** (attempt - 1), 4))
                    continue
                raise FeishuAPIError(f"Feishu network error: {exc.reason}") from exc
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError as exc:
            raise FeishuAPIError("Feishu returned invalid JSON", log_id=log_id) from exc
        code = payload.get("code", 0)
        if code not in (0, None):
            raise FeishuAPIError(
                f"Feishu API error {code}: {payload.get('msg', 'unknown error')}",
                code=code,
                log_id=log_id,
            )
        return payload


def quote_path(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def wiki_url(tenant_domain: str, node_token: str) -> str:
    domain = tenant_domain.strip().rstrip("/")
    if not domain.startswith(("http://", "https://")):
        domain = "https://" + domain
    return f"{domain}/wiki/{node_token}"
