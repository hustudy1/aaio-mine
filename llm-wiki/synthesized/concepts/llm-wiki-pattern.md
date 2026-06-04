---
title: LLM Wiki Pattern
type: concept
sources:
  - path: ../../raw/llm-wiki-decision-202606.md
    ts: 2026-06-05T00:00:00+09:00
    claim: "Karpathy 의 LLM Wiki 패턴 정의 및 vendor-neutral 의도 명시"
cross_links:
  - ../entities/karpathy.md
  - ../topics/sandbox-vs-ecosystem-wide.md
confidence: 0.95
last_synthesized_at: 2026-06-05T00:00:00+09:00
agent: claude-code
schema_version: "1.0"
---

# LLM Wiki Pattern

Andrej Karpathy 가 2026-04 에 공개한 지식 관리 패턴. raw 자료 (외부 문서 · 회의록 · 영상 자막 등) 를 LLM 이 1회 컴파일해서 사람이 읽는 markdown wiki 로 누적하는 구조.

## RAG 와의 핵심 차이

| | RAG | LLM Wiki |
|---|---|---|
| 저장 단위 | embedding 벡터 chunk | 사람 읽는 markdown 페이지 |
| Query 시 처리 | semantic search → LLM 합성 (매번) | wiki 페이지 read (1회 합성) |
| 누적 효과 | 인덱스 size 증가 | 합성된 페이지 자체 진화 |
| 사람 가독성 | 낮음 (chunk 단위) | 높음 (페이지 단위) |

## vendor-neutral 의도

원본 gist 가 명시 — Codex CLI · Claude Code · OpenCode · Pi 등 어느 LLM Agent 에서도 동작. 본 sandbox 는 그 의도를 두 CLI (Claude + Codex) 호환으로 구현. 정책 SSOT 1 개 (`llm-wiki/policy.yaml`) 에서 양쪽 진입 컴파일.

## starter sandbox 채택 이유

ecosystem-wide 적용 시 Codex 두 라운드 검토에서 식별된 critical risk 13 종이 즉시 적용에 부적합 판단. sandbox 단일 트랙으로 격리하면 blast radius 통제 + 학습 evidence 확보 가능. 사용자 personal 자산 · ai-pkm · OO 본체 · 27 managed projects 영향 0.

## 검증 방법

본 패턴이 동작하는지 검증은 raw 자료를 `llm-wiki/raw/` 에 dump 한 후 "wiki 합성" 발화 시 합성 페이지가 4 카테고리 (concept · entity · topic · timeline) 에 누적되는 양상으로 확인. 사람이 직접 페이지를 browse 해서 의미 있는 합성인지 평가.

## 관련

- [Andrej Karpathy](../entities/karpathy.md) — 본 패턴 원본 작성자
- [Sandbox vs Ecosystem-wide](../topics/sandbox-vs-ecosystem-wide.md) — 적용 범위 결정 흐름
