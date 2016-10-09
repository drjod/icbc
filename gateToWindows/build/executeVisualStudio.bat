@echo off


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
::  Task: 
::      Call visual studio devenv.exe to build release (builds only if changes in source / header files)
::  Arguments to pass:
::    1: computer
::    2: code
::    3: branch
::    4: configuration

echo Building %2 %3 %4 on %1 
C:\"Program Files (x86)\Microsoft Visual Studio 12.0"\Common7\IDE\devenv.exe F:\testingEnvironment\%1\%2\%3\Build_%4\OGS.sln /build Release
