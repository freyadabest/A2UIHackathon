@echo off
cd /d "%~dp0..\agent"
uv run uvicorn main:app --port 8123 --reload
