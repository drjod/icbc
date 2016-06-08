@echo off

echo COMPILE LOCAL
	
set ogs_configurations_local=OGS_FEM OGS_FEM_SP

setlocal ENABLEDELAYEDEXPANSION

for %%c in (%ogs_configurations_local%) do (
echo    %%c
: del %baseLocal%\%code%\%version%\sources\Build_%%c\bin\Release\ogs.exe
%VISUALSTUDIO% %baseLocal%\%code%\%version%\sources\Build_%%c\OGS.sln /build release
echo       WARNING - COULD BE BASED ON OLD CODE
set current_ogs_configuration=%%c
call %icbcLocal%\automaticBuildAndTest\checkBuildTime.bat
)

: set BUILD_STATUS=%ERRORLEVEL%
: echo %ERRORLEVEL%
: if %BUILD_STATUS%==0 echo Build success
: if not %BUILD_STATUS%==0  echo Build failed

: %VISUALSTUDIO% %baseLocal%\%code%\%version%\sources\Build_%%c/OGS.sln /build release "%baseLocal%\%code%\%version%\sources\%%c\OGS.sln"
: call %icbcLocal%\automaticBuildAndTest\checkBuildTime.bat
: )


echo _____________________________________________________(o.o)_____________________



:: echo UPLOAD SOURCE CODE - SYNCHRONIZING %local% %remote%
:: %WINSCP% /script=%icbcLocal%\interface\winscp_uploadSourceCode.txt

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::: compile remote
:: setlocal ENABLEDELAYEDEXPANSION

:: set operation=update
:: set mode=icbc
:: call "%icbcLocal%\interface\runRemote.bat"

:: setlocal DISABLEDELAYEDEXPANSION

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


setlocal DISABLEDELAYEDEXPANSION

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::: get and pack executables 

copy %baseLocal%\%code%\%version%\sources\Build_OGS_FEM\bin\Release\ogs.exe  %baseLocal%\%code%\%version%\executables\ogs_win_OGS_FEM.exe
copy %baseLocal%\%code%\%version%\sources\Build_OGS_FEM_SP\bin\Release\ogs.exe  %baseLocal%\%code%\%version%\executables\ogs_win_OGS_FEM_SP.exe


:: echo GET REMOTE EXECUTABLES
:: %WINSCP% /script=%icbcLocal%\interface\winscp_downloadExecutables.txt

:: %sevenZip% a %baseLocal%\%code%\%version%\executables.7z %baseLocal%\%code%\%version%\executables\ogs*


: pause
