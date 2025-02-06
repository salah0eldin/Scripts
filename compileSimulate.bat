@echo off
set SHOW_WAVEFORM=0

if "%2"=="" (
    python "%~dp0compileSimulate.py" %1
) else (
    if "%2"=="-w" (
        set SHOW_WAVEFORM=1
    )
    python "%~dp0compileSimulate.py" %1 --show_waveform
)
