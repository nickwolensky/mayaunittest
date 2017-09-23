@echo off & SETLOCAL ENABLEDELAYEDEXPANSION

set MAYA_PATH="C:\Program Files\Autodesk\Maya2016_SP6_201603180400-990260"
REM set TEST_DIR="C:\00_git\bpt-artists\src\mcRig"
REM set TEST_DIR=C:\00_git\mcRig
set TEST_DIR=C:\00_git\nw_tools
set TEST_STR=""

:loop
echo ===========================================================
echo                RUNNING MAYA UNITTESTS 1.0.0
echo                        Nick Wolensky
echo ===========================================================
echo TEST DIRECTORY: %TEST_DIR:"=%
IF NOT %TEST_STR% == "" echo TEST:           %TEST_STR%
echo -----------------------------------------------------------

REM python "%cd%\runmayatests.py" -dir %TEST_DIR -m_dir %MAYA_PATH% --test %TEST_STR%
py -2 "%cd%\runmayatests.py" -dir %TEST_DIR% --test %TEST_STR%

REM python "%~dp0\runmayatests.py" -dir %TEST_DIR% --test %TEST_STR%

echo Do you wish to run again? Leave empty for all test suites or specify test location (i.e Child Directory.tests.test_file). 
echo Type 'quit' to exit. Type 'y' or 'n' to run the same task again. Leave blank to run all possible tests.
set /p CONTINUE=">"

REM Add a switch to run the test I wanted again or add a new name or quit
IF /I "%CONTINUE%" == "quit" EXIT
IF /I "%CONTINUE%" == "y" goto break
IF /I "%CONTINUE%" == "n" (
    set TEST_STR=""
	goto break
)
IF /I "%CONTINUE%" == "" (
    set TEST_STR=""
) ELSE (
    set TEST_STR=!CONTINUE!
)

:break
set CONTINUE=""
goto loop