# 04_ui_references.md

## Butterfly — UI References & Design Inspiration

This document captures the visual and interaction inspirations for Butterfly.
It defines *what Butterfly should feel like*, not how it is implemented.

The goal is **clarity, calmness, and power without clutter**.

---

## 1. Overall UI Direction

Butterfly follows a **balanced-density** design philosophy.

- Not sparse to the point of hiding power
- Not dense to the point of overwhelming users
- Designed to scale from beginner usage to expert workflows

The interface should feel:
- Calm
- Intentional
- Structured
- Trustworthy

---

## 2. Primary Inspirations

### 2.1 Figma — Visual Clarity & State Awareness

Butterfly borrows from Figma:
- Clear separation of panels
- Strong visual hierarchy
- Subtle but meaningful use of color
- Explicit states (selected, active, disabled, running)

Key takeaways:
- The user should always know *where they are*
- Actions should feel deliberate, not accidental
- Active elements should be visually obvious

---

### 2.2 Notion — Structured Blocks & Calm Interaction

Butterfly borrows from Notion:
- Block-based mental model
- Clean typography
- Low visual noise
- Content-first layout

Key takeaways:
- Everything is a block with a purpose
- Blocks are easy to understand at a glance
- Complexity is revealed progressively, not upfront

---

### 2.3 JupyterLab — Execution & Technical Power

Butterfly borrows from JupyterLab:
- Execution-oriented workflows
- Clear relationship between code and output
- Notebook-style vertical flow where appropriate

Key takeaways:
- Users should feel confident running computations
- Execution results must be clearly tied to inputs
- Outputs should feel inspectable and trustworthy

---

## 3. What Butterfly Explicitly Avoids

Butterfly should **not** resemble:
- Traditional dashboards with excessive charts
- IDEs with overwhelming panels and toolbars
- AutoML tools that hide logic behind single buttons

Avoid:
- Visual clutter
- Overuse of icons
- Excessive animations
- Bright or decorative color palettes

---

## 4. Visual Metaphor Priority

The dominant metaphor in Butterfly is **pipeline-first**.

- The ML pipeline is the primary visual structure
- Blocks represent meaningful stages in computation
- Flow direction communicates execution order

The pipeline is:
- Always visible
- Always understandable
- Always editable (in draft state)

---

## 5. Code Visibility Philosophy

Code in Butterfly is:
- Present
- Accessible
- Not forced

By default:
- Code is collapsed but visible
- UI controls are primary
- Code expands on intent, not by accident

This ensures:
- Beginners are not intimidated
- Advanced users feel respected

---

## 6. Color Usage Philosophy

Butterfly uses color **semantically**, not decoratively.

Color communicates:
- State (idle, running, completed, failed)
- Warnings and errors
- Selection and focus

Default palette:
- Neutral grayscale base
- Muted accent colors
- Strong contrast only where necessary

---

## 7. Summary

Butterfly’s UI should feel like:
- Figma’s clarity
- Notion’s calm structure
- JupyterLab’s computational seriousness

The UI must never distract from:
- Understanding
- Control
- Trust

This document defines **inspiration**, not enforcement.
