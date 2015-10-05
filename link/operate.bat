@echo off

echo operating on %code% %version%

echo.
echo _______________________________________________________________________________
echo.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::	CONFIGURATION


set local=%baseLocal%%versionRoot%\%code%\%version%
set remote=/%baseRemote%%versionRootRemote%/%code%/%version%


set operationTypes="(c)ompilation" "(s)tore" "s(y)nchronization" "(r)estart" 
			

set synchronizationType=0

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::	SELECT OPERATION TYPE


setlocal ENABLEDELAYEDEXPANSION
set n=0
for %%o in (%operationTypes%) do (
   echo 	%%o 
set operationTypes_vec[!n!]=%%o
   set /a n+=1
)
setlocal DISABLEDELAYEDEXPANSION

		

echo.
choice /m "SELECT operation type" /c csyr 
echo.


if ERRORLEVEL 1 set nOperationType=0
if ERRORLEVEL 2 set nOperationType=1
if ERRORLEVEL 3 set nOperationType=2
if ERRORLEVEL 4 set nOperationType=3


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::	DO OPERATIONS	:::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: type 0: (c)ompilation
::		write interface\operation.sh for (g)et (u)pdate or (t)est
::		plink interface\operation.sh (start interface.sh on remote)
::		
:: type 1: (s)tore
::		write interface\operation.sh for store
::		plink interface\operation.sh (start interface.sh on remote)
::
:: type2: s(y)nchronization
::		winscp interface\(u)pload.txt
::			synchronize remote "%local%\sources\ ..." "%remote%/sources ..."
:: 		winscp interface\(d)ownpload.txt
::			synchronize local "%baseLocal%\results\testCases\%code%\%version%" "/%baseRemote%/testCases/results/%code%/%version%"
::			call unpack.bat
::			preplot
::


if %nOperationType%==0 (

	setlocal ENABLEDELAYEDEXPANSION
	
	echo SELECT !operationTypes_vec[%nOperationType%]! mode
	choice /m "	(g)et (u)pdate or (t)est executable (or (a)bort)" /c guta
	if ERRORLEVEL 1	set operation=get
	if ERRORLEVEL 2	set operation=update
	if ERRORLEVEL 3	set operation=test
	if ERRORLEVEL 4	call operate.bat

	echo cd /%icbcRemote%  > interface\operate.sh
	echo . ./interface.sh %workfolder% %login% %code% %version% !operation! icbc 1 1 >> interface\operate.sh
									:: ALLOW_BUILD_flag - SELECT_MEMBER_flag
	setlocal DISABLEDELAYEDEXPANSION
	
	call interface\runRemote.bat
	
	
) else (
if %nOperationType%==1 (
	echo #!/bin/sh	> interface\operate.sh
	echo cd /%icbcRemote%  >> interface\operate.sh
	echo . ./interface.sh %workfolder% %login% %code% %version% store icbc 1 1 >> interface\operate.sh
 									:: ALLOW_BUILD_flag - SELECT_MEMBER_flag  							::  
	call interface\runRemote.bat

) else (
if %nOperationType%==2 (

	setlocal ENABLEDELAYEDEXPANSION	
	
	echo SELECT !operationTypes_vec[%nOperationType%]! mode
	choice /m "	(u)pload source or (d)ownload result (or (a)bort)" /c uda

	if ERRORLEVEL 1	set synchronizationType=1
	if ERRORLEVEL 2	set synchronizationType=2
	if ERRORLEVEL 3	call operate.bat
	
	setlocal DISABLEDELAYEDEXPANSION
	
) else (
if %nOperationType%==3 (
	call run.bat

))))




:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::   SYNCHRONIZATION


if %synchronizationType%==1 (

	echo SYNCHRONIZING %local% %remote%

	setlocal ENABLEDELAYEDEXPANSION

	if not exist "%remote%" mkdir %remote%
	if not exist "%remote%/sources" mkdir %remote%/sources	
	
	set synchronization=interface/upload.txt
	%WINSCP% /script=!synchronization!

	setlocal DISABLEDELAYEDEXPANSION
) else (
if %synchronizationType%==2 (

		
	setlocal ENABLEDELAYEDEXPANSION

	if not exist "%baseLocal%\remoteResults%inputRoot%\%code%" mkdir %baseLocal%\remoteResults%inputRoot%\%code%
	if not exist "%baseLocal%\remoteResults%inputRoot%\%code%\%version%" mkdir %baseLocal%\remoteResults%inputRoot%\%code%\%version%
	
	set synchronization=interface/download.txt
	%WINSCP% /script=!synchronization!

	setlocal DISABLEDELAYEDEXPANSION

	call unpack.bat
		
	F: 									
	cd %baseLocal%\remoteResults%inputRoot%\%code%\%version%\output

	for /r %%g in (*.tec) do C:\"Program Files\Tecplot\Tec360 2013R1\bin"\preplot.exe %%g


	cd %icbcLocal%


))


:: LOOP


call operate.bat


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
