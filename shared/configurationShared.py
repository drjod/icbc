
verbosity=1     # 0: no messages , 1: messages

inputFileEndings = ['bc', 'fct', 'gli', 'ic', 'mcp', 'mfp', 'mmp', 'msh', 'msp', 'num', 'out', 'pcs', 'rfd', 'st', 'tim', 'pqc', 'krc']
outputFileEndings = ['tec', 'txt', 'plt', 'vtk', 'asc']
additionalFileEndings = ['exe', 'dat', 'sts']             # to export to or import from repository

solver2number = {'gauss': 1, 'bcgs': 2, 'bicg': 3, 'qmrggStab': 4, 'cg': 5, 'cgnr': 6, 'cgs': 7, 'richardson': 8, 'jor': 9, 'sor': 10, 'amg1r5': 11, 'umf': 12, 'gmres': 13} 
# preconditioner2number = {'none': 0, 'jacobi': 1, 'ilu': 100}
matrixStorage2number = {'full': 1, 'sparse': 2, 'symSparse': 3, 'unsymSparse': 4} 
#  3 : for precond incomplete Cholesky
#  4 : for precond incomplete LDU

examplesName = 'testCase'

testingLevel = '1'


# num input (for all processes):

coupling_iterations_min = '5' 
coupling_iterations_max = '25'

maxIterations_linear = '5000'
maxIterations_nonlinear = '100'
norm = '6'
tollerance_linear = '1.e-14'
tollerance_nonlinear = '10.' 


matrixStorage = 'sparse'
numberOfGaussPoints = '2'

