@echo off
rem =============
rem by AmazingChz
rem =============

color 2

Title Decompress *.NSO...

IF [%1] EQU [] Goto:Error

Goto:decompress

rem -------------------------

:decompress
cd ./resources/tools/hactool/
hactool -t nso %1 --uncompressed=%1.uncompressed

Exit /b

rem -------------------------

:Error
Color 0C & echo(
ECHO    You must drag and drop a *.NSO file onto this batch program to decompress it.
Timeout /T 6 /NoBreak >nul
Exit /b

rem -------------------------

pause