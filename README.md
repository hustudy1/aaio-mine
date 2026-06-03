# OpenOrchestrator Personal Starter Kit

> Minimal personal Orchestrator scaffold for AI-augmented knowledge workers.
> 5 templates + WBS-first task intake + session-resume protocol + Git-Branch-as-Intent.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE) [![Status: MVP](https://img.shields.io/badge/Status-MVP-orange.svg)](#status)

---

## What it is

A **single-person Orchestrator (OO)** scaffold for anyone who wants to:

- Keep a **single SSOT for their tasks** (`master-wbs.md`) instead of scattered todo apps
- **Resume work from a document, not a chat scrollback** (`session-state.md`)
- Use **Git branches as intent broadcast** to teammates (`wip/T-{id}-{summary}`)
- Capture **5 common work types** as structured tasks (code review / bug investigation / meeting followup / vendor request / approval request)

This is the **MVP / Starter** edition — minimal moving parts, file-first, no infrastructure.

---

## What it is NOT

- ❌ A multi-agent orchestration platform (that is the upstream OpenOrchestrator project, separate)
- ❌ A team project management tool (Linear / Jira / Asana cover that)
- ❌ A knowledge base (Notion / Obsidian cover that)
- ❌ Tied to any specific AI vendor (works with Claude Code, Codex CLI, Cursor, Copilot, Kiro)

It is a **personal coordination layer (L2)** sitting between you and your AI assistant.

---

## Getting Started

### 1. Clone

```bash
git clone https://github.com/{{your-org}}/openorchestrator-starter.git my-oo
cd my-oo
```

### 2. Personalize

Replace `{{이름}}` (or `{{name}}`) placeholders in:
- `CLAUDE.md` (AI entrypoint)
- `master-wbs.md` (your task list header)
- `session-state.md` (your resume pack header)

### 3. First task

```bash
# 1. Add a row to master-wbs.md
# 2. Copy a template
cp templates/code-review.md tasks/task-T-001-my-first-review.md
# 3. Fill in the task
# 4. Commit (broadcasts intent)
git add . && git commit -m "feat: start T-001 code review"
```

### 4. Resume from any AI session

Attach `session-state.md` + `master-wbs.md` to a new AI conversation and say:
> "Resume T-001 from where I left off."

The AI reads your current state from documents, not from the previous chat.

---

## Git Branch as Intent Protocol

Every active task = a `wip/T-{id}-{summary}` branch.

```bash
# Start
git checkout -b wip/T-002-vendor-quote

# Mid-work commit (intent broadcast)
git commit -m "wip: T-002 sent quote request to vendor X"
git push

# Done
git checkout main && git merge wip/T-002-vendor-quote
```

Teammates can `git fetch --all && git branch -r | grep wip/` to see who is doing what — in real time, without a separate status meeting.

---

## File Structure

```
my-oo/
├── CLAUDE.md              # AI entrypoint (rules + quick-start)
├── master-wbs.md          # Your task list (SSOT)
├── session-state.md       # Current state (resume pack)
├── templates/             # 5 task templates
│   ├── code-review.md
│   ├── bug-investigation.md
│   ├── meeting-followup.md
│   ├── vendor-request.md
│   └── approval-request.md
├── tasks/                 # Active task files
├── tasks_done/            # Completed tasks
└── shared_data/inbox/     # Incoming requests (gitignored)
```

---

## Why "Starter"

The upstream **OpenOrchestrator** project is a multi-agent, multi-machine personal AI operations platform with 27+ managed sub-projects, a custom MCP gateway, governance hooks, and a Wave autonomous execution engine.

That is **not** what most people need on day one.

This starter kit is the **single-file-tree subset** that any knowledge worker can adopt in under 30 minutes with no infrastructure. If you outgrow it, the upstream project is the natural next step.

---

## Status

**MVP** — single-user personal scaffold. No multi-agent, no MCP gateway, no governance hooks. The 5 templates + WBS + session-state + Git-Branch-Intent are the minimum viable surface.

Future (not in this starter kit, available in the upstream OpenOrchestrator):
- Multi-agent dispatch (Claude Code + Codex CLI + Cursor + Copilot + Kiro simultaneous)
- 5-Plane Operating Model (Intent / Control / Governance / Execution / Observability)
- MCP Contract Surface (Ingress / Contract normalization / Governed dispatch / Observation handoff)
- Wave autonomous execution
- POER (Periodic Ecosystem Review) bi-weekly self-audit

---

## License

**Apache License 2.0** — see [LICENSE](LICENSE).

Apache 2.0 grants permissive use (commercial, modification, distribution, private use) with the additional protection of an explicit patent grant and explicit termination on patent litigation. This avoids RAIL-family viral clauses and GPL copyleft propagation while keeping standard OSS compatibility.

Copyright 2026 OpenOrchestrator Authors.

---

## Lineage

This starter kit is the **Mode C wrap (a)** of the upstream OpenOrchestrator project (Asset Custody three-mode model: Mode A = personal Core, Mode B = methodology share, Mode C = external wrap product). Only the external-safe scaffold subset is published here. Upstream core (governance hooks, MCP gateway, 27 sub-projects, Tier 1 backend) remains under sole control of the original author.
