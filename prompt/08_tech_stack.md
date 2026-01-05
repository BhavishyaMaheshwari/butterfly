# 08_tech_stack.md

## Butterfly — Technology Stack

This document defines the **official technology stack** for Butterfly.
It specifies **what technologies are used**, **why they are chosen**, and **where flexibility is allowed**.

This is a **decision document**, not a wishlist.

---

## 1. Guiding Principles

All technology choices must satisfy:

- Local-first execution
- Deterministic behavior
- Strong ML ecosystem support
- Clear separation of concerns
- Future desktop packaging compatibility

No technology is chosen purely for convenience or trendiness.

---

## 2. High-Level Architecture

Butterfly is composed of:

- A **local application shell**
- A **local backend service**
- A **headless ML execution engine**
- A **web-based frontend UI**
- A **local storage layer**

The system is intentionally **polyglot**, with clear boundaries.

---

## 3. Backend & Core Services

### 3.1 Backend Languages

Butterfly uses **two backend languages**, each with a clear role.

#### Python — ML Execution Layer
Used for:
- Machine learning logic
- Pipeline execution
- AutoML logic
- User code injection
- Framework adapters (sklearn, PyTorch, etc.)

Rationale:
- Dominant ML ecosystem
- Required for user-injected ML code
- Fast iteration and experimentation

---

#### Go — System & Orchestration Layer
Used for:
- Application bootstrap
- Process management
- Execution orchestration
- Workspace management
- Long-running service stability
- Desktop packaging integration (later)

Rationale:
- Strong concurrency model
- Predictable performance
- Excellent for local system services
- Clean binary distribution

Go **does not execute ML logic directly**.
It orchestrates and supervises Python execution.

---

## 4. Inter-Process Communication

- Go ↔ Python communication via:
  - gRPC or HTTP
  - Explicit contracts

Rationale:
- Strong separation of concerns
- Crash isolation
- Language independence

---

## 5. ML & Data Stack (Python)

### 5.1 Tabular ML (Default AutoML)
- scikit-learn
- XGBoost
- LightGBM
- CatBoost

---

### 5.2 Deep Learning (NLP & CV)
- PyTorch
- torchvision
- Hugging Face Transformers
- OpenCV (for preprocessing)

---

### 5.3 Optional / User-Injected Frameworks
- TensorFlow / Keras
- Custom PyTorch training loops
- Any Python-based ML framework

Butterfly is **framework-agnostic by contract**.

---

### 5.4 Data Handling
- pandas (default)
- polars (large datasets)
- dask (streaming / distributed scenarios)

Backend may adapt automatically based on dataset size.

---

### 5.5 Hyperparameter Optimization
- Optuna

---

### 5.6 Explainability
- SHAP
- Native framework explainability tools

---

## 6. Execution & Isolation

### 6.1 Execution Model (v1)
- Python execution managed by Go
- Runs executed in isolated Python processes

---

### 6.2 Docker Integration

Docker is **supported and optional**.

Docker may be used for:
- Isolated execution environments
- Reproducible runs
- Dependency consistency
- Advanced sandboxing

Modes:
- **Local native execution** (default)
- **Docker-backed execution** (opt-in)

Docker is not mandatory for basic usage.

---

### 6.3 Determinism
- Explicit seed control
- Hash-based versioning
- Deterministic pipeline snapshots

---

## 7. Code Execution & Sandboxing

### Responsibilities
- User code executes inside:
  - Restricted Python runtime
  - Optional Docker container
- Resource limits:
  - CPU
  - Memory
  - Time

Failures are contained per run.

---

## 8. Storage & Persistence

### Medium
- Local filesystem

### Formats
- JSON (metadata)
- Parquet / binary (data artifacts)
- Framework-native formats (models)

No external database is required in v1.

---

## 9. Frontend Stack

### 9.1 UI Framework
- React or Svelte
- TypeScript

---

### 9.2 Code Editing
- Monaco Editor

---

### 9.3 Visualization
- D3.js or equivalent
- Custom pipeline visualization components

---

## 10. Desktop Packaging (Later)

### Packaging Framework
- Tauri (preferred)
- Electron (fallback)

Go is the preferred integration layer for desktop packaging.

---

## 11. Explicit Non-Choices (v1)

Butterfly will NOT require:
- Cloud infrastructure
- External databases
- Kubernetes
- Always-on Docker usage

---

## 12. Technology Boundaries

Allowed:
- Go for orchestration
- Python for ML execution
- Docker for isolation
- Multiple ML frameworks via adapters

Disallowed:
- Mixing UI logic into backend
- Tight coupling between Go and Python internals
- Framework-specific assumptions in domain logic

---

## 13. Summary

Butterfly is:
- **Python-powered for ML**
- **Go-powered for system orchestration**
- **Docker-enabled for isolation**
- **Web-based for interaction**

This stack balances:
- Power
- Safety
- Flexibility
- Long-term scalability

This document defines the **technical foundation** of Butterfly.
