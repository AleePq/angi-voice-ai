@echo off
title Iniciando J.A.R.V.I.S.
cls
echo ========================================================
echo        SISTEMA DE ACTIVACION J.A.R.V.I.S.
echo ========================================================
echo.

:: Intentar detectar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR CRITICO] No se detecto Python instalado.
    echo.
    echo Para que Jarvis funcione, NECESITAS instalar Python.
    echo.
    echo 1. Ve a: https://www.python.org/downloads/
    echo 2. Descarga la ultima version.
    echo 3. IMPORTANTE: Al instalar, marca la casilla "Add Python to PATH".
    echo.
    echo Una vez instalado, cierra esta ventana y vuelve a intentarlo.
    echo.
    pause
    exit
)

echo [OK] Python detectado. Verificando librerias...
echo.

:: Instalar requerimientos si faltan
pip install -r requirements.txt >nul 2>&1

echo [OK] Sistemas listos.
echo.
echo Iniciando servidor e interfaz...
python app.py
pause
