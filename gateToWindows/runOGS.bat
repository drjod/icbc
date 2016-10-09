@echo off

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: Run OGS by draging and dropping an input file 
:: Using convention over configuration principle, i.e.
:: script exploits folder structure of testing environment 
:: e.g. for branch ogs_kb1 the executable (named ogs.exe) on 'amak' desktop is 
:: for the configuration OGS_FEM in folder
:: F:\testingEnvironment\amak\ogs\ogs_kb1\Build_OGS_FEM\bin\Release\
:: Test examples are in
:: F:\testingEnvironment\amak\ogs\ogs_kb1\examples\files\%type%\%case%\%configuration%
::
:: by JOD 2016

echo.
echo __ icbc 0.2  ____________(-.-)________________________________________________
echo ______________________________________________________________________________
echo.
echo %1

SET EXECUTABLE=ogs.exe
SET LOCALBASE=F:

: SET tempFolder=C:\Windows\Temp  : access denied error, take script folder instead going for runas admin 
SET tempFolder=%~dp0
SET temporaryFile=%tempFolder%%path.txt

::::: get file name and path of file
SET file=%1
FOR /f %%i IN ("%file%") DO (
: ECHO filedrive=%%~di
SET filepath=%%~pi
SET filename=%%~ni
ECHO %%~pi>%temporaryFile%
)


::::: get path of EXECUTABLE 
   
FOR /F "tokens=1,2,3,4,5,6,7,8,9 delims=\" %%G in (%temporaryFile%) DO (
IF NOT [%%G]==[] SET myVar1=%%G
IF NOT [%%H]==[] SET computer=%%H
IF NOT [%%I]==[] SET code=%%I
IF NOT [%%J]==[] SET branch=%%J
IF NOT [%%K]==[] SET myVar5=%%K
IF NOT [%%L]==[] SET myVar6=%%L
IF NOT [%%M]==[] SET type=%%M
IF NOT [%%N]==[] SET case=%%N
IF NOT [%%O]==[] SET configuration=%%O
)
DEL %temporaryFile% /F /Q

::::: run ogs

echo RUNNING %code% %branch%
echo EXAMPLE %type% %case% %configuration%
%LOCALBASE%\%myVar1%\%computer%\%code%\%branch%\Build_%configuration%\bin\Release\%EXECUTABLE% %filepath%%filename% > %filepath%out.txt



