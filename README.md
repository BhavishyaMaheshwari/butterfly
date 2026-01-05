# 🦋 Butterfly

**Local-First, Visual, Hackable Machine Learning Application**

Butterfly is a desktop ML application that runs entirely on your machine. It provides a visual interface for building ML pipelines while allowing complete customization through code injection.

## Features

✅ **Local-First**: Everything runs on your machine. No cloud, no auth, no external dependencies.

✅ **Visual Pipeline**: See your ML workflow as connected blocks, not scattered code.

✅ **Immutable Runs**: Every execution creates a permanent, reproducible run.

✅ **Deterministic**: Same input + same seed = same output, guaranteed.

✅ **Hackable**: Override any part of the system with Python code hooks.

✅ **Full Lineage**: Track every run back to its exact data, code, and configuration.

## Architecture

Butterfly follows a strict separation of concerns:

- **Python Backend**: FastAPI server handling orchestration, storage, and ML execution
- **React Frontend**: Clean, calm UI following Figma/Notion-inspired design principles
- **Domain Model**: Workspace → Experiments → Runs (immutable)
- **Execution Engine**: Enforces hook precedence (override → before → system → after)

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+

### Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install frontend dependencies
cd frontend
npm install
cd ..
```

### Running Butterfly

```bash
# Start the application
python butterfly.py
```

This will:
1. Start the backend server on `http://localhost:8000`
2. Start the frontend dev server on `http://localhost:3000`
3. Open your browser automatically

## Usage

### 1. Import a Dataset

- Click "Choose File" and select a CSV file
- The dataset will be imported, hashed, and validated
- You'll see row count, column count, and schema

### 2. Create an Experiment

- Click "Create Experiment" on a dataset
- Give it a name
- Choose task type (or use auto-detect)
- A pipeline with 10 blocks will be created

### 3. Run the Experiment

- Click "Run Experiment"
- Watch real-time logs as blocks execute
- See the pipeline progress visually
- View metrics when complete

### 4. View Results

- Completed runs show metrics and best model
- All runs are immutable and reproducible
- Compare multiple runs side-by-side

## Pipeline Blocks

Every experiment uses a canonical 10-block pipeline:

1. **Data Ingestion** - Load and validate CSV
2. **Task Resolution** - Auto-detect classification vs regression
3. **Preprocessing** - Handle missing values, encode categoricals, scale features
4. **Feature Engineering** - Feature selection and transformation
5. **Model Selection** - Choose candidate models (sklearn, XGBoost, LightGBM)
6. **Hyperparameter Tuning** - Optimize hyperparameters (Optuna-ready)
7. **Training** - Train all candidate models
8. **Evaluation** - Compute metrics, select best model
9. **Explainability** - Generate feature importance
10. **Output Packaging** - Create artifacts and exports

## Hook System

You can inject custom Python code at any block:

- **Before hooks**: Run before system logic
- **After hooks**: Run after system logic  
- **Override hooks**: Replace system logic entirely

Hook precedence is **strict and deterministic**:
```
override → before → system → after
```

If an override hook exists, system logic is skipped.

## Project Structure

```
butterfly/
├── butterfly.py              # Main entry point
├── requirements.txt          # Python dependencies
├── README.md
│
├── backend/
│   ├── server.py            # FastAPI application
│   ├── domain/              # Domain model entities
│   ├── storage/             # Local filesystem persistence
│   ├── execution/           # Execution engine
│   └── ml/                  # ML block implementations
│
├── frontend/                # React application
│   ├── src/
│   │   ├── App.tsx         # Main application
│   │   ├── api/            # Backend client
│   │   └── store/          # State management
│   └── package.json
│
└── workspaces/              # Local workspace storage
    └── default/
        ├── datasets/
        ├── experiments/
        └── runs/
```

## Core Principles

From the specification documents:

1. **Auto by Default** - Works without ML expertise
2. **Manual When Needed** - Override any automated decision
3. **Hackable Always** - Inject code anywhere
4. **Deterministic & Trustworthy** - Reproducible results
5. **Visual, Not Magical** - Show what's happening and why

## Execution Rules

- ✅ All execution happens via immutable Runs
- ✅ Pipeline is snapshotted before execution
- ✅ Same seed + same input = same output
- ✅ Completed runs cannot be modified
- ✅ User code cannot affect past runs
- ✅ Failures are contained per run

## Technology Stack

**Backend:**
- FastAPI (HTTP + WebSocket)
- pandas, scikit-learn, XGBoost, LightGBM
- Optuna (hyperparameter tuning)
- SHAP (explainability)

**Frontend:**
- React + TypeScript
- Vite (build tool)
- Zustand (state management)
- Monaco Editor (code editing)

## Development

### Backend Development

```bash
# Run backend only
cd backend
python server.py
```

### Frontend Development

```bash
# Run frontend only
cd frontend
npm run dev
```

### Testing

```bash
# Run backend tests
pytest backend/tests/

# Test execution rules
pytest backend/tests/test_execution_rules.py

# Test domain model
pytest backend/tests/test_domain_model.py
```

## Sample Workflow

1. Import `iris.csv` dataset
2. Create experiment "Iris Classification"
3. Run with default settings
4. View results: accuracy, precision, recall
5. Add a `before_preprocessing` hook to customize data cleaning
6. Run again - new immutable run is created
7. Compare the two runs

## Future Enhancements

- Full Optuna hyperparameter tuning
- SHAP visualizations
- Notebook export
- Docker execution mode
- Desktop packaging (Tauri)
- NLP and CV pipelines
- Plugin system



