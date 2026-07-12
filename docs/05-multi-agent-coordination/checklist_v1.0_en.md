# Multi-Agent Coordination Checklist (v1.0)

> **Purpose**: Sign-off gate before running concurrent agents on the same codebase.
> **How to use**: Fill out BEFORE starting any multi-agent run. If any mandatory gate is unchecked, **do not run concurrently**.
> **Related**: [中文版](checklist_v1.0_zh.md)

---

# Multi-Agent Coordination Checklist: <Project / Run Name>

> **Date**: YYYY-MM-DD
> **Reviewer**: <name>
> **Agent(s) involved**: <agent-1, agent-2, ...>

---

## Pre-requisite gates

- [ ] **Stage 4 (Test Plan) signed off** for the project
- [ ] **Stage 3 (Plan) signed off** for the project
- [ ] **All concurrent task cards have `## Target Files` sections** (Layer 1 prerequisite)
- [ ] **All concurrent task cards pass `validate-card`** (Target Files syntactically valid)

---

## Layer 1 gates (Declaration)

- [ ] **Every concurrent task declares its Target Files** in its Kanban card body
- [ ] **No overlapping Target Files** between concurrent tasks (verified by overlap detector)
- [ ] **Target Files paths are project-root relative** (no `/`, `./`, or absolute paths)
- [ ] **Section heading matches lenient spec** (`## Target Files` or equivalent)

---

## Layer 2 gates (Isolation)

- [ ] **Each agent runs in its own worktree** at `.worktrees/<task_id>`
- [ ] **Branch naming follows convention** `wt/<task_id>`
- [ ] **Main checkout is untouched** during agent runs
- [ ] **No shared mutable state** between worktrees (e.g., shared tmpfiles, shared dev servers)

---

## Layer 3 gates (Detection)

- [ ] **BASE_SHA captured at run start** for every agent
- [ ] **`git fetch origin main` ran at run start** (so BASE_SHA is recent)
- [ ] **Stale-base detection script scheduled** to run before patch generation
- [ ] **Patch format includes both SHAs** when stale-base detected

---

## Patch handoff gates

- [ ] **Patch lands in `docs/pending-reviews/`**, not as direct commit
- [ ] **Patch filename follows convention** `<task_id>_<timestamp>.patch`
- [ ] **Patch header includes required fields**: From, Date, Subject, Base-SHA-Start, Base-SHA-End, Task-ID, Target-Files
- [ ] **Human review scheduled** before patch lands in main

---

## Commit authority gates

- [ ] **No agent has direct commit rights to `main`** / protected branch
- [ ] **Agents only commit to `wt/<task_id>` branches**
- [ ] **Patch application is human-driven** (Ezio or pre-authorized designated reviewer)
- [ ] **`11-governance` rules respected** (see [`../11-governance/_index_en.md`](../11-governance/_index_en.md))

---

## Quality gates

Strongly recommended (not strict, but skipping usually means the multi-agent setup isn't ready).

- [ ] **Concurrent task count is realistic** — not 10 agents on one codebase simultaneously
- [ ] **Tasks have explicit dependencies** (which Tasks block which)
- [ ] **Communication channel between agents exists** (e.g., shared notes file, Kanban comments)
- [ ] **Failure recovery is planned** — what if an agent crashes mid-run? Stale worktree cleanup?

---

## Self-check questions

1. **Could two agents both edit `core/scoring.py` at the same time?** If yes, Layer 1 is broken.
2. **Could an agent's run modify the main checkout by accident?** If yes, Layer 2 is broken.
3. **Could an agent silently undo another agent's commit?** If yes, Layer 3 is broken.
4. **Could an agent's commit land in `main` without human review?** If yes, Commit Authority is broken.

If any answer is "yes, that's possible", **do not start the multi-agent run**.

---

## Sign-off

- [ ] All pre-requisite gates checked
- [ ] All 3 Layer gates checked (Declaration + Isolation + Detection)
- [ ] Patch handoff gates checked
- [ ] Commit authority gates checked
- [ ] Quality gates addressed (or explicitly waived with reason)
- [ ] Self-check questions: all 4 answered "no"

**Reviewer signature**: ___________________
**Date**: ___________________

---

> Once signed off, concurrent agent runs may begin. See [`../06-implementation/_index_en.md`](../06-implementation/_index_en.md) for how individual Tasks consume this protocol.