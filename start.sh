#!/bin/bash

# Butterfly Startup Script
# Starts both backend and frontend in development mode

echo "🦋 Starting Butterfly..."
echo ""

# Check if Python dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "Starting backend and frontend..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start backend in background
python butterfly.py &
BACKEND_PID=$!

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
