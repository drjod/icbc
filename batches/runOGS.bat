@echo off

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: Run OGS by draging and dropping an input file 
:: script exploits folder structure of testing environment, i.e. 
:: F:\testingEnvironment\%computer%\%code%\%branch%\examples\files\%type%\%case%\%configuration%
:: (convention over configuration)
::
::

echo.
echo __ icbc 0.2  ____________(-.-)________________________________________________
echo ______________________________________________________________________________
echo.

: SET tempFolder=C:\Windows\Temp  : access denied error
SET tempFolder=%~dp0
SET temporaryFile=%tempFolder%%path.txt

::::: get file name and path
SET file=%1
FOR /f %%i IN ("%file%") DO (
: ECHO filedrive=%%~di
SET filepath=%%~pi
SET filename=%%~ni
ECHO %%~pi>%temporaryFile%
)


::::: crumble path
   
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
F:\%myVar1%\%computer%\%code%\%branch%\Build_%configuration%\bin\Release\ogs.exe %filepath%%filename% > %filepath%out.txt



