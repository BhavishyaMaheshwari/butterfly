# 02_app_flow.md

## Butterfly — Application Flow

This document describes how users interact with Butterfly from launch to completed machine learning runs.  
It focuses on **user-visible flow**, not internal implementation.

---

## 1. Application Launch Flow

1. User starts Butterfly (script or packaged app).
2. Butterfly starts a **local backend server**.
3. Backend initializes:
   - Workspace directory
   - Execution engine
   - Experiment storage
4. Butterfly opens a **local web application** in the browser or embedded webview.
5. User lands on the **Workspace Home** screen.

Key principles:
- No login
- No cloud dependency
- No external network required
- Everything runs locally

---

## 2. Workspace Flow

### 2.1 Workspace Home

The Workspace Home shows:
- Existing datasets
- Existing experiments
- Recent runs
- Option to create a new experiment

User actions:
- Create new experiment
- Open existing experiment
- Import dataset

A workspace is persistent and stateful.

---

## 3. Dataset Flow

### 3.1 Dataset Import

User can:
- Upload a CSV file (primary)
- Select an existing dataset in the workspace

On import:
- Dataset is validated
- Basic statistics are computed
- Dataset is hashed for lineage

User sees:
- Row and column count
- Column types
- Missing value summary
- Sample preview

---

## 4. Experiment Creation Flow

### 4.1 Create Experiment

User creates an experiment by:
- Selecting a dataset
- Choosing task type:
  - Auto-detect (default)
  - Manual override (classification, regression, NLP, CV, etc.)

Butterfly creates:
- An editable **Pipeline Canvas**
- A draft experiment state

---

## 5. Pipeline Canvas Flow

### 5.1 Default Pipeline Generation

Butterfly auto-generates a pipeline consisting of blocks:

1. Dataset
2. Preprocessing
3. Feature Engineering
4. Model Selection
5. Training
6. Evaluation
7. Explainability

Each block:
- Has default system logic
- Is editable
- Can be replaced with code

---

### 5.2 Block Interaction

For each block, the user can:
- View configuration (UI controls)
- Switch to code view
- Inject or edit Python logic
- Disable or override the block

Changes immediately update the **draft pipeline**, not past runs.

---

## 6. Running an Experiment

### 6.1 Run Trigger

User initiates execution by clicking **Run Experiment**.

At this point:
- The pipeline state is frozen
- A new immutable **Run** is created
- A seed is fixed for determinism

---

### 6.2 Execution Flow

During execution:
- Blocks execute sequentially
- Progress is shown visually on the pipeline
- Logs and intermediate outputs stream to the UI
- Errors are surfaced with context

The user cannot modify the pipeline during a run.

---

## 7. Run Completion Flow

When execution completes:
- Metrics are displayed
- Best model (or ranked models) are shown
- Explainability outputs are generated
- Artifacts are stored

The run is marked **Completed** or **Failed**.

---

## 8. Results & Inspection Flow

User can:
- Inspect metrics per model
- View feature importance / explanations
- Open the auto-generated notebook
- Download model artifacts

All results are tied to the specific run.

---

## 9. Experiment Iteration Flow

From a completed run, the user can:
- Duplicate the experiment
- Modify the pipeline
- Re-run with changes

Each re-run creates a **new run**, preserving lineage.

---

## 10. Run Comparison Flow

User can select multiple runs to:
- Compare metrics
- Compare configurations
- Inspect differences in pipeline and code
- Identify best-performing runs

Comparison is read-only.

---

## 11. Lineage Flow

Butterfly allows users to:
- Trace a run back to:
  - Dataset version
  - Pipeline configuration
  - User-injected code
- Reproduce any run exactly

Lineage is visual and navigable.

---

## 12. Error Handling Flow

If a run fails:
- The failed block is highlighted
- Error logs are shown
- User can fix configuration or code
- User can re-run after changes

Failures never corrupt past runs.

---

## 13. Application Exit Flow

On exit:
- No data is lost
- All state is persisted locally
- Running executions are safely terminated or warned

---

## 14. Flow Guarantees

Butterfly guarantees:
- No implicit execution
- No hidden state changes
- No mutation of completed runs
- Clear separation between draft and run states

---

This document defines **how users move through Butterfly**, not how the system is implemented internally.
