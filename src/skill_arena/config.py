from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "default.yaml"


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_config(path: Path | None = None) -> dict[str, Any]:
    load_dotenv()
    cfg_path = path or DEFAULT_CONFIG
    with cfg_path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    models = cfg.setdefault("models", {})
    models["executor"] = os.getenv(
        "SKILL_ARENA_EXECUTOR_MODEL", models.get("executor", "gpt-5.6-luna")
    )
    models["judge"] = os.getenv(
        "SKILL_ARENA_JUDGE_MODEL", models.get("judge", "gpt-5.6-sol")
    )

    eval_cfg = cfg.setdefault("eval", {})
    if os.getenv("SKILL_ARENA_REPEATS"):
        eval_cfg["repeats"] = int(os.environ["SKILL_ARENA_REPEATS"])

    cfg["modelhub"] = {
        "base_url": os.getenv(
            "MODELHUB_BASE_URL",
            "https://agihub.bytedance.net/api_proxy/modelhub/agent-cn-01/api/modelhub/online",
        ),
        "api_key": os.getenv("MODELHUB_API_KEY") or os.getenv("AGIHUB_USER_TOKEN") or "",
        "ak": os.getenv("MODELHUB_AK") or "",
    }
    cfg["root"] = str(ROOT)
    return cfg


def resolve_path(cfg: dict[str, Any], key: str) -> Path:
    rel = cfg["paths"][key]
    p = Path(rel)
    if not p.is_absolute():
        p = Path(cfg["root"]) / p
    p.mkdir(parents=True, exist_ok=True)
    return p
