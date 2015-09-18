@echo off

%DOS2UNIX% %icbcLocal%\interface\operate.sh
plink %login%@%hostName% -pw %pwd% -m %icbcLocal%\interface\operate.sh
