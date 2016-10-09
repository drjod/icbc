@echo off


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
::  Task: 
::      Call executeVisualStudio.bat () same directory
::      as administrator (AG-Admin, password must be given once at first execution) 
::  Arguments to pass:

set computer=%1
set code=%2
set branch=%3
set configuration=%4

::
::

setlocal ENABLEDELAYEDEXPANSION

runas /savecred /user:AG-Admin "%~dp0\executeVisualStudio.bat !computer! !code! !branch! !configuration!" 

setlocal DISABLEDELAYEDEXPANSION

