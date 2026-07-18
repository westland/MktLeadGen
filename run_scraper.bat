@echo off
cd /d %~dp0
call .venv\Scripts\activate.bat
python -m src.marketing_leads_generator.main
pause