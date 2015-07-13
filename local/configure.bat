@echo off

set login=sungw389
set pwd=*****
set workfolder=work_j
set hostName=rzcluster.rz.uni-kiel.de

set baseLocal=F:
set baseRemote=home/%login%
set icbcRemote=home/%login%/tools/icbc

set WINSCP=C:\"Program Files (x86)"\WinSCP\WinSCP.com
set DOS2UNIX=F:\tools\dos2unix-6.0.5-win64-nls\bin\dos2unix.exe
set sevenZip=C:\"Program Files"\7-Zip\7z.exe

set code=ogs
set versionRoot=
set inputRoot=\testCases
set versions=trunk ogs_branches_kiel_one kiel_one_2015_3_26 ogs_elisabetta_2015_3_26 ogs_abm_2015_4_7 ogs_2014_11_10_JOD 
