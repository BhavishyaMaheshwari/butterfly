# 01_prd.md

## Butterfly — Product Requirements Document (PRD)

---

## 1. Product Overview

### Product Name
Butterfly

### Product Type
Local-first web application (desktop-packaged later)

### Description
Butterfly is a visual, hackable machine learning application that automatically builds ML pipelines while allowing users to override, modify, or replace any part of the system using code.

---

## 2. Target Users

### Primary Users
- ML beginners and learners
- ML engineers
- Researchers
- Hackathon and project builders

### Secondary Users
- Data analysts transitioning to ML
- Power users who want speed without boilerplate

---

## 3. User Problems

Butterfly addresses the following problems:
- AutoML tools are opaque and rigid
- Notebooks scale poorly for experimentation and comparison
- ML workflows lack visibility and reproducibility
- Experiment tracking is often bolted on instead of foundational
- Custom logic requires excessive boilerplate

---

## 4. Product Goals

### Functional Goals
- Enable end-to-end ML workflows with minimal setup
- Automatically select models and tune hyperparameters
- Allow full user override via UI and code
- Support multiple ML domains in one system

### Non-Functional Goals
- Deterministic execution
- Local-only computation
- Clean and minimal UI
- Modular and extensible architecture

---

## 5. Core Features (v1)

### 5.1 Machine Learning Support

Butterfly must support:
- Tabular ML (classification, regression)
- Time-series
- NLP
- Computer Vision

The system must:
- Infer task type automatically
- Respect user-specified task over inference
- Recommend models while allowing manual selection

---

### 5.2 Dataset Handling

- CSV is the primary supported input format
- Medium and large datasets must be supported
- Backend adapts execution strategy automatically
- Datasets are hashed for lineage tracking

---

### 5.3 Pipeline Architecture

Butterfly uses a canonical ML pipeline:

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

Each stage:
- Has a default system implementation
- Can be augmented or replaced by user code

---

### 5.4 Code Injection & Customization

Users must be able to:
- Inject Python code inline
- Upload `.py` files
- Override pipeline stages
- Hook into execution lifecycle events

Supported hook types:
- `before_<stage>`
- `after_<stage>`
- `override_<stage>`

Injected code runs in a restricted but powerful sandbox.

---

### 5.5 User Interface

#### UI Style
Custom hybrid:
- Notebook-like execution
- Dashboard-style controls
- Visual pipeline representation

#### Core UI Elements
- Workspace
- Canvas
- Pipeline blocks
- Parameter panels
- Metrics and comparison views

---

### 5.6 Runs & Experiments

- Every execution produces an immutable run
- Runs are deterministic
- Each run stores:
  - Dataset hash
  - Configuration snapshot
  - User code hash
  - Metrics
  - Artifacts

Users can:
- Compare runs
- View lineage
- Inspect decision logs

---

### 5.7 Outputs

Each run must produce:
- Evaluation metrics
- Trained model artifact
- Explainability outputs
- Downloadable notebook
- Production-ready Docker image (future)

---

### 5.8 Framework Support & Extensibility

Butterfly is framework-agnostic by design.

Out of the box, Butterfly provides system-managed pipelines using:
- scikit-learn and gradient-boosting libraries for tabular machine learning
- PyTorch-based pipelines for NLP and computer vision tasks

The system must:
- Select appropriate frameworks automatically based on task and data type
- Allow users to override framework and model choices explicitly
- Allow users to inject custom models and training logic using any Python ML framework

Butterfly does not restrict users to a fixed ML stack.  
Any framework (e.g., PyTorch, TensorFlow, OpenCV-based pipelines) may be used through user-provided code, as long as it conforms to the pipeline contract.

--- 

## 6. Transparency & Explainability

Butterfly must:
- Explain why models were selected
- Show alternatives considered
- Log all automated decisions
- Allow user overrides at any time

Explainability is a first-class feature.

---

## 7. Reproducibility & Lineage

Butterfly guarantees:
- Deterministic execution
- Full lineage from data to output
- Ability to reproduce any run exactly

---

## 8. Out of Scope (v1)

- Cloud hosting
- Multi-user collaboration
- Production MLOps pipelines
- Automatic cloud deployment

---

## 9. Success Criteria

Butterfly v1 is successful if:
- Beginners can train models without writing code
- Advanced users can replace pipeline logic entirely
- Runs are reproducible and comparable
- The system feels clean, predictable, and powerful

---

## 10. Deferred Topics

- Cloud-based execution
- Plugin marketplace
- Shared pipelines
- Collaboration features
