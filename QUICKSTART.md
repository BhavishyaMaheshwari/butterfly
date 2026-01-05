# Butterfly v1 - Quick Start Guide

## Installation

```bash
cd /Users/bhavishya/code/butterfly

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Running Butterfly

### Option 1: Automatic (Recommended)

```bash
python butterfly.py
```

This will:
- Start the backend server
- Open your browser automatically
- Note: You'll need to start the frontend separately for full functionality

### Option 2: Development Mode

```bash
# Terminal 1: Backend
python butterfly.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Then open `http://localhost:3000` in your browser.

### Option 3: Using the startup script

```bash
./start.sh
```

## First Steps

1. **Import the sample dataset**
   - Click "Choose File"
   - Select `sample_data/iris.csv`
   - Dataset will be imported automatically

2. **Create an experiment**
   - Click "Create Experiment" on the Iris dataset
   - Name it "My First Experiment"
   - A 10-block pipeline will be created

3. **Run the experiment**
   - Click "Run Experiment"
   - Watch the real-time logs
   - See results when complete

## Architecture Overview

```
Butterfly
├── Backend (Python/FastAPI)
│   ├── Domain Model (Workspace, Dataset, Experiment, Run, etc.)
│   ├── Storage Layer (Local filesystem)
│   ├── Execution Engine (Immutable runs, hook system)
│   └── ML Blocks (10-block pipeline)
│
└── Frontend (React/TypeScript)
    ├── Workspace Home
    ├── Experiment View
    └── Run View
```

## Key Features

✅ **Immutable Runs** - Every execution is permanent and reproducible
✅ **Deterministic** - Same seed + same input = same output
✅ **Hook System** - Inject custom Python code anywhere
✅ **Real-time Logs** - Watch execution progress live
✅ **Local-First** - Everything runs on your machine

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.9+)
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Install dependencies: `cd frontend && npm install`

### Port already in use
- Backend uses port 8000
- Frontend uses port 3000
- Kill existing processes or change ports in code

## Next Steps

- Read [README.md](file:///Users/bhavishya/code/butterfly/README.md) for full documentation
- See [walkthrough.md](file:///Users/bhavishya/.gemini/antigravity/brain/182c93ce-3b3f-49e6-9319-a62b24ffd7a3/walkthrough.md) for implementation details
- Try creating hooks to customize the pipeline
- Import your own CSV datasets

## Support

For issues or questions, refer to the specification documents in `prompt/`.
