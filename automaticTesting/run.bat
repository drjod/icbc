@echo off

set operationType=%1
set computer=%2
set code=%3
set branch=%4
set configuration=%5

::
::

setlocal ENABLEDELAYEDEXPANSION

: runas /savecred /user:AG-Admin "C:\\Python34\\python.exe F:\\testingEnvironment\\scripts\\icbc\\automaticTesting\\Build.py amak windows ogs ogs_kb1" 
start C:\\Python34\\python.exe F:\\testingEnvironment\\scripts\\icbc\\automaticTesting\\Run.py !operationType! !computer! !code! !branch! !configuration!

setlocal DISABLEDELAYEDEXPANSION

pause