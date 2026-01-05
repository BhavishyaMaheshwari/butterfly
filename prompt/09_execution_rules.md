# 09_execution_rules.md

## Butterfly — Execution Rules & Guarantees

This document defines the **execution semantics** of Butterfly.
It is the **final authority** on how pipelines run, how hooks behave, and how determinism, safety, and isolation are enforced.

If there is ever ambiguity between implementation and documentation, **this document wins**.

---

## 1. Core Execution Principles

Butterfly execution is governed by the following principles:

1. Explicit is better than implicit  
2. Determinism over convenience  
3. Isolation over shared state  
4. User intent overrides system intelligence  
5. Failure must be contained, not catastrophic  

These principles are non-negotiable.

---

## 2. Execution Units

### 2.1 What Can Execute

The smallest executable unit in Butterfly is a **Block**.

- Blocks execute sequentially
- Blocks never execute partially
- A pipeline execution is an ordered execution of blocks

---

### 2.2 What Cannot Execute

The following **never execute independently**:
- Experiments
- Pipelines (without a run)
- Completed runs
- Artifacts

Only a **Run** can trigger execution.

---

## 3. Run Creation Rules

A run is created when the user explicitly initiates execution.

At run creation time:
- The pipeline is snapshotted
- All block configurations are frozen
- All user-injected code is hashed
- A global seed is fixed
- Dataset version is locked

Once created, a run is immutable.

---

## 4. Execution Order Rules

### 4.1 Canonical Block Order

Blocks must execute in the following order unless explicitly overridden:

1. Data Ingestion  
2. Task Resolution  
3. Preprocessing  
4. Feature Engineering  
5. Model Selection  
6. Hyperparameter Tuning  
7. Training  
8. Evaluation  
9. Explainability  
10. Output Packaging  

The backend enforces this order.

---

### 4.2 Override Restrictions

- Users may override block logic
- Users may not violate block ordering
- Skipping a block must be explicit

No implicit reordering is allowed.

---

## 5. Hook Execution Rules

### 5.1 Hook Types

Each block supports three hook types:

- `before_<block>`
- `after_<block>`
- `override_<block>`

---

### 5.2 Hook Precedence

Hook execution precedence is **strict and deterministic**:

1. `override_<block>`  
2. `before_<block>`  
3. System block logic  
4. `after_<block>`

Rules:
- If an override hook exists, system logic is skipped
- Before/after hooks wrap system logic
- Multiple hooks of the same type execute in registration order

---

### 5.3 Hook Scope

- Hooks affect only the current run
- Hooks cannot modify global state
- Hooks cannot affect other runs

---

## 6. Execution Context Rules

### 6.1 Context Lifecycle

- A new execution context is created per run
- Context is passed block-to-block
- Context is destroyed after run completion

No context reuse is allowed.

---

### 6.2 Context Mutation Rules

- Blocks may mutate the execution context
- Mutations must be explicit
- Context must remain internally consistent

Hidden or implicit mutations are forbidden.

---

## 7. Determinism Rules

Butterfly guarantees deterministic execution under the following rules:

- A single global seed is applied per run
- All randomness must derive from this seed
- Any non-deterministic operation must be declared explicitly

Violations:
- Undeclared randomness is considered a bug
- Non-deterministic user code must opt out explicitly

---

## 8. Parallelism & Concurrency

### 8.1 Default Behavior

- Blocks execute sequentially
- No implicit parallel execution

---

### 8.2 Allowed Parallelism

Parallelism is allowed only for:
- Hyperparameter search
- Model training across candidates
- User-declared parallel blocks

Parallel execution must:
- Preserve determinism
- Not mutate shared state unsafely

---

## 9. Failure Handling Rules

### 9.1 Failure Scope

- Failures are scoped to a single run
- A failure in one run cannot affect others
- Backend must remain alive after failure

---

### 9.2 Failure Semantics

On failure:
- Execution stops immediately
- The failed block is marked
- Error logs and traceback are persisted
- Partial artifacts are preserved if safe

Silent failure is forbidden.

---

## 10. Docker Execution Rules

When Docker is enabled:

- Each run executes in an isolated container
- Container image is versioned
- File system access is controlled
- Network access is restricted by default

Docker execution must produce **identical results** to native execution given the same inputs.

---

## 11. User Code Execution Rules

- User code runs with the same execution guarantees as system code
- User code cannot bypass sandbox restrictions
- User code errors are treated as run failures

Butterfly does not attempt to fix user code.

---

## 12. Immutability Rules

The following are strictly immutable once created:

- Completed runs
- Run artifacts
- Dataset versions
- Pipeline snapshots

Any modification requires creating a new run.

---

## 13. Auditability Rules

Butterfly must be able to answer:

- What code ran?
- On what data?
- With what configuration?
- In what order?
- With what outcome?

If the system cannot answer these, it is considered incorrect.

---

## 14. Explicit Prohibitions

Butterfly must never:
- Execute code implicitly
- Mutate past runs
- Hide execution steps
- Mask errors
- Guess user intent when explicitly specified

---

## 15. Summary

Execution in Butterfly is:
- Explicit
- Deterministic
- Isolated
- Auditable
- User-controlled

These rules define **how Butterfly thinks and behaves at runtime**.

Breaking these rules breaks Butterfly.
