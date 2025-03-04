@echo off

set show_gui_flag=
set reload_flag=

rem Capture the first argument which is the top module name
set top_module=%1
shift

:parse_args
if "%~1"=="" goto run_script
if "%~1"=="-gui" set show_gui_flag=-gui
if "%~1"=="-r" set reload_flag=-r
if not "%~1"=="-gui" if not "%~1"=="-r" (
    echo Error: Unrecognized flag "%~1".
    echo Usage: qlint [top_module] [options]
    echo Options:
    echo   -gui   Show GUI
    echo   -r     Reload environment
    exit /b 1
)
shift
goto parse_args

:run_script
python "C:\\scripts\\Qlint.py" %top_module% %show_gui_flag% %reload_flag%
exit /b %ERRORLEVEL%