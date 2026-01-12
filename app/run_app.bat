@echo off
echo ========================================
echo Domain-Aware Prompt Optimizer App
echo ========================================
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>NUL
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo Starting the app...
echo.
streamlit run domain_prompt_optimizer.py --server.port 8501

pause
