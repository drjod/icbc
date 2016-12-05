@echo off


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
::  Task: 
::      Call buildAsAGAdmin.bat (same directory) 
::      to build code in certain branch for all configurations on local windows computer
::      builds (compiles) only if changes in source / header files
::
::      computer, code, branch, configurations are preset:   

set computer=amak
set code=ogs
set branch=ogs_kb1

set configurations=OGS_FEM OGS_FEM_SP


:: location of visual studio devenve.exe is set in build\executeVisualStudio 

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


setlocal ENABLEDELAYEDEXPANSION

for %%c in (%configurations%) do ( 
set configuration=%%c
call %~dp0\build\buildAsAGAdmin.bat !computer! !code! !branch! !configuration!
)
setlocal DISABLEDELAYEDEXPANSION

: pause


