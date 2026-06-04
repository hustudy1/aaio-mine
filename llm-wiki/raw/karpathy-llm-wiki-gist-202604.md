# Karpathy LLM Wiki Gist (2026-04)

본 자료는 Andrej Karpathy 가 2026-04 에 공개한 LLM Wiki 패턴 원본 gist (`442a6bf555914893e9891c11519de94f`) 의 핵심 본문 정리입니다. WebFetch + WebSearch 결과 통합.

## 원본 의도 (직접 인용)

"This document is intentionally abstract. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs."

"This is an idea file designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.)."

## RAG 의 한계 진단

"Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation."

"Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up."

## LLM Wiki Pattern 핵심

"Raw data from a given number of sources is collected, then compiled by an LLM into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM."

## Framing

"In this framing: Obsidian is the IDE. The LLM is the programmer. The wiki is the codebase."

## 유지보수 비용 관점

"The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."

## Wiki 컴포넌트 (원본 명시)

"summaries, entity pages, concept pages, comparisons, an overview, a synthesis". 다만 specific schema 정의 X — "your domain, your preferences, and your LLM of choice 에 따라 결정."

## Raw 자료 입력 형식

"Articles, papers, images, data files" — 종류별 처리 방식 명시 X. 댓글에서 PDF (PyMuPDF), 오피스 문서 (python-docx), 비디오 자막 (Whisper) 처리 논의 있음.

## Workflow

"Ingest sources one at a time" 또는 "batch-ingest" 모두 허용. "It's up to you to develop the workflow."

## 의도적으로 비어 있는 영역 (사용자가 채워야)

1. 데이터 종류별 처리 방식 차이
2. wiki schema (구체적)
3. write trigger / 빈도 / 경계 정책
4. 폴더 포함/제외 / redaction 정책
5. 동시성 정책 (concurrent write — gist 댓글에서 corruption 문제 제기)

## Markdown + Obsidian 선택 이유

"Plain markdown is the right format because it's portable, future-proof, and something LLMs read natively. Obsidian is the best front-end for managing the files — your data stays local and file-based."

## 영향력

2026-04 공개 후 며칠 만에 5K+ star. 다수 open source 구현체 등장 (AgriciDaniel/claude-obsidian, Ar9av/obsidian-wiki, lucasastorian/llmwiki, ussumant/llm-wiki-compiler, MehmetGoekce/llm-wiki, ScrapingArt/Karpathy-LLM-Wiki-Stack 등).
