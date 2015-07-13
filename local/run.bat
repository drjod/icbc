@echo off

     
:::::::::::::::: CONFIGURATION ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


set icbcLocal=%cd%
set icbcVersion=0.1
call configure.bat
set baseRemote=home/%login%

setlocal EnableDelayedExpansion

if "!versionRoot!" == "" (
set versionRootRemote=
) else (
set versionRootRemote=%versionRoot:\=/%
)

if "!inputRoot!" == "" (
set inputRootRemote=
) else (
set inputRootRemote=%inputRoot:\=/%
)



setlocal DISABLEDELAYEDEXPANSION


echo _________________________()_()_________________________________________________
echo _________________________('.')_________________________________________________
echo _________________________()  icbc %icbcVersion%        ___________________
echo _______________________________________________________________________________
echo.



echo CONFIGURATION - synchronizing icbc 
::   BY UPLOADING shared.sh

echo.
echo #!/bin/sh						> interface\shared.sh
echo cVersions=(					>> interface\shared.sh
for %%v in (%versions%) do (
echo %%v						>> interface\shared.sh
)
echo )							>> interface\shared.sh
echo cCode="%code%"					>> interface\shared.sh
echo workfolder="%workfolder%"				>> interface\shared.sh
echo icbcVersion="%icbcVersion%"			>> interface\shared.sh
echo versionRoot="%versionRootRemote%"			>> interface\shared.sh
echo inputRoot="%inputRootRemote%"			>> interface\shared.sh


%DOS2UNIX% %icbcLocal%\interface\shared.sh
%WINSCP% /script=%icbcLocal%\interface\share_configuration.txt


echo.
echo.
echo _______________________________________________________________________________
echo.
echo.


:::::::::::::::: SELECT VERSION :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


setlocal ENABLEDELAYEDEXPANSION

set n=0
for %%v in (%versions%) do (
   echo !n! : %%v 
   set versions_vec[!n!]=%%v
   set /A n+=1
)
echo.
set /P selectedVersion="SELECT %code% version by number: "


set version=!versions_vec[%selectedVersion%]!


setlocal DISABLEDELAYEDEXPANSION


echo.
echo _________________________________________________________(-.-)_________________
echo.


call operate.bat


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
