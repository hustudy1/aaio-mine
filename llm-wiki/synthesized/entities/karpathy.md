---
title: Andrej Karpathy
type: entity
sources:
  - path: ../../raw/llm-wiki-decision-202606.md
    ts: 2026-06-05T00:00:00+09:00
    claim: "LLM Wiki 패턴 원본 gist 작성자, 2026-04 공개, 5K+ star"
cross_links:
  - ../concepts/llm-wiki-pattern.md
confidence: 0.90
last_synthesized_at: 2026-06-05T00:00:00+09:00
agent: claude-code
schema_version: "1.0"
---

# Andrej Karpathy

OpenAI 공동창립 멤버, Tesla AI 리더 (former). LLM 관련 교육 · 연구로 영향력 큼.

## LLM Wiki 와의 관계

2026-04 에 gist 형식으로 LLM Wiki 패턴 공개. 며칠 만에 5K+ star.

핵심 framing — "Obsidian 은 IDE, LLM 은 programmer, wiki 는 codebase." 사람은 wiki 직접 편집 거의 안 함, LLM 이 maintainer 역할.

본인의 RAG 한계 진단 — "the LLM is rediscovering knowledge from scratch on every question. There's no accumulation." LLM Wiki 는 그 누적을 가능하게 하는 패턴.

## 의도적 추상화

원본 gist 명시 — "This document is intentionally abstract... The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs."

즉 사용자 도메인 · 선호 · LLM 선택에 따라 instantiate 해야 함. starter 의 sandbox 는 그 instantiation 의 한 예시 — 사용자가 본인 통제권 보존하며 작은 격리 환경에서 검증.

## 관련

- [LLM Wiki Pattern](../concepts/llm-wiki-pattern.md) — 본 entity 가 작성한 핵심 개념
