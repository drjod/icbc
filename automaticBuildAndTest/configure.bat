@echo off

set icbcLocal=F:\tools\icbc
set icbcVersion=0.1

set login=sungw389
set pwd=*****
set workfolder=work_j
set hostName=rzcluster.rz.uni-kiel.de


set baseRemote=home/%login%
set icbcRemote=home/%login%/tools/icbc

set WINSCP=C:\"Program Files (x86)"\WinSCP\WinSCP.com
set DOS2UNIX=F:\tools\dos2unix-6.0.5-win64-nls\bin\dos2unix.exe
set UNIX2DOS=F:\tools\dos2unix-6.0.5-win64-nls\bin\unix2dos.exe
set sevenZip=C:\"Program Files"\7-Zip\7z.exe
set TECPLOT=C:\"Program Files"\Tecplot\"Tec360 2013R1"\bin\tec360.exe
set PREPLOT="C:\Program Files\Tecplot\Tec360 2013R1\bin"\preplot

set code=ogs
set versionRoot=
set inputRoot=\examples
set versions=trunk kb1 kiel_testing 
: kiel_one_2015_3_26 ogs_elisabetta_2015_3_26 ogs_abm_2015_4_7 ogs_2014_11_10_JOD 
set ogsConfigurations_local=OGS_FEM OGS_FEM_SP

:: !!!! inputRoot does not work for remote (synchronization_downloadResults) !!!!!
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


set baseRemote=home/%login%

setlocal ENABLEDELAYEDEXPANSION

if "!versionRoot!" == "" (
set versionRootRemote=
) else (
set versionRootRemote=%versionRoot:\=/%
)



if "!inputRoot!" == "" (
set inputRootRemote=
) else (
set inputRootRemote="/examples"
%inputRoot:\=/%
)


setlocal DISABLEDELAYEDEXPANSION



::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



echo CONFIGURATION - synchronizing icbc 
::   BY GENERATING AND UPLOADING shared.sh

echo.
echo #!/bin/sh						> %icbcLocal%\interface\shared.sh
echo cVersions=(					>> %icbcLocal%\interface\shared.sh
for %%v in (%versions%) do (
echo %%v						>> %icbcLocal%\interface\shared.sh
)
echo )							>> %icbcLocal%\interface\shared.sh
echo cCode="%code%"					>> %icbcLocal%\interface\shared.sh
echo workfolder="%workfolder%"				>> %icbcLocal%\interface\shared.sh
echo icbcVersion="%icbcVersion%"			>> %icbcLocal%\interface\shared.sh
echo versionRoot="%versionRootRemote%"			>> %icbcLocal%\interface\shared.sh
echo inputRoot="%inputRootRemote%"			>> %icbcLocal%\interface\shared.sh


%DOS2UNIX% %icbcLocal%\interface\shared.sh
:: %WINSCP% /script=%icbcLocal%\interface\winscp_share_configuration.txt                                       :: SWITCHED OFF


del %icbcLocal%\interface\shared.sh 

echo.
echo.
echo _______________________________________________________________________________
echo.
echo.

