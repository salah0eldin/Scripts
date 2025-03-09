@echo off

set show_waveform_flag=
set force_flag=
set html_flag=
set seed_flag=-sv_seed random


rem Capture the first argument which is the name
set input=%1
if "%input%"=="" (
    echo Error: Name is required.
    exit /b 1
)
if "%input:~0,1%"=="-" (
    echo Error: Name cannot start with "-".
    exit /b 1
)
shift

:parse_args
if "%~1"=="" goto run_script
if "%~1"=="-w" (
    set show_waveform_flag=--show_waveform
) else if "%~1"=="-f" (
    set force_flag=--force
) else if "%~1"=="-html" (
    set html_flag=--html
) else if "%~1"=="-seed" (
    shift
    if "%~1"=="" (
        echo Error: -seed option requires a value.
        exit /b 1
    )
    set seed_flag=-sv_seed %~1
) else (
    echo Error: Unrecognized flag "%~1".
    echo Usage: CompileSimulate [name] [options]
    echo Name:
    echo Options:
    echo   -w           Show waveform
    echo   -f           Force execution
    echo   -html        Generate HTML coverage
    echo   -seed [val]  Set seed with static number (default: random)
    exit /b 1
)
shift
goto parse_args

:run_script
python "C:\\scripts\\CompileSimulate.py" %input% %show_waveform_flag% %force_flag% %html_flag% %seed_flag%