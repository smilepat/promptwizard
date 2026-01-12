#!/bin/bash

echo "========================================"
echo "Domain-Aware Prompt Optimizer App"
echo "========================================"
echo ""

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

echo "Starting the app..."
echo ""
streamlit run domain_prompt_optimizer.py --server.port 8501
