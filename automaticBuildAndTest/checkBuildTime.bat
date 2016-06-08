@echo off

SET filename=%baseLocal%\%code%\%version%\sources\Build_%current_ogs_configuration%\bin\Release\ogs.exe

IF NOT EXIST %filename% echo Build failed

FOR %%f IN (%filename%) DO SET filedatetime=%%~tf
echo       Last successful build: %filedatetime%


: pause
