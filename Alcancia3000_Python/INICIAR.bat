@echo off
cd /d "%~dp0"
python app.py
if errorlevel 1 (
  echo No se pudo iniciar. Comprueba que Python 3 este instalado y agregado al PATH.
  pause
)
