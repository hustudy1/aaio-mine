"""policy.yaml 이 llm-wiki-policy-v1.json schema 정합 검증."""
import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
POLICY_YAML = REPO_ROOT / "llm-wiki" / "policy.yaml"
POLICY_SCHEMA = REPO_ROOT / "schemas" / "llm-wiki-policy-v1.json"


def test_policy_yaml_loads():
    """policy.yaml 가 YAML parse 가능."""
    data = yaml.safe_load(POLICY_YAML.read_text(encoding="utf-8"))
    assert data is not None
    assert "scope" in data
    assert "trigger" in data
    assert "redaction" in data


def test_policy_schema_loads():
    """policy schema 가 JSON parse 가능."""
    schema = json.loads(POLICY_SCHEMA.read_text(encoding="utf-8"))
    assert schema["title"] == "LLM Wiki Policy v1"
    assert "scope" in schema["required"]


def test_policy_required_fields():
    """policy.yaml 가 schema 의 required 필드 모두 보유."""
    data = yaml.safe_load(POLICY_YAML.read_text(encoding="utf-8"))
    schema = json.loads(POLICY_SCHEMA.read_text(encoding="utf-8"))
    for field in schema["required"]:
        assert field in data, f"required field {field} missing in policy.yaml"


def test_policy_forbidden_includes_raw():
    """raw 폴더가 forbidden write 영역에 포함."""
    data = yaml.safe_load(POLICY_YAML.read_text(encoding="utf-8"))
    forbidden = data["scope"]["forbidden"]
    assert any("raw" in f for f in forbidden), "raw must be forbidden write"


def test_policy_trigger_mode_explicit():
    """sandbox 의 trigger mode 는 explicit_user_only."""
    data = yaml.safe_load(POLICY_YAML.read_text(encoding="utf-8"))
    assert data["trigger"]["mode"] == "explicit_user_only"


def test_policy_ecosystem_separation_locked():
    """ai_pkm_watcher false + oo_governance_inherit false 확인."""
    data = yaml.safe_load(POLICY_YAML.read_text(encoding="utf-8"))
    sep = data["ecosystem_separation"]
    assert sep["ai_pkm_watcher"] is False
    assert sep["oo_governance_inherit"] is False
