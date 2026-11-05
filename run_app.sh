#!/bin/bash
cd "$(dirname "$0")"
echo "Starting YouTube Creator Agent Streamlit App..."
/Users/sdazz/nifty-swing-assistant/venv/bin/streamlit run app.py --server.port 8502 --server.headless false
