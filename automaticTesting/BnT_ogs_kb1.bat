@echo off

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: BnT_ogs_kb1: Build and Test ogs Kiel Branch One

set PYTHON=C:\\Python34\\python.exe


:::::::::::::::::::::::::

start %PYTHON% %~dp0\BuildAndTest.py amak windows ogs ogs_kb1 
start %PYTHON% %~dp0\BuildAndTest.py rzcluster linux ogs ogs_kb1 

pause





