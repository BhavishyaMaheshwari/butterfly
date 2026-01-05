# 07_backend_responsibilities.md

## Butterfly — Backend Responsibilities

This document defines the responsibilities of the Butterfly backend.
It clarifies **what the backend owns**, **what it guarantees**, and **what it explicitly does not do**.

This is a **behavioral contract** between the backend, the frontend UI, and the execution engine.

---

## 1. Backend Role

The Butterfly backend is a **local, headless service** responsible for:
- Orchestrating ML execution
- Managing state and persistence
- Enforcing domain invariants
- Providing APIs to the frontend

The backend is **UI-agnostic** and **framework-agnostic**.

---

## 2. Core Responsibilities

The backend must handle the following domains.

---

## 3. Workspace Management

### Responsibilities
- Create, load, and persist workspaces
- Maintain workspace directory structure
- Manage workspace metadata

### Guarantees
- Workspace state is always recoverable
- No workspace data is mutated implicitly

### Explicit Non-Responsibilities
- User authentication
- Multi-user access control

---

## 4. Dataset Management

### Responsibilities
- Import datasets into the workspace
- Validate dataset integrity
- Infer schema and basic statistics
- Compute content-based hashes

### Guarantees
- Datasets are immutable after import
- Dataset hashes uniquely identify content

### Explicit Non-Responsibilities
- Dataset modification
- External data synchronization

---

## 5. Experiment & Pipeline Management

### Responsibilities
- Create and persist experiments
- Manage draft pipeline state
- Validate pipeline structure
- Snapshot pipelines for execution

### Guarantees
- Draft pipelines are editable
- Snapshotted pipelines are immutable
- Experiments cleanly separate draft and run states

### Explicit Non-Responsibilities
- UI layout decisions
- Visualization logic

---

## 6. Block & Hook Management

### Responsibilities
- Register pipeline blocks
- Attach and manage hooks
- Validate hook structure
- Hash hook code for lineage

### Guarantees
- Hooks are versioned via hashing
- Hooks affect only the current run
- Hook execution order is deterministic

### Explicit Non-Responsibilities
- Authoring or editing hook code
- Providing IDE-like tooling

---

## 7. Execution Orchestration

### Responsibilities
- Create and manage runs
- Freeze execution state
- Execute pipeline stages in order
- Emit execution events
- Handle failures gracefully

### Guarantees
- Deterministic execution
- Clear run state transitions
- No partial mutation of completed runs

### Explicit Non-Responsibilities
- Real-time UI rendering
- Progress visualization logic

---

## 8. Execution Context Management

### Responsibilities
- Initialize execution context per run
- Pass context through pipeline stages
- Enforce controlled access to shared state

### Guarantees
- Context isolation between runs
- No state leakage across executions

---

## 9. Code Execution & Sandboxing

### Responsibilities
- Execute user-provided code
- Enforce sandbox restrictions
- Apply resource limits
- Capture logs and errors

### Guarantees
- User code cannot corrupt system state
- Failures are contained within a run
- Errors are surfaced with context

### Explicit Non-Responsibilities
- Preventing logically incorrect user code
- Fixing user code errors

---

## 10. Model & Framework Handling

### Responsibilities
- Provide adapters for supported ML frameworks
- Enforce a uniform model interface
- Manage training and evaluation calls

### Guarantees
- Framework-agnostic execution
- Consistent metric reporting

### Explicit Non-Responsibilities
- Maintaining parity across frameworks
- Guaranteeing optimal performance

---

## 11. Experiment Tracking & Lineage

### Responsibilities
- Persist run metadata
- Track lineage between datasets, pipelines, hooks, and artifacts
- Support run comparison queries

### Guarantees
- Full reproducibility
- Accurate lineage derivation

### Explicit Non-Responsibilities
- External experiment syncing
- Cloud-based tracking

---

## 12. Artifact Management

### Responsibilities
- Store run artifacts locally
- Organize artifacts by run
- Provide export paths

### Guarantees
- Artifacts are immutable
- Artifacts are tied to a specific run

---

## 13. API Layer

### Responsibilities
- Expose backend capabilities via APIs
- Emit execution events
- Support asynchronous execution

### Guarantees
- Stable API contracts
- Clear error semantics

### Explicit Non-Responsibilities
- Frontend state management
- UI-side validation

---

## 14. Error Handling

### Responsibilities
- Catch and classify execution errors
- Associate errors with specific blocks
- Persist error logs

### Guarantees
- Backend does not crash on run failure
- Errors never corrupt persisted state

---

## 15. Backend Invariants (Non-Negotiable)

- No backend action mutates completed runs
- No implicit execution occurs
- All persisted state is recoverable
- Backend logic is deterministic given the same inputs

---

## 16. Summary

The backend is the **guardian of correctness**.

It:
- Owns execution
- Enforces rules
- Preserves trust

It does not:
- Decide UX
- Hide complexity
- Make assumptions on behalf of users

This document defines the backend’s contract and responsibilities.
