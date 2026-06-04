---
name: llm-wiki-sandbox
description: starter 의 llm-wiki/ sandbox 에서 raw 자료를 합성 wiki 페이지로 컴파일. Karpathy LLM Wiki 패턴 적용. ecosystem-wide LLM Wiki 와 분리.
trigger_keywords_korean:
  - "wiki 합성"
  - "wiki 정리"
  - "llm-wiki update"
  - "raw 자료 wiki 화"
  - "Karpathy wiki"
---

# LLM Wiki Sandbox Skill (Claude Code)

## 활성화 조건

사용자가 다음 키워드 발화 시 발동:
- `wiki 합성` / `wiki 정리` / `llm-wiki update` / `raw 자료 wiki 화` / `Karpathy wiki`

## 진입 시 자동 수행

1. `llm-wiki/policy.yaml` Read + `schemas/llm-wiki-policy-v1.json` 으로 검증
2. `llm-wiki/meta/.lock` 존재 확인 — 존재 시 다른 세션 작업 중, 즉시 종료 + 사용자 알림
3. `.lock` 생성 후 작업 시작
4. `llm-wiki/meta/hot.md` Read — 이전 세션 흐름 복구

## 작업 흐름

1. 사용자 의도 확인 — raw 의 어느 자료를 합성?
2. `llm-wiki/raw/` 의 대상 자료 Read
3. policy 의 PII 패턴 detect — 발견 시 `llm-wiki/meta/quarantine/` 로 격리 + 사용자 알림
4. 자료의 의미 단위 식별 — concept · entity · topic · timeline 중 분류
5. `llm-wiki/synthesized/<type>/` 에 페이지 신설 또는 기존 페이지 업데이트
6. frontmatter 는 `schemas/llm-wiki-page-v1.json` 정합 — sources 필수 (각 claim 의 source 추적)
7. cross_links 자동 — 같은 entity 가 다른 페이지에서 언급되면 양쪽 cross_links 갱신
8. `llm-wiki/meta/changelog.md` 에 entry 추가 (ts · agent · action · target_page · source_ref · confidence)

## 종료 시 자동 수행

1. `llm-wiki/meta/hot.md` 갱신 — 본 세션 summary + 다음 세션 진입점
2. `llm-wiki/meta/.lock` 삭제
3. 사용자에게 Layer 4 결과 카드 출력 (intent-alignment 룰 정합)

## 금지

- `llm-wiki/raw/` write 금지 (immutable)
- `llm-wiki/` 외부 폴더 write 금지 (policy.yaml 의 forbidden 영역)
- ecosystem (OO 본체 · ai-pkm · 27 managed projects) 영향 금지
- starter 외부 배포 시 사용자 personal 자산 노출 금지 (redaction layer)

## dual-CLI schema check

세션 시작 시 policy.yaml 의 `schema_version` + `schema_hash` 가 Codex 의 `AGENTS.md` 에서 인식하는 값과 일치하는지 확인. 불일치 시 fail_closed (작업 안 함, 사용자에게 sync 요청).
