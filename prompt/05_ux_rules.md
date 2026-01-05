# 05_ux_rules.md

## Butterfly — UX Rules & Interaction Principles

This document defines **non-negotiable UX rules** for Butterfly.
These rules exist to preserve clarity, trust, and correctness as the product grows.

---

## 1. No Hidden Execution

- The system must never execute code implicitly
- Every execution must be user-initiated
- Execution state must always be visible

If something is running, the user must know **what**, **why**, and **where**.

---

## 2. Clear State Separation

Butterfly has three explicit states:

- **Draft** — editable
- **Running** — frozen
- **Completed** — immutable

Rules:
- Completed runs are never editable
- Draft changes never affect past runs
- Running state locks the canvas

This prevents accidental corruption and ensures reproducibility.

---

## 3. Progressive Disclosure

Complexity must be revealed **only when needed**.

Rules:
- UI controls are shown first
- Code is collapsed by default
- Advanced options require explicit user action

Never overwhelm beginners to satisfy power users.

---

## 4. Visual Feedback Is Mandatory

Every meaningful action must produce feedback.

Examples:
- Running a block highlights it
- Failed blocks show errors clearly
- Disabled blocks are visually distinct

Silent state changes are not allowed.

---

## 5. Read-Only Means Read-Only

When a run is completed:
- Nothing in that run can be edited
- Views are strictly inspect-only
- Copying is allowed
- Mutating is not

To change anything, the user must create a new run.

---

## 6. Calm Interaction Over Speed

Butterfly prioritizes:
- Deliberate actions
- Clear confirmations
- Predictable behavior

Avoid:
- Surprise modals
- Aggressive shortcuts
- Auto-saving destructive changes

Speed should never come at the cost of trust.

---

## 7. Errors Are First-Class Citizens

Errors must:
- Be localized to the failing block
- Show actionable messages
- Preserve system state

Errors should never:
- Crash the application
- Corrupt workspace data
- Hide stack traces from advanced users

---

## 8. User Always Wins

If the user explicitly chooses something:
- It overrides system recommendations
- It is respected even if suboptimal
- The system may warn, but never block

Butterfly advises — it does not dictate.

---

## 9. Determinism Is Sacred

Rules:
- Same inputs + same seed = same output
- Any non-determinism must be explicit
- Randomness must be visible and configurable

Trust depends on repeatability.

---

## 10. No Dead Ends

At any point, the user must be able to:
- Go back
- Duplicate
- Re-run
- Inspect

The system must never trap the user in a state.

---

## 11. Consistency Over Cleverness

- Same actions behave the same everywhere
- Same icons mean the same thing everywhere
- Same terminology is used throughout

Avoid “smart” UX that breaks expectations.

---

## 12. UX Is Part of the System

UX decisions are not cosmetic.
They directly affect:
- Reproducibility
- Trust
- Correctness

Any UX change must respect the rules in this document.

---

This document defines **how Butterfly must behave**, not how it looks.
