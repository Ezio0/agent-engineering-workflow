# Quickstart — 5 Minutes to Get Started

> Goal: Let a first-time reader run through the T1 Lite gate check in 5 minutes.
>
> Chinese version: [QUICKSTART.zh.md](QUICKSTART.zh.md)

---

## Prerequisites

- Python ≥ 3.10 (required by gate-check.py / adr-lint.py)
- git
- An empty directory (new project root) or an existing project

---

## 3-Minute Version: Get T1 Passing

### Step 1: Clone the handbook as reference

```bash
git clone https://github.com/Ezio0/agent-engineering-workflow ~/agent-workflow
```

`~/agent-workflow` below refers to this directory.

### Step 2: Set up your project structure

```bash
cd my-new-project

# Create required directories
mkdir -p docs/00-positioning .kanban .workflow

# Declare Tier (T1 lite)
cat > .workflow/tier <<EOF
tier: T1
justification: Single-module small feature, ~3 days delivery
EOF

# Start a Kanban
cat > .kanban/README.md <<EOF
# Kanban

## In Progress
- T-001 Set up project skeleton
EOF
```

### Step 3: Draft Positioning Memo from template

```bash
cp ~/agent-workflow/docs/00-positioning/template_v1.0_en.md \
   docs/00-positioning/my-project_positioning_v1.0_$(date +%Y-%m-%d).en.md

$EDITOR docs/00-positioning/my-project_positioning_v1.0_*.en.md
```

Positioning Memo answers 5 questions, ≤ 500 words:

- **WHO**: A specific person (not a persona)
- **WHY**: A pain point that exists independent of the product
- **WHY NOW**: A specific trigger (external change / internal accumulation / opportunity window)
- **UNDERLYING LOGIC**: Mechanism, not conclusion
- **ANTI-POSITIONING**: At least 3 things it is NOT

**Signature** last line: `Sign-off: <your name> <YYYY-MM-DD>`.

### Step 4: Gate check

```bash
python3 ~/agent-workflow/scripts/gate-check.py --tier T1 --project-root .
```

Expected output:

```
✅ PASS — Tier T1
```

If FAIL, it will tell you exactly what's missing.

### Step 5: Start implementing

Tier T1 only needs the Positioning Memo to enter Implementation. **Write and test iteratively**, following [Stage 06 Implementation SOP](docs/06-implementation/_index_en.md).

After shipping, do a Retro within 7 days:

```bash
git tag v0.1.0
~/agent-workflow/scripts/retro-init.sh v0.1.0
```

This auto-generates `docs/09-retro/v0.1.0_draft.en.md` skeleton.

---

## Full Version: Get T2 Passing

T2 requires all 5 Gates: Positioning → PRD → Spec → Plan → Test Plan.

See [examples/full-t2/](examples/full-t2/) for a complete example, or copy templates in order:

| Gate | Template | Checklist |
|------|----------|-----------|
| 00 Positioning | `docs/00-positioning/template_v1.0_en.md` | `docs/00-positioning/checklist_v1.0_en.md` |
| 01 PRD | `docs/01-prd/template_v1.0_en.md` | `docs/01-prd/checklist_v1.0_en.md` |
| 02 Spec | `docs/02-spec/template_v1.0_en.md` | `docs/02-spec/checklist_v1.0_en.md` |
| 03 Plan | `docs/03-plan/template_v1.0_en.md` | `docs/03-plan/checklist_v1.0_en.md` |
| 04 Test Plan | `docs/04-test-plan/template_v1.0_en.md` | `docs/04-test-plan/checklist_v1.0_en.md` |

After each Gate, run:

```bash
python3 ~/agent-workflow/scripts/gate-check.py --tier T2 --project-root .
```

All 5 Gates must pass before entering Implementation.

---

## How to Pick a Tier

Not sure between T0/T1/T2? Let the script decide:

```bash
python3 ~/agent-workflow/scripts/gate-check.py --auto-detect-tier --project-root .
```

Rules (hardcoded):

- Single file < 20 lines changed → **T0** (Kanban only)
- Single module, no interface change → **T1** (+ Positioning Memo)
- Cross-module / new API / DB schema / > 200 lines → **T2** (all 5 Gates)

---

## Fast Lane (T0 chore lite card)

Fixing a typo, bumping a dependency? Chore changes still need a Kanban entry, but as a lite card (single-line what+why, no AC/review):

```bash
# Add a line to .kanban/README.md:
echo "- CHORE-001 fix typo in README (link broken)" >> .kanban/README.md

git commit -m "chore: fix typo in README"

python3 ~/agent-workflow/scripts/gate-check.py --tier T0 --project-root .
```

Chore boundary: typo / comments / dependency bump / log wording / formatting / non-core config small change.
**Any logic/interface/test change is NOT chore.**

---

## Next Steps

- See [`examples/minimal-t1/`](examples/minimal-t1/) — complete T1 skeleton
- See [`examples/full-t2/`](examples/full-t2/) — complete T2 5-Gate example
- Read [Sections Index](docs/agent_engineering_workflow_sections_v1.0_2026-07-12.en.md) — handbook overview
- Stuck? Check [Stage 90 Pitfalls](docs/90-pitfalls/_index_en.md) — 48 pitfall entries
