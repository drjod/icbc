@echo off

::::::::::::::::::::::::::::::
::
:: required: version must be selected previously by setting variable 
:: version (set version=...)
::
::

::::: CONFIGURATION

set icbcVersion=0.1
set baseLocal=F:

call "%baseLocal%\tools\icbc\configure.bat"
set local=%baseLocal%%versionRoot%\%code%\%version%
set remote=/%baseRemote%%versionRootRemote%/%code%/%version%
set VISUALSTUDIO=C:\"Program Files (x86)\Microsoft Visual Studio 12.0"\Common7\IDE\devenv.exe

echo _________________________()_()_________________________________________________
echo _________________________('.')_________________________________________________
echo _________________________()  icbc %icbcVersion%        ___________________
echo _______________________________________________________________________________
echo.
echo DEALING WITH %code% %version%

echo Now it is %date% %time%

::::: COMPILE AND TEST

echo START COMPILATION
call %icbcLocal%\automaticBuildAndTest\compile.bat

echo START TESTING
call %icbcLocal%\automaticBuildAndTest\test.bat 

: pause
