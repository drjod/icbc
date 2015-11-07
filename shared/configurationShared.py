
verbosity=1     # 0: no messages , 1: messages

inputFileEndings = ['bc', 'fct', 'gli', 'ic', 'mcp', 'mfp', 'mmp', 'msh', 'msp', 'num', 'out', 'pcs', 'rfd', 'st', 'tim']
outputFileEndings = ['asc', 'tec', 'txt', 'plt']

solver2number = {'gauss': 1, 'bcgs': 2, 'bicg': 3, 'qmrggStab': 4, 'cg': 5, 'cgnr': 6, 'cgs': 7, 'richardson': 8, 'jor': 9, 'sor': 10, 'amg1r5': 11, 'umf': 12, 'gmres': 13} 
preconditioner2number = {'none': 0, 'jacobi': 1, 'ilu': 100}
matrixStorage2number = {'full': 1, 'sparse': 2, 'symSparse': 3, 'unsymSparse': 4} 
#  3 : for precond incomplete Cholesky
#  4 : for precond incomplete LDU

examplesName = 'testCase'

testingDepth = '3'
