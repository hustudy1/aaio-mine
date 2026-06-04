# LLM Wiki Sandbox Tests

본 폴더는 sandbox 동작 검증 fixture 입니다. Codex review 가 식별한 13 critical risk 중 sandbox 에서 실측 가능한 영역의 검증 자산.

## 실행

starter repo 안 .venv 환경에서:

```bash
pip install pytest pyyaml
python -m pytest llm-wiki/tests/ -v
```

## 검증 영역

- `test_policy_schema.py`: policy.yaml 가 JSON Schema 정합 (필수 필드 · forbidden raw · trigger mode · ecosystem 분리)
- `test_page_schema.py`: 합성 페이지 frontmatter 검증 (valid · invalid fixture · type enum)
- `test_pii_patterns.py`: 이메일 · 한국 전화번호 · 주민번호 정규식 정밀도 (positive · false positive)
- `test_lock_behavior.py`: single-session lock 동작 simulate (acquire · block · release · double-release)

## fixture 종류

- `sample_raw_with_pii.md`: PII 검출 테스트 (raw 자료에 PII 포함된 case)
- `sample_page_valid.md`: 정상 합성 페이지 frontmatter
- `sample_page_invalid_no_sources.md`: hallucinated synthesis 차단 검증 (sources 누락)

## 미검증 영역 (Codex 권고, 추후 보강)

- 이중 CLI schema hash 결정론 (Claude · Codex 양쪽 같은 정책 인식)
- PII 의 semantic 검출 (정규식 외 — 예: 이름 · 회사명)
- LLM 합성 페이지의 hallucinated claim 비율 (raw source 와 페이지 claim 매칭)
- 세션 간 hot cache 의 효용 (cold start 시간 측정)
