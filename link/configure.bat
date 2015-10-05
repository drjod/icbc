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
set versions=kb1 ogs_kb1 trunk
