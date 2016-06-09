@echo off

set tempFolder=C:\Windows\Temp

set WINSCP=C:\"Program Files (x86)"\WinSCP\WinSCP.com

set remoteComputer=rzcluster
set login=sungw389
set hostName=rzcluster.rz.uni-kiel.de

set winscpScript=%tempFolder%\winscp_keepUpToDate_icbc_rzcluster.txt

call F:\testingEnvironment\scripts\icbc\pwds\%remoteComputer%.bat

echo option batch abort > %winscpScript%
echo option confirm off >> %winscpScript%
echo open sftp://%login%:%pwd%@%hostName%/ >> %winscpScript%
echo keepuptodate F:\testingEnvironment\scripts\icbc\shared /home/%login%/testingEnvironment/scripts/icbc/shared >> %winscpScript%




%WINSCP% /script=%winscpScript%

