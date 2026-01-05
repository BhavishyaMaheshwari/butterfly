# 06_domain_model.md

## Butterfly — Domain Model

This document defines the **core domain concepts** of Butterfly.
It describes the *entities*, their *responsibilities*, and their *relationships*.

This is the **conceptual backbone** of the system.
All backend logic, UI state, and execution flow must map cleanly to this model.

No implementation details are included here.

---

## 1. Core Domain Principles

- All state is explicit
- No hidden global state
- Completed executions are immutable
- Everything traceable must be traceable
- Domain objects represent **real user concepts**, not technical artifacts

---

## 2. Top-Level Domain Objects

Butterfly is built around the following primary entities:

1. Workspace  
2. Dataset  
3. Experiment  
4. Pipeline  
5. Block  
6. Run  
7. Artifact  
8. Model  
9. Hook  
10. Execution Context  

Each is defined below.

---

## 3. Workspace

### Description
A **Workspace** is the top-level container for all user activity.

### Responsibilities
- Owns datasets, experiments, and runs
- Defines storage location
- Persists all state locally

### Key Properties
- Workspace ID
- Name
- Root path
- Creation timestamp

### Relationships
- One Workspace → many Datasets
- One Workspace → many Experiments

---

## 4. Dataset

### Description
A **Dataset** represents a versioned input data source.

### Responsibilities
- Store dataset metadata
- Provide consistent data access
- Enable lineage and reproducibility

### Key Properties
- Dataset ID
- Name
- Source path
- Schema (columns, types)
- Row count
- Hash (content-based)

### Relationships
- One Dataset → many Experiments
- One Dataset → many Runs (via experiments)

Datasets are immutable once imported.

---

## 5. Experiment

### Description
An **Experiment** is a logical setup for running ML workflows on a dataset.

### Responsibilities
- Own a draft pipeline
- Group related runs
- Act as a comparison boundary

### Key Properties
- Experiment ID
- Name
- Associated Dataset
- Task definition (auto or manual)
- Creation timestamp

### Relationships
- One Experiment → one Dataset
- One Experiment → one Pipeline (draft)
- One Experiment → many Runs

Experiments are editable; runs are not.

---

## 6. Pipeline

### Description
A **Pipeline** represents the ordered ML workflow definition.

### Responsibilities
- Define execution order
- Hold block configuration
- Serve as the blueprint for runs

### Key Properties
- Pipeline ID
- Ordered list of Blocks
- Global configuration
- Version hash

### Relationships
- One Pipeline → many Blocks
- One Pipeline → many Runs (snapshotted)

Pipelines are mutable only in draft state.

---

## 7. Block

### Description
A **Block** represents a single stage in the ML pipeline.

### Examples
- Preprocessing
- Feature Engineering
- Model Selection
- Training
- Evaluation
- Explainability

### Responsibilities
- Encapsulate stage logic
- Expose configuration
- Accept user code overrides

### Key Properties
- Block ID
- Block type
- Default system logic reference
- Configuration state
- Attached Hooks

### Relationships
- One Block → many Hooks
- One Block → exactly one position in a Pipeline

Blocks are the smallest executable unit.

---

## 8. Run

### Description
A **Run** is a single immutable execution of a pipeline.

### Responsibilities
- Execute a frozen snapshot of the pipeline
- Produce artifacts
- Store metrics and logs

### Key Properties
- Run ID
- Experiment reference
- Pipeline snapshot
- Dataset hash
- Seed
- Status (running / completed / failed)
- Start & end timestamps

### Relationships
- One Run → one Experiment
- One Run → many Artifacts
- One Run → one Execution Context

Runs are immutable once completed.

---

## 9. Artifact

### Description
An **Artifact** is any output produced by a run.

### Examples
- Trained model file
- Metrics report
- Plots
- Explainability outputs
- Generated notebook

### Responsibilities
- Store execution outputs
- Enable inspection and export

### Key Properties
- Artifact ID
- Type
- File path or reference
- Metadata
- Associated Run ID

Artifacts are read-only.

---

## 10. Model

### Description
A **Model** represents a trained or candidate ML model.

### Responsibilities
- Encapsulate framework-specific logic
- Expose a uniform interface to the system

### Key Properties
- Model ID
- Framework (sklearn, torch, etc.)
- Hyperparameters
- Training metadata

### Relationships
- One Run → one or more Models
- One Model → zero or more Artifacts

Models are always tied to a run.

---

## 11. Hook

### Description
A **Hook** is user-provided code injected into pipeline execution.

### Types
- before_<stage>
- after_<stage>
- override_<stage>

### Responsibilities
- Modify or replace system behavior
- Operate on execution context

### Key Properties
- Hook ID
- Hook type
- Associated Block
- Source (inline or file-based)
- Code hash

Hooks are versioned via hashing.

---

## 12. Execution Context

### Description
The **Execution Context** is the shared state passed through pipeline execution.

### Responsibilities
- Carry data, models, and metadata between stages
- Enforce determinism
- Provide controlled access to state

### Key Properties
- Dataset reference
- Intermediate data
- Feature representations
- Model objects
- Metrics
- Logs

The execution context exists only during a run.

---

## 13. Domain Invariants (Non-Negotiable)

- A completed Run cannot be modified
- A Dataset cannot be mutated after import
- Hooks cannot affect past runs
- Pipeline snapshots are immutable per run
- All lineage must be derivable from domain objects

---

## 14. Domain Model Summary

At a high level:

- Workspaces contain Experiments
- Experiments define Pipelines
- Pipelines contain Blocks
- Runs execute Pipeline snapshots
- Runs produce Artifacts
- Hooks modify execution behavior
- Execution Context carries state

This domain model defines **what Butterfly is**, not how it is built.

---

This document is the **authoritative source** for all system behavior.
Any implementation must map cleanly to these domain concepts.
