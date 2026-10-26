import pytest

from skill_arena.config import load_config
from skill_arena.gateway import GatewayClient, GatewayError

GATEWAY_ENV = (
    "MODEL_GATEWAY_URL",
    "MODEL_GATEWAY_API_KEY",
    "MODEL_GATEWAY_USER_TOKEN",
    "MODEL_GATEWAY_AK",
)


@pytest.fixture
def gateway_env(monkeypatch):
    monkeypatch.setattr("skill_arena.config.load_dotenv", lambda path=None: None)
    for key in GATEWAY_ENV:
        monkeypatch.delenv(key, raising=False)
    return monkeypatch


def test_url_unset_or_blank_uses_placeholder(gateway_env):
    assert load_config()["gateway"]["base_url"] == "<YOUR_MODEL_GATEWAY>"
    gateway_env.setenv("MODEL_GATEWAY_URL", "")
    assert load_config()["gateway"]["base_url"] == "<YOUR_MODEL_GATEWAY>"
    gateway_env.setenv("MODEL_GATEWAY_URL", "https://example.invalid/gw")
    assert load_config()["gateway"]["base_url"] == "https://example.invalid/gw"


def test_api_key_preferred_over_user_token(gateway_env):
    gateway_env.setenv("MODEL_GATEWAY_API_KEY", "api-key")
    gateway_env.setenv("MODEL_GATEWAY_USER_TOKEN", "user-token")
    assert load_config()["gateway"]["api_key"] == "api-key"

    gateway_env.setenv("MODEL_GATEWAY_API_KEY", "")
    assert load_config()["gateway"]["api_key"] == "user-token"

    gateway_env.delenv("MODEL_GATEWAY_API_KEY")
    gateway_env.delenv("MODEL_GATEWAY_USER_TOKEN")
    assert load_config()["gateway"]["api_key"] == ""


def test_access_key_alone_is_used(gateway_env):
    gateway_env.setenv("MODEL_GATEWAY_AK", "ak-only")
    cfg = load_config()["gateway"]
    assert cfg["api_key"] == ""
    assert cfg["ak"] == "ak-only"

    client = GatewayClient(cfg["base_url"], api_key=cfg["api_key"], ak=cfg["ak"])
    assert client._url("responses").endswith("?ak=ak-only")


def test_missing_api_key_and_access_key_raises():
    message = "MODEL_GATEWAY_API_KEY / MODEL_GATEWAY_USER_TOKEN or MODEL_GATEWAY_AK"
    with pytest.raises(GatewayError, match=message):
        GatewayClient("https://example.invalid", api_key="", ak="")
