@Echo OFF

Set "Pattern=results"

For /R "%baseLocal%\remoteResults\%inputRoot%\%code%\%version%\" %%# in (*.gz) Do (
    Echo %%~nx# | FIND "%Pattern%" 1>NUL && (
        :: Echo Full Path: %%~#
        :: Echo FileName : %%~nx#
        :: Echo Directory: %%~p#
	%sevenZip% e -r -aoa %baseLocal%%%~p#results.gz -o"%baseLocal%%%~p#"
	%sevenZip% x -aoa %baseLocal%%%~p#results -o"%baseLocal%%%~p#"
	del %baseLocal%%%~p#results
	del %baseLocal%%%~p#results.gz
    )
)

