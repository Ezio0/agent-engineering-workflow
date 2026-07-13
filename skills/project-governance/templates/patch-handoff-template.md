# Patch Handoff Template

Copy this template into a Telegram message when handing off a patch to Ezio for review.

---

## Patch Ready for Review

**Task**: <link to Kanban card or short title>
**Patch**: `docs/pending-reviews/YYYY-MM-DD-{name}.patch`

### Diff stat
```
<output of: git diff --stat HEAD>
```

### Files changed
- `<file 1>` — <one-line description>
- `<file 2>` — <one-line description>

### Test result
```
<output of: pytest <relevant paths> -q | tail -5>
```

### Notes / decisions
- <any deviation from the original task and WHY>
- <any silent assumption made>

### Known follow-ups (NOT in this patch)
- <anything you noticed but didn't fix — separate Kanban card recommended>

---

## After Ezio commits
Run:
```bash
hermes kanban complete <task-id> \
  --summary "<short summary>" \
  --metadata '{"files_changed":[...],"lines_added":N,"lines_removed":M}'
```