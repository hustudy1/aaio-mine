"""Wiki page frontmatter schema 검증."""
import json
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PAGE_SCHEMA = REPO_ROOT / "schemas" / "llm-wiki-page-v1.json"
FIXTURES = REPO_ROOT / "llm-wiki" / "tests" / "fixtures"


def parse_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert m, f"no frontmatter in {md_path}"
    return yaml.safe_load(m.group(1))


def test_page_schema_loads():
    schema = json.loads(PAGE_SCHEMA.read_text(encoding="utf-8"))
    assert schema["title"] == "LLM Wiki Page Frontmatter v1"
    assert "sources" in schema["required"]


def test_sample_page_valid():
    """valid fixture 가 required 필드 모두 보유."""
    fixture = FIXTURES / "sample_page_valid.md"
    fm = parse_frontmatter(fixture)
    required = ["title", "type", "sources", "cross_links", "confidence",
                "last_synthesized_at", "agent", "schema_version"]
    for field in required:
        assert field in fm, f"required field {field} missing in valid fixture"
    assert len(fm["sources"]) >= 1, "sources must have at least 1 entry"


def test_sample_page_invalid_no_sources():
    """invalid fixture (sources 없음) 가 hallucinated synthesis 차단 영역."""
    fixture = FIXTURES / "sample_page_invalid_no_sources.md"
    fm = parse_frontmatter(fixture)
    assert fm.get("sources", []) == [], "fixture should have empty sources (invalid)"


def test_page_type_enum():
    """type 필드는 4 enum 중 하나."""
    fixture = FIXTURES / "sample_page_valid.md"
    fm = parse_frontmatter(fixture)
    assert fm["type"] in ["concept", "entity", "topic", "timeline"]
