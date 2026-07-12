# 00 — Product Positioning

> **Status**: Active (Stage 0)
> **Last reviewed**: 2026-07-12
> **Related**: [中文版](_index_zh.md)

This is the **front gate** of every new project. Before writing any code, answer 5 questions. If you can't answer them in one sentence each, **you don't have a project yet** — you have a feature idea.

---

## The 5 Questions

### 1. WHO — Target user

**One specific person, not a demographic.**

- ❌ "Chinese millennials who shop online"
- ✅ "A 28-year-old product manager in Hangzhou who reads 3 books a month and has no time to remember what she's read"

If you can't picture her face, you don't have a user.

### 2. WHY — The problem (their pain, not your solution)

**The pain must exist without your product.**

- ❌ "Users need better book recommendations"
- ✅ "She's forgotten 60% of the books on her shelf — and her memory is the only metadata she has"

If the problem disappears when your product dies, it wasn't the real problem.

### 3. WHY NOW — What's changed

**Why does this matter today and not 3 years ago?**

Examples of valid "why now":
- A technology cost dropped (e.g., LLM inference 100x cheaper)
- A new data source became accessible (e.g., a previously-closed API opened)
- A regulatory shift created a new constraint/opportunity
- A user behavior shifted (e.g., post-COVID reading habits)

If your "why now" is "because I want to build it" — you don't have a project.

### 4. UNDERLYING LOGIC — Why this approach works

**The mechanism, not the conclusion.**

- ❌ "LLM can do reasoning" — that's a **conclusion**, weak
- ✅ "Sparse user behavior (3 clicks vs 30) carries 10x less signal, but LLM inference chains can extract intent from sparse data because the model already encodes domain knowledge from pretraining" — that's a **mechanism**, strong

If you can't explain HOW it works, you can't debug when it doesn't.

### 5. ANTI-POSITIONING — What we are NOT

**This is the most important question. It kills projects faster than anything.**

You must be able to list at least **3 things your project is NOT**.

- ❌ Not Goodreads competitor (too broad, wrong positioning)
- ❌ Not book social network (no social need validated)
- ❌ Not "AI-powered reading assistant" (vague, sold-out category)
- ❌ Not a tool for casual readers (they don't have the pain)

If you can't list 3 things you're NOT, you don't know what you ARE.

---

## How to use this stage

1. **Write a 1-page Positioning Memo** answering these 5 questions.
2. **Keep it to one page.** If it doesn't fit, you don't understand it yet.
3. **Re-read it before Stage 1 (PRD).** The PRD must be consistent with positioning.
4. **Revisit at v1.1, v2.0, etc.** Positioning evolves as you learn.

---

## Deliverables for Stage 0

Two artifacts must exist before moving to Stage 1 (PRD):

| Artifact | File pattern | Purpose |
|----------|--------------|---------|
| **Positioning Memo** | `<project>_positioning_v1.0_<date>.{en,zh}.md` | 1-page filled-in answers to the 5 questions |
| **Positioning Checklist** | `checklist_v1.0_{en,zh}.md` | Sign-off checklist before moving to PRD |

The template for the memo lives at [`template_v1.0_en.md`](template_v1.0_en.md) (English) and [`template_v1.0_zh.md`](template_v1.0_zh.md) (Chinese). Copy it, fill it in, save as your memo.

The sign-off checklist lives at [`checklist_v1.0_en.md`](checklist_v1.0_en.md) and [`checklist_v1.0_zh.md`](checklist_v1.0_zh.md).

---

## Common failure modes

| Symptom | Real cause |
|---------|-----------|
| Positioning memo is 3+ pages | You haven't decided yet — keep cutting |
| "It's for everyone" | You've skipped WHO — pick one specific person |
| "Uses AI" is in positioning | That's a feature, not positioning |
| You can't list 3 anti-positionings | You don't know what you ARE |
| "Why now" is missing | Either the timing isn't real, or you haven't found it yet |

---

## Related sections

- Stage 1 (PRD) depends on this section — see [`../01-prd/_index_en.md`](../01-prd/_index_en.md)
- Positioning is NOT code structure — see [`../10-coding-practices/_index_en.md`](../10-coding-practices/_index_en.md) for what code-level concerns this stage intentionally ignores