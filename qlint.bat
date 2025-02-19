@echo off
set show_gui_flag=
set reload_flag=

rem Capture the first argument (module name)
set input=%1
shift

:parse_args
if "%~1"=="" goto run_script
if "%~1"=="-gui" set show_gui_flag=-gui
if "%~1"=="-r" set reload_flag=-r
if not "%~1"=="-gui" if not "%~1"=="-r" (
    echo Error: Unrecognized flag "%~1".
    echo Usage: LintHDL [name] [options]
    echo Options:
    echo   -gui    Open GUI after linting
    echo   -r      Reload from vlog command
    exit /b 1
)
shift
goto parse_args

:run_script
python "C:\scripts\Qlint.py" %input% %show_gui_flag% %reload_flag%
exit /b %ERRORLEVEL%