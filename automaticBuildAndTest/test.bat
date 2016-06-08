@echo off

:: echo TESTING REMOTE

:: setlocal ENABLEDELAYEDEXPANSION

:: set operation=test
:: set mode=icbc
:: call %icbcLocal%\interface\runRemote.bat 

:: setlocal DISABLEDELAYEDEXPANSION



echo    TESTING LOCAL

call %icbcLocal%\testCases\globalRun.bat



pause
