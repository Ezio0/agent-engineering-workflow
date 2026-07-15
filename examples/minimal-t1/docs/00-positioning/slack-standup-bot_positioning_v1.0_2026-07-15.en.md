# Positioning Memo — Slack Standup Bot

> **Status**: Signed
> **Version**: v1.0
> **Date**: 2026-07-15
> **Chinese**: `slack-standup-bot_positioning_v1.0_2026-07-15.zh.md`

---

## WHO

**Yang Lei** (Backend Tech Lead, managing 6-person team). Daily standup at 10am, people don't all show up, he chases each on Slack with "what did you do yesterday, what today", 3-4 times per day.

Not "all tech leads" — this specific person. He said verbatim: "I don't want to feel like a debt collector every day."

## WHY

Yang Lei spends 20 min/day chasing progress, team of 6 × 20 min = 10 hours/week of pure chasing, and it interrupts people who are coding.

Pain exists independent of this bot: **async status sync in remote teams is expensive** — a problem predating Slack itself; this bot is just one solution.

## WHY NOW

**Internal accumulation trigger**: Team grew from 3 to 6 last quarter; manual chasing went from "occasional" to "daily grind". Yang Lei explicitly raised it in last week's 1:1: "Can we automate this?"

Not an external change (Slack has been there); an internal scale threshold.

## UNDERLYING LOGIC

**Mechanism**: Change "chasing" from push (human asks) to pull (bot asks on schedule). Each person fills 30 seconds/day, cheaper than being interrupted 3 times.

**Why this works**: Fill-in cost < interruption cost → people will fill proactively.

**Why not "another meeting"**: Remote timezones don't align, meetings are what people escape from.

## ANTI-POSITIONING

This bot is **NOT**:

1. **AI-generated weekly report tool** — no summarizing, no beautifying, no external-facing report content.
2. **Project management system** — no task assignment, priority, or dependency.
3. **Performance review tool** — no scoring, ranking, or "who's slacking" for management.
4. **General chatops platform** — does one thing (nag standup sync), no slash-command marketplace.

If Yang Lei asks "can we add feature X", first check if it slides into any of the above; if yes, decline.

---

## Self-Check (3 questions, mandatory)

**Q1: Can you pitch it in 30 seconds at a dinner?**

"A Slack bot for my tech lead friend — auto-asks his 6-person team 'yesterday/today' every morning, so he doesn't have to be the debt collector, saving him 10 hours/week."

**Q2: Cheapest validation done?**

Yes: last Wednesday Yang Lei manually @'d 6 people in a Slack group for 2 days. Result: 5/6 filled willingly, 1/6 needed a 2nd nudge. **Validated pass**: not the "nobody replies" scenario.

**Q3: What would have to be true in the world for this to FAIL even if done well?**

- Team shrinks back to <3 → manual is enough
- Company bans third-party Slack apps → can't deploy (internal compliance risk, needs CTO approval)
- People start treating bot as "punch card", fill with junk → data worthless (soft failure)

First is uncontrollable, second confirmed compliant, third mitigated by "data only visible to Yang Lei, not for performance review".

---

**Sign-off: Ezio 2026-07-15**
