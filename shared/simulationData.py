import configurationShared
import fileinput, imp, copy
import utilities
import numerics

import shutil, sys, os, subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'temp'))
import numerics_global, numerics_flow, numerics_heat, numerics_mass, prc


#################################################################
#  class: ReadFileFlags
#  Task:
#      control data file reloads dependend on selected operation
#      numerics and parallelization data Files are reloaded if flags are set True
#

class ReadFileFlags:

    _numerics = False
    _processing = False

    def __init__( self, operationType, operation ):
    
         if operationType == 's': # simulation
            if operation == 'n':  # write num
                self._numerics = True
            if operation == 'n' or operation == 'p' or operation == 'm': # write num, write pbs, mesh partition 
                self._processing = True

#################################################################
#  class: SimulationData
#  Task:
#      contains the numerics data from mySQL database
#      interface to write *.num and *.pbs files
#

class SimulationData:

    # numerics data that depend on process
    __preconditioner = [] # 0 no preconditioner, 1 Jacobi, 100 ILU - each process one list item
    __theta = []  # 1 implicit, 0, explicit - each process one list item
    __solver = None  # support only for one solver bcgs , gmres, ...

    __numerics = None # numerics data than are independent of process
    __processing = None 

    def __init__( self, operationType, operation):

        self.__readFileFlags = ReadFileFlags( operationType, operation)
        #self.__preconditioner.clear()
        #self.__theta.clear()

    def __del__(self):  

        del self.__preconditioner[:]
        del self.__theta[:]

    #################################################################
    #  SimulationData:setReadFile flag
    #  Task:
    #      set flags to upload and reload data files
    #
        
    def setReadFileFlags( self, operationType, operation ):

        if operationType == 's': # simulation
            if operation == 'n':  # write num
                self.__readFileFlags._numerics = True
            if operation == 'n' or operation == 'p' or operation == 'm': # write num, write pbs, mesh partition 
                self.__readFileFlags._processing = True

    # getter
    def getReadFileFlags( self ):
        return self.__readFileFlags

    #################################################################
    #  SimulationData:reloadDataFiles
    #  Task:
    #      reload files with mySQL data on remote computer
    #

    def reloadDataFiles( self ):

        try:
            if self.__readFileFlags._numerics == True:
                self.reloadFile('configurationShared', False)
                self.reloadFile('numerics_global', True)
                self.reloadFile('numerics_flow', True)
                if numerics_global.massFlag == '1':
                    self.reloadFile('numerics_mass', True)
                if numerics_global.heatFlag == '1':
                    self.reloadFile('numerics_heat', True)
            if self.__readFileFlags._processing == True:    
                self.reloadFile('prc', True)
        except:
            utilities.message( type='ERROR', text='Failed to import data from file' )

    #################################################################
    #  SimulationData:reloadFile
    #  Task:
    #      reload single file with mySQL data on remote computer
    #      called by reloadDataFiles

    def reloadFile( self, fileName, removeFlag = False ):
        utilities.message( type='INFO', text='Reloading ' + fileName )
        if platform.system() == 'Windows':  # ????? ERROR with linux, no update without it in windows
            os.remove(getattr(sys.modules[fileName], '__cached__', fileName + '.pyc')) # forget old data
        imp.reload(sys.modules[fileName])
        if removeFlag == True:
            #os.remove('\\testingEnvironment\\scripts\\icbc\\temp\\' + fileName + '.py')
            try:
                fileStream = open( '\\testingEnvironment\\scripts\\icbc\\temp\\' + fileName + '.py', 'w' )
            except OSError as err:
                utilities.message( type='ERROR', text='OS error: {0}'.format(err) )
            else:           
                fileStream.write( '\n' )          
                fileStream.close()

        

    #################################################################
    #  SimulationData:setProcessing
    #  Task:
    #      store the parallelization data from mySQL

           
    def setProcessing( self, processing ):
 
        self.__processing = processing

         
    #################################################################
    #  SimulationData:setNum
    #  Task:
    #      store the numerics data from mySQL

           
    def setNum( self, numerics, solver, preconditioner, theta ):
 
        self.__numerics = numerics
        self.__solver = solver
        self.__preconditioner = preconditioner 
        self.__theta = theta 

    #################################################################
    #  SimulationData:writeParallelizationData
    #  Task:
    #      calls member function writeDataFile to 
    #      write parallelization data into a file
    #      which can be transfered to remote computer
    #

    def writeProcessingData( self ):   

        self.writeDataFile( 'prc.py', 0, 0 )

    #################################################################
    #  SimulationData:writeNumData
    #  Task:
    #      calls member function writeDataFile to 
    #      write files with numerics data (flow, mass, heat separately)
    #      which can be transfered to remote computer
    #
      
    def writeNumData( self ):    
                   
        self.writeDataFile( 'numerics_global.py', 0, 0 )

        i = 0
        for process in self.__numerics._processes: # loop over flow, mass, heat
            self.writeDataFile( 'numerics_' + process +  '.py', self.__preconditioner[i], self.__theta[i] )
            i = i + 1                    

    #################################################################
    #  SimulationData:writeNum
    #  Task:
    #      Reads global numerics and parallelization data from files and writes *.num file for simulation
    #
    
    def writeNum( self, directory ):
        
        try:
            fileStream = open( directory + configurationShared.examplesName + '.num', 'w' )
        except OSError as err:
            utilities.message( type='ERROR', text='OS error: {0}'.format(err) )
        else:
            if numerics_global.coupledFlag == '1':
                fileStream.write( '\n$OVERALL_COUPLING\n' )
                fileStream.write( ' ' + str( numerics_global.coupling_iterations_min ) + ' ' + str( numerics_global.coupling_iterations_max ) + '\n' )

            self.writeProcessIntoNumFile( fileStream, 'flow' )
            if numerics_global.massFlag == '1':
                self.writeProcessIntoNumFile( fileStream, 'mass' )           
            if numerics_global.heatFlag == '1':
                self.writeProcessIntoNumFile( fileStream, 'heat' )              
            fileStream.write( '\n#STOP\n' )          
            fileStream.close()

    #################################################################
    #  SimulationData:writeProcessIntoNumFile
    #  Task:
    #      called by writeNum for each process
    #      Reads numerics data file and writes num data for a selected process into file
    #

    def writeProcessIntoNumFile( self, fileStream, process ):

        fileStream.write( '\n#NUMERICS\n' )
        #  PCS
        fileStream.write( ' $PCS_TYPE\n' )
        if process == 'flow':
            fileStream.write( '  ' + numerics_global.flowProcess  + '\n' )
        elif process == 'mass':
            fileStream.write( '  MASS_TRANSPORT\n' )
        elif process == 'heat':
            fileStream.write( '  HEAT_TRANSPORT\n' )
        # LUMPING
        if numerics_global.lumpingFlag == '1' and process == 'flow':   # only flow gets lumped
            fileStream.write( ' $ELE_MASS_LUMPING\n' )
            fileStream.write( '  1\n' )
        # LINEAR SOLVER
        fileStream.write( ' $LINEAR_SOLVER\n' )
        if prc.mode == 'mpi_nodes':
            fileStream.write( '; method precond error_tolerance max_iterations theta\n' )  
            fileStream.write( '  petsc ' + numerics_global.solver + ' asm ' + str( sys.modules['numerics_' + process].tollerance_linear ) + ' ' + str( sys.modules['numerics_' + process].maxIterations_linear ) + ' 1. \n' )                
        elif prc.mode == 'omp':  # matrix storage is 4
            fileStream.write( '; method norm error_tolerance max_iterations theta precond storage\n' )
            fileStream.write( '  805 ' + str( sys.modules['numerics_' + process].norm ) + ' ' + str( sys.modules['numerics_' + process].tollerance_linear ) + ' ' + str( sys.modules['numerics_' + process].maxIterations_linear ) + ' ' + str( sys.modules['numerics_' + process].theta ) + '  ' + str( sys.modules['numerics_' + process].precond ) + ' 4\n' )
        elif prc.mode == 'sequential' or prc.mode == 'mpi_elements':
             fileStream.write( '; method norm error_tolerance max_iterations theta precond storage\n' )
             fileStream.write( '  ' + str( configurationShared.solver2number[numerics_global.solver] ) + ' ' + str( sys.modules['numerics_' + process].norm ) + ' ' + str( sys.modules['numerics_' + process].tollerance_linear ) + ' ' + str( sys.modules['numerics_' + process].maxIterations_linear ) + ' ' + str( sys.modules['numerics_' + process].theta ) + '  ' + str (sys.modules['numerics_' + process].precond) + ' ' + str( configurationShared.matrixStorage2number[sys.modules['numerics_' + process].matrixStorage] ) + '\n' )
        else:
             utilities.message( type='ERROR', text='Mode ' + prc.mode + ' not supported' )
        # NONLINEAR SOLVER
        if numerics_global.nonlinearFlag == '1':
            fileStream.write( ' $NON_LINEAR_ITERATIONS\n' )
            fileStream.write( ';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n' )
            fileStream.write( '  PICARD LMAX ' + str( sys.modules['numerics_' + process].maxIterations_nonlinear ) + ' 0.0 ' + str( sys.modules['numerics_' + process].tollerance_nonlinear ) + '\n' )
        # NUMBER OF GAUSS POINTS
        fileStream.write( ' $ELE_GAUSS_POINTS\n' )
        fileStream.write( '  ' + str( sys.modules['numerics_' + process].numberOfGaussPoints ) + '\n' )
        # COUPLING
        if numerics_global.coupledFlag == '1':
            fileStream.write( '$COUPLING_CONTROL\n' )
            fileStream.write( ' LMAX ' + str( sys.modules['numerics_' + process].tollerance_nonlinear ) + '\n' )


    #################################################################
    #  SimulationData:writeData
    #  Task:
    #      called by member function writeData 
    #      to write numerics or parallelization data into a file
    #

      
    def writeDataFile( self, fileName, precond, theta ):

        try:
            fileStream = open( configurationCustomized.rootDirectory + '\\testingEnvironment\\scripts\\icbc\\temp\\' + fileName, 'w' )
        except OSError as err:
            message.console( type='ERROR', text='OS error: {0}'.format(err) )
        else:
            utilities.message( type='INFO', text='Writing ' + configurationCustomized.location + ' ' + fileName )
            if fileName == 'numerics_global.py':
                fileStream.write( 'coupling_iterations_min = \'' + configurationShared.coupling_iterations_min + '\' \n' )
                fileStream.write( 'coupling_iterations_max = \'' + configurationShared.coupling_iterations_max + '\' \n' )
                fileStream.write( 'flowProcess = \'' + self.__numerics._prcs._flow  + '\' \n' )
                fileStream.write( 'massFlag = \'' + self.__numerics._prcs._massFlag + '\' \n' )
                fileStream.write( 'heatFlag = \'' + self.__numerics._prcs._heatFlag + '\' \n\n' )
                fileStream.write( 'coupledFlag = \'' + self.__numerics._coupledFlag + '\' \n' )
                fileStream.write( 'lumpingFlag = \'' + self.__numerics._lumpingFlag + '\' \n' )
                fileStream.write( 'nonlinearFlag = \'' + self.__numerics._nonlinearFlag + '\' \n' )
                fileStream.write( 'solver = \'' + self.__solver + '\' \n' )
            elif fileName == 'prc.py':
                fileStream.write( 'numberOfCPUs = \'' + self.__processing._numberOfCPUs + '\' \n' )
                fileStream.write( 'mode = \'' + self.__processing._mode + '\' \n' )
            else:
                fileStream.write( 'maxIterations_linear = \'' + configurationShared.maxIterations_linear + '\' \n' )
                fileStream.write( 'maxIterations_nonlinear = \'' + configurationShared.maxIterations_nonlinear + '\' \n' )
                fileStream.write( 'norm = \'' + configurationShared.norm + '\' \n' )
                fileStream.write( 'tollerance_linear = \'' + configurationShared.tollerance_linear + '\' \n' )
                fileStream.write( 'tollerance_nonlinear = \'' + configurationShared.tollerance_nonlinear + '\' \n' )
                fileStream.write( 'precond = \''+  str(precond) + '\'\n' )
                fileStream.write( 'matrixStorage = \'sparse\'\n' )
                fileStream.write( 'numberOfGaussPoints = \'' + configurationShared.numberOfGaussPoints + '\'\n' )
                fileStream.write( 'theta = \'' + str(theta) + '\'\n' )

            fileStream.close()

    #################################################################
    #  SimulationData:writePbs
    #  Task:
    #      reloads prc.py to get parallelization data and writes *.pbs file 
    #
    
    def writePbs( self, directory, executable, itemType ):

        # config
        ompthreads = None 
        if prc.mode == 'sequential':            
            ncpus = '1'              
            command = ' '
            place = 'group=host'
        elif prc.mode == 'omp':            
            ncpus = prc.numberOfCPUs
            ompthreads = prc.numberOfCPUs      
            command = ' '
            place = 'group=host'
        elif prc.mode == 'mpi_elements' or prc.mode == 'mpi_nodes':  # parallel
            ncpus = prc.numberOfCPUs
            command = 'mpirun -r rsh -machinefile $PBS_NODEFILE -n ' + ncpus + ' '
            place = 'scatter'
        else: 
           utilities.message( type='ERROR', notSupported='Mode ' + prc.mode )
           return 
        # write
        try:
            fileStream = open( directory + 'run.pbs', 'w' )
        except OSError as err:
            utilities.message( type='ERROR', text='OS error: {0}'.format(err) ) 
        else:
            fileStream.write( '#!/bin/bash\n' )
            fileStream.write( '#PBS -o ' + directory + 'screenout.txt\n' )
            fileStream.write( '#PBS -j oe\n' )  
            fileStream.write( '#PBS -r n\n' )
            fileStream.write( '#PBS -l walltime=' + configurationCustomized.walltime + '\n' )
            fileStream.write( '#PBS -l select=1:ncpus=' + ncpus )
            if ompthreads:
                fileStream.writelines( ':ompthreads=' + prc.numberOfCPUs )
            fileStream.write( ':mem=3gb\n' )
            fileStream.write( '#PBS -l place=' + place + '\n' )
            fileStream.write( '#PBS -q ' + configurationCustomized.queue + '\n' )
            fileStream.write( '#PBS -N ' + itemType +'\n' )
            fileStream.write( '\n' )
            fileStream.write( 'cd $PBS_O_WORKDIR\n' )
            fileStream.write( '\n' )
            fileStream.write( '. /usr/share/Modules/init/bash\n' ) 
            fileStream.write( '\n' )
            fileStream.write( configurationCustomized.setCompilerVariables )
            fileStream.write( configurationCustomized.setMklVariables )
            fileStream.write( configurationCustomized.setMpiVariables )
            fileStream.write( '\n' ) 
            fileStream.write( 'time ' + command + executable + ' ' + directory + configurationShared.examplesName + '\n' )
            fileStream.write( '\n' ) 
            fileStream.write( 'qstat -f $PBS_JOBID\n' )
            fileStream.write( 'exit\n' )                                                                                                 
            fileStream.close()       

    #################################################################
    #  SimulationData:writePbs
    #  Task:
    #      reloads prc.py to get parallelization data and writes *.pbs file 
    #
    
    def partitionMesh( self, directory ):

        partitionScript = configurationCustomized.rootDirectory + utilities.adaptPath( 'testingEnvironment\\scripts\\' ) + 'partition.sh'
               
        os.chdir( directory )
        myMeshfile = directory + configurationShared.examplesName + '.msh'
        if os.path.isfile( myMeshfile ):     
           try:       
               if prc.mode == 'mpi_elements': # for OGS_FEM_MPI, ...
                   subprocess.Popen( partitionScript + ' ' + prc.numberOfCPUs + ' -e -asci ' + directory, shell=True )     
               if prc.mode == 'mpi_nodes':    # for OGS_FEM_PETSC
                   subprocess.Popen( partitionScript + ' ' + prc.numberOfCPUs + ' -n -binary ' + directory, shell=True )                                                                    
           except:
               utilities.message( type='ERROR', text='%s' % sys.exc_info()[0]  )
        else:
            utilities.message( type='ERROR', text='Mesh file missing' )              
