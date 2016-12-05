@echo off


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
::  Task: 
::      Call executable
::      as administrator (AG-Admin, password must be given once at first execution) 
::  Arguments to pass:

set computer=%1
set code=%2
set branch=%3
set type=%4
set case=%5
set configuration=%6
set flow_process=%7
set element_type=%8
set examplesName=%9


::
::

setlocal ENABLEDELAYEDEXPANSION

:: runas /savecred /user:AG-Admin 
:: runas requires " "
F:\\testingEnvironment\\!computer!\\!code!\\!branch!\\Build_!configuration!\\bin\\Release\\ogs.exe F:\\testingEnvironment\\!computer!\\!code!\\!branch!\\examples\\files\\!type!\\!case!\\!flow_process!\\!element_type!\\!configuration!\\!examplesName! > F:\\testingEnvironment\\!computer!\\!code!\\!branch!\\examples\\files\\!type!\\!case!\\!flow_process!\\!element_type!\\!configuration!\\out.txt

setlocal DISABLEDELAYEDEXPANSION

