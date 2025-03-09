@echo off

set show_waveform_flag=
set force_flag=
set html_flag=

rem Capture the first argument which is the name
set input=%1
shift

:parse_args
if "%~1"=="" goto run_script
if "%~1"=="-w" set show_waveform_flag=--show_waveform
if "%~1"=="-f" set force_flag=--force
if "%~1"=="-html" set html_flag=--html
if not "%~1"=="-w" if not "%~1"=="-f" if not "%~1"=="-html"(
    echo Error: Unrecognized flag "%~1".
    echo Usage: CompileSimulate [name] [options]
    echo Options:
    echo   -w       Show waveform
    echo   -f       Force execution
    echo   -html    Generate HTML coverage
    exit /b 1
)
shift
goto parse_args

:run_script
python "C:\\scripts\\CompileSimulate.py" %input% %show_waveform_flag% %force_flag% %html_flag%