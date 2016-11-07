from sys import path as syspath
from os import path
syspath.append(path.join(path.dirname(__file__), '..', 'shared'))

outputFile = 'out.txt'
location = 'local'
rootDirectory = '/home/jens/'
computer = 'ibiza'
compiler = 'GNU'


testingDepth = 3
walltime  = 0
queue = 'no_queue'
setCompilerVariables = ''
setMklVariables = ''
setMpiVariables = ''

preplot = "\"C:\\Program Files\\Tecplot\\Tec360 2013R1\\bin\\preplot.exe\"" 
tecplot = "\"C:\\Program Files\\Tecplot\\Tec360 2013R1\\bin\\tec360.exe\"" 
winscp="\"C:\\Program Files (x86)\\WinSCP\\WinSCP.com\""
# visualStudio = "\"C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\Common7\\IDE\devenv.exe"" set in batch file  
localBuild = rootDirectory + "testingEnvironment\\scripts\\icbc\\gateToWindows\\build\\buildAsAGAdmin.bat"
localRun = rootDirectory + "testingEnvironment\\scripts\\icbc\\gateToWindows\\run\\RunAsAGAdmin.bat"








