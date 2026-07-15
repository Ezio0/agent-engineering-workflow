# Positioning Memo: Agent Engineering Workflow

> **Version**: v1.0
> **Date**: 2026-07-15
> **Author**: Ezio Zero (reviewed by Ezio Sun)
> **Status**: Active
>
> Chinese version: `agent_engineering_workflow_positioning_v1.0_2026-07-15.zh.md`

---

## 1. WHO — Target User

**Ezio Sun**, 30+, Hangzhou, Alibaba search product manager. Works on e-commerce search intent understanding by day; builds personal projects with AI agents (Hermes, Claude Code, Codex) on evenings and weekends. He runs 2-3 projects in parallel, each with its own agent team. His pain point isn't "can't use agents" — it's that there are too many agents, too many projects, and rules scattered everywhere. Every new project reinvents the workflow from scratch.

---

## 2. WHY — The Problem

Every agent-driven project **reinvents the workflow**: PRD templates differ across projects, commit authority rules have subtly inconsistent versions across 3 skills, and new agents learn governance boundaries through trial and error. It's not "no documentation" — it's too much documentation, scattered across project `.hermes/` directories, contradicting each other. **The 2026-07-12 incident** (an agent skipped all Gates and shipped code directly) exposed this systemic fragility.

---

## 3. WHY NOW — What's Changed

- **Agent capability inflection**: By mid-2026, AI agents can autonomously complete the full chain from PRD to deployment, but "can do" ≠ "should do" — an agent without Gates is a sports car without brakes
- **Parallel project count crossed the threshold**: The number of simultaneously running projects exceeded what the human brain can track per-project rules for
- **Incident density rising**: 2026-07-10 governance gap, 2026-07-12 PRD bypass — the same class of problem recurring signals systemic absence, not isolated cases

---

## 4. UNDERLYING LOGIC — Why This Approach Works

**Mechanism: Versioned Gates + Automated Checking = Turning tacit knowledge into executable constraints.**

This handbook isn't "advisory documentation" — it encodes rules into `gate-check.py`: Tier auto-detection, chapter completeness validation, signature verification, upstream reference chain. If an agent bypasses a Gate, the script FAILs. This doesn't rely on agent goodwill; it relies on toolchain enforcement.

Remove `gate-check.py`, and the handbook degrades into markdown — agents can ignore it, just like any document. **Tooling is the core mechanism.**

---

## 5. ANTI-POSITIONING — What We Are NOT

- ❌ Not an **Agent Framework** (this handbook doesn't provide an agent runtime, doesn't dispatch agents, doesn't manage agent lifecycles — that's Hermes / OpenClaw's job)
- ❌ Not a **Coding Standard** (this handbook contains no linter rules or style guides — that's the language ecosystem's job; we only govern "when to write code" and "what's required before writing," not "how to write code")
- ❌ Not a **Project Management Tool** (this handbook doesn't replace Jira / Linear / Kanban — it defines "when to use Kanban," but the Kanban itself uses Hermes built-in or external tools)
- ❌ Not an **AI Agent Tutorial** (this handbook assumes readers are already using agents; it doesn't teach "how to talk to agents" or "how to configure agents")

---

Sign-off: Ezio 2026-07-15
