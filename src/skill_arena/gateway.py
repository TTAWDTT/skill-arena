from __future__ import annotations

import json
import time
import uuid
from typing import Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter


class GatewayError(RuntimeError):
    pass


class GatewayClient:
    """Minimal model gateway Responses API client.

    Auth:
      - Authorization: Bearer <MODEL_GATEWAY_API_KEY> or MODEL_GATEWAY_USER_TOKEN
      - and/or query param ak=<MODEL_GATEWAY_AK>

    Endpoint:
      POST {base_url}/responses
    """

    def __init__(
        self,
        base_url: str,
        api_key: str = "",
        ak: str = "",
        timeout: float = 180.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.ak = ak
        self.timeout = timeout
        if not api_key and not ak:
            raise GatewayError(
                "Missing MODEL_GATEWAY_API_KEY / MODEL_GATEWAY_USER_TOKEN or MODEL_GATEWAY_AK. "
                "Copy .env.example → .env and fill credentials."
            )

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "X-TT-LOGID": f"skill-arena-{uuid.uuid4().hex[:16]}",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            # Some gateways also accept api-key style
            headers["api-key"] = self.api_key
        return headers

    def _url(self, path: str) -> str:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if self.ak:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}ak={self.ak}"
        return url

    @retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(1, 8), reraise=True)
    def responses_create(
        self,
        *,
        model: str,
        input: Any,
        instructions: Optional[str] = None,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        extra: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": model, "input": input}
        if instructions:
            payload["instructions"] = instructions
        if temperature is not None:
            payload["temperature"] = temperature
        if max_output_tokens is not None:
            payload["max_output_tokens"] = max_output_tokens
        if extra:
            payload.update(extra)

        started = time.perf_counter()
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(
                self._url("responses"),
                headers=self._headers(),
                json=payload,
            )
        latency_ms = int((time.perf_counter() - started) * 1000)
        if resp.status_code >= 400:
            raise GatewayError(
                f"Gateway HTTP {resp.status_code}: {resp.text[:800]}"
            )
        data = resp.json()
        data["_skill_arena"] = {"latency_ms": latency_ms}
        return data

    @staticmethod
    def extract_text(response: dict[str, Any]) -> str:
        """Best-effort text extraction from Responses API payloads."""
        if not isinstance(response, dict):
            return str(response)

        # Common: output_text
        if isinstance(response.get("output_text"), str) and response["output_text"]:
            return response["output_text"]

        chunks: list[str] = []
        for item in response.get("output") or []:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "message":
                for part in item.get("content") or []:
                    if not isinstance(part, dict):
                        continue
                    if part.get("type") in ("output_text", "text") and part.get("text"):
                        chunks.append(str(part["text"]))
            elif item.get("type") in ("output_text", "text") and item.get("text"):
                chunks.append(str(item["text"]))
        if chunks:
            return "\n".join(chunks)

        # Chat-completions-like fallback
        choices = response.get("choices") or []
        if choices and isinstance(choices[0], dict):
            msg = choices[0].get("message") or {}
            if isinstance(msg.get("content"), str):
                return msg["content"]

        # Last resort
        try:
            return json.dumps(response, ensure_ascii=False)[:4000]
        except Exception:
            return str(response)[:4000]

    @staticmethod
    def usage_tokens(response: dict[str, Any]) -> tuple[Optional[int], Optional[int]]:
        usage = response.get("usage") or {}
        if not isinstance(usage, dict):
            return None, None
        inp = usage.get("input_tokens")
        if inp is None:
            inp = usage.get("prompt_tokens")
        out = usage.get("output_tokens")
        if out is None:
            out = usage.get("completion_tokens")
        return (
            int(inp) if inp is not None else None,
            int(out) if out is not None else None,
        )
