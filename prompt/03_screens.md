# 03_screens.md

## Butterfly — Screens & Views Specification

This document defines all user-facing screens in Butterfly and their responsibilities.  
It maps the application flow (`02_app_flow.md`) to concrete screens and UI views.

This is a **structural document**, not a visual design document.

---

## 1. Launch / Loading Screen

### Purpose
- Indicate that Butterfly is starting locally
- Build user trust that everything runs on their machine

### Contents
- Butterfly logo / name
- Status text:
  - “Starting local engine…”
  - “Loading workspace…”
- Optional spinner or progress indicator

### Exit Condition
- Automatically transitions to Workspace Home once backend is ready

---

## 2. Workspace Home Screen

### Purpose
- Act as the main entry point
- Show the current state of the workspace

### Visible Elements
- Workspace name / location
- List of datasets
- List of experiments
- Recent runs
- Primary action: **Create New Experiment**

### User Actions
- Import dataset
- Open existing experiment
- Create new experiment

---

## 3. Dataset Import Screen

### Purpose
- Allow users to add data into the workspace

### Visible Elements
- File upload control (CSV primary)
- Dataset name input
- Validation feedback

### On Successful Import
- Dataset is stored and hashed
- User is redirected to Dataset Overview

---

## 4. Dataset Overview Screen

### Purpose
- Provide transparency into dataset structure and quality

### Visible Elements
- Dataset metadata:
  - Rows
  - Columns
  - File size
- Column list with inferred types
- Missing value summary
- Sample preview table

### User Actions
- Use dataset to create experiment
- Return to Workspace Home

---

## 5. Create Experiment Screen

### Purpose
- Initialize a new experiment

### Visible Elements
- Dataset selector
- Task selection:
  - Auto-detect (default)
  - Manual override
- Experiment name

### User Actions
- Create experiment
- Cancel

### On Create
- User is taken to the Pipeline Canvas screen

---

## 6. Pipeline Canvas Screen (Core Screen)

### Purpose
- Central working area for ML workflow construction

### Layout
- Left sidebar: navigation and context
- Center canvas: pipeline blocks
- Right panel: configuration and details

---

### 6.1 Pipeline Canvas — Left Sidebar

#### Contents
- Dataset info
- Experiment info
- Run history
- Navigation shortcuts

#### User Actions
- Switch between runs
- Open comparison view
- Return to Workspace Home

---

### 6.2 Pipeline Canvas — Main Canvas

#### Contents
- Visual pipeline representation:
  - Dataset block
  - Preprocessing block
  - Feature Engineering block
  - Model Selection block
  - Training block
  - Evaluation block
  - Explainability block

Each block shows:
- Status (idle / running / completed / failed)
- Summary of configuration

---

### 6.3 Pipeline Canvas — Block Detail Panel

#### Purpose
- Configure or override a pipeline stage

#### Views
- **Config View**
  - UI controls (toggles, sliders, dropdowns)
- **Code View**
  - Inline Python code editor
  - Hook selection (before / after / override)

#### User Actions
- Edit parameters
- Write or upload code
- Disable or override block

---

## 7. Run Execution View

### Purpose
- Show real-time execution progress

### Visible Elements
- Highlighted active block
- Execution logs (streaming)
- Progress indicators per block

### Behavior
- Canvas becomes read-only
- User cannot modify pipeline
- Execution state is clearly visible

---

## 8. Run Results Screen

### Purpose
- Present outcomes of a completed run

### Visible Elements
- Run summary
- Metrics table
- Selected / best model
- Warnings or notes
- Quick actions:
  - View explainability
  - Open notebook
  - Download artifacts

---

## 9. Explainability Screen

### Purpose
- Provide insight into model behavior

### Visible Elements
- Feature importance
- SHAP or equivalent plots
- Model-specific explanations

### User Actions
- Switch explanation method
- Export visualizations

---

## 10. Notebook View

### Purpose
- Show an auto-generated, executable notebook representation of the run

### Visible Elements
- Ordered code cells
- Outputs and plots
- Read-only by default

### User Actions
- Download notebook
- Copy code snippets

---

## 11. Run Comparison Screen

### Purpose
- Compare multiple runs within an experiment

### Visible Elements
- Side-by-side metrics
- Configuration differences
- Model differences
- Dataset and pipeline lineage

### Behavior
- Read-only
- No execution from this screen

---

## 12. Error Screen / Error State

### Purpose
- Clearly surface failures without breaking workflow

### Visible Elements
- Failed block highlighted
- Error message and traceback
- Logs

### User Actions
- Fix configuration or code
- Re-run experiment

---

## 13. Settings Screen (Minimal v1)

### Purpose
- Control global behavior

### Visible Elements
- Default seed settings
- Execution limits
- Sandbox settings (high-level)
- Workspace location

---

## 14. Screen Principles

All screens must follow these rules:
- No hidden execution
- Clear system state at all times
- Read-only views for completed runs
- Clear separation between draft and run states

---

This document defines **what screens exist and what they do**, not how they look visually.
