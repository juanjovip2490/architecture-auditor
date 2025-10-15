@echo off
REM Script de instalación para Windows

echo 🏗️ Instalando Architecture Auditor...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en PATH
    pause
    exit /b 1
)

REM Crear directorio de instalación
set INSTALL_DIR=%USERPROFILE%\.architecture-auditor
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar archivos
xcopy /E /I /Y . "%INSTALL_DIR%"

REM Crear scripts batch para ejecutar
echo @echo off > "%INSTALL_DIR%\audit.bat"
echo python "%INSTALL_DIR%\auditor.py" %%* >> "%INSTALL_DIR%\audit.bat"

echo @echo off > "%INSTALL_DIR%\audit-runner.bat"
echo python "%INSTALL_DIR%\audit_runner.py" %%* >> "%INSTALL_DIR%\audit-runner.bat"

REM Agregar al PATH (requiere reiniciar terminal)
setx PATH "%PATH%;%INSTALL_DIR%" >nul

echo ✅ Instalación completada!
echo.
echo Reinicia tu terminal y usa:
echo   audit --project C:\ruta\del\proyecto
echo   audit-runner C:\ruta\del\proyecto
echo.
echo Para desinstalar: rmdir /s "%INSTALL_DIR%"
pause