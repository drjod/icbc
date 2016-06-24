import configurationShared
import fileinput, imp, copy
import utilities
import numerics, processing


import shutil, sys, os, subprocess, platform
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'customized'))
import configurationCustomized

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'temp'))
import numerics_global_OGS_FEM, numerics_flow_OGS_FEM, numerics_mass_OGS_FEM, numerics_heat_OGS_FEM
import numerics_global_OGS_FEM_SP, numerics_flow_OGS_FEM_SP, numerics_mass_OGS_FEM_SP, numerics_heat_OGS_FEM_SP
import numerics_global_OGS_FEM_MKL, numerics_flow_OGS_FEM_MKL, numerics_mass_OGS_FEM_MKL, numerics_heat_OGS_FEM_MKL
import numerics_global_OGS_FEM_MPI, numerics_flow_OGS_FEM_MPI, numerics_mass_OGS_FEM_MPI, numerics_heat_OGS_FEM_MPI
import numerics_global_OGS_FEM_PETSC, numerics_flow_OGS_FEM_PETSC, numerics_mass_OGS_FEM_PETSC, numerics_heat_OGS_FEM_PETSC

import prc_OGS_FEM,  prc_OGS_FEM_SP,  prc_OGS_FEM_MKL,  prc_OGS_FEM_MPI,  prc_OGS_FEM_PETSC

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
    __solver = []

    __numerics = None # all numerics data - numerics.Global
    __processing = None # parallelization

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
    #  SimulationData:importNumDataFiles
    #  Task:
    #      import files with mySQL data on remote computer
    #

    def importNumDataFiles( self, configuration ):

        try:
            if self.__readFileFlags._numerics == True:
                # global numerics
                if configuration == "OGS_FEM":
                    imp.reload(numerics_global_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    imp.reload(numerics_global_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    imp.reload(numerics_global_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    imp.reload(numerics_global_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    imp.reload(numerics_global_OGS_FEM_PETSC)
                else:
                    utilities.message( type='ERROR', text='Failed to import numerics_global' )
                # flow numerics
                if configuration == "OGS_FEM":
                    imp.reload(numerics_flow_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    imp.reload(numerics_flow_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    imp.reload(numerics_flow_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    imp.reload(numerics_flow_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    imp.reload(numerics_flow_OGS_FEM_PETSC)
                else:
                    utilities.message( type='ERROR', text='Failed to import numerics_flow' )
                # mass numerics - imports always
                if configuration == "OGS_FEM":
                    imp.reload(numerics_mass_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    imp.reload(numerics_mass_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    imp.reload(numerics_mass_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    imp.reload(numerics_mass_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    imp.reload(numerics_mass_OGS_FEM_PETSC)
                else:
                    utilities.message( type='ERROR', text='Failed to import numerics_mass' )
                # heat numerics - imports always
                if configuration == "OGS_FEM":
                    imp.reload(numerics_heat_OGS_FEM)
                elif configuration == "OGS_FEM_SP":
                    imp.reload(numerics_heat_OGS_FEM_SP)
                elif configuration == "OGS_FEM_MKL":
                    imp.reload(numerics_heat_OGS_FEM_MKL)
                elif configuration == "OGS_FEM_MPI":
                    imp.reload(numerics_heat_OGS_FEM_MPI)
                elif configuration == "OGS_FEM_PETSC":
                    imp.reload(numerics_heat_OGS_FEM_PETSC)
                else:
                    utilities.message( type='ERROR', text='Failed to import numerics_heat' )
        except:
            utilities.message( type='ERROR', text='Failed to import num data from files' )
          
   #################################################################
    #  SimulationData:importProcessingDataFiles
    #  Task:
    #      import files with mySQL data on remote computer
    #

    def importProcessingDataFiles( self, configuration ):

        try:
            if configuration == "OGS_FEM":
                imp.reload(prc_OGS_FEM)
            elif configuration == "OGS_FEM_SP":
                imp.reload(prc_OGS_FEM_SP)
            elif configuration == "OGS_FEM_MKL":
                imp.reload(prc_OGS_FEM_MKL)
            elif configuration == "OGS_FEM_MPI":
                imp.reload(prc_OGS_FEM_MPI)
            elif configuration == "OGS_FEM_PETSC":
                imp.reload(prc_OGS_FEM_PETSC)
            else:
                utilities.message( type='ERROR', text='Failed to import prc' )
                
        except:
            utilities.message( type='ERROR', text='Failed to import processing data from files' )
        
    #################################################################
    #  SimulationData:getNumDataFromFiles
    #  Task:
    #      Put numerics data from module into SimData 

    def getNumDataFromModules( self, configuration ):

        if configuration == "OGS_FEM":
            self.getNumDataFromModules_OGS_FEM()
        elif configuration == "OGS_FEM_SP":
            self.getNumDataFromModules_OGS_FEM_SP()
        elif configuration == "OGS_FEM_MKL":
            self.getNumDataFromModules_OGS_FEM_MKL()
        elif configuration == "OGS_FEM_MPI":
            self.getNumDataFromModules_OGS_FEM_MPI()
        elif configuration == "OGS_FEM_PETSC":
            self.getNumDataFromModules_OGS_FEM_PETSC()

           
    def getNumDataFromModules_OGS_FEM( self ):
 
        globNum = numerics.Global()
        prcs = numerics.processes() 

        preconditioner = []
        solver = []
        theta = []

        prcs.set(numerics_global_OGS_FEM.flowProcess, numerics_global_OGS_FEM.massFlag, numerics_global_OGS_FEM.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM.coupledFlag, numerics_global_OGS_FEM.lumpingFlag, numerics_global_OGS_FEM.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM.theta)
        solver.append(numerics_flow_OGS_FEM.solver)
        preconditioner.append(numerics_flow_OGS_FEM.precond)
        
        if numerics_global_OGS_FEM.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM.theta)
            solver.append(numerics_mass_OGS_FEM.solver)
            preconditioner.append(numerics_mass_OGS_FEM.precond)

        if numerics_global_OGS_FEM.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM.theta)
            solver.append(numerics_heat_OGS_FEM.solver)
            preconditioner.append(numerics_heat_OGS_FEM.precond)

        self.setNum( globNum, solver, preconditioner, theta ) 

    def getNumDataFromModules_OGS_FEM_SP( self ):
 
        globNum = numerics.Global()
        prcs = numerics.processes() 

        preconditioner = []
        solver = []
        theta = []

        prcs.set(numerics_global_OGS_FEM_SP.flowProcess, numerics_global_OGS_FEM_SP.massFlag, numerics_global_OGS_FEM_SP.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_SP.coupledFlag, numerics_global_OGS_FEM_SP.lumpingFlag, numerics_global_OGS_FEM_SP.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_SP.theta)
        solver.append(numerics_flow_OGS_FEM_SP.solver)
        preconditioner.append(numerics_flow_OGS_FEM_SP.precond)
        
        if numerics_global_OGS_FEM_SP.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_SP.theta)
            solver.append(numerics_mass_OGS_FEM_SP.solver)
            preconditioner.append(numerics_mass_OGS_FEM_SP.precond)

        if numerics_global_OGS_FEM_SP.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_SP.theta)
            solver.append(numerics_heat_OGS_FEM_SP.solver)
            preconditioner.append(numerics_heat_OGS_FEM_SP.precond)

        self.setNum( globNum, solver, preconditioner, theta ) 

    def getNumDataFromModules_OGS_FEM_MKL( self ):
 
        globNum = numerics.Global()
        prcs = numerics.processes() 

        preconditioner = []
        solver = []
        theta = []

        prcs.set(numerics_global_OGS_FEM_MKL.flowProcess, numerics_global_OGS_FEM_MKL.massFlag, numerics_global_OGS_FEM_MKL.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_MKL.coupledFlag, numerics_global_OGS_FEM_MKL.lumpingFlag, numerics_global_OGS_FEM_MKL.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_MKL.theta)
        solver.append(numerics_flow_OGS_FEM_MKL.solver)
        preconditioner.append(numerics_flow_OGS_FEM_MKL.precond)
        
        if numerics_global_OGS_FEM_MKL.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_MKL.theta)
            solver.append(numerics_mass_OGS_FEM_MKL.solver)
            preconditioner.append(numerics_mass_OGS_FEM_MKL.precond)

        if numerics_global_OGS_FEM_MKL.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_MKL.theta)
            solver.append(numerics_heat_OGS_FEM_MKL.solver)
            preconditioner.append(numerics_heat_OGS_FEM_MKL.precond)

        self.setNum( globNum, solver, preconditioner, theta ) 

    def getNumDataFromModules_OGS_FEM_MPI( self ):
 
        globNum = numerics.Global()
        prcs = numerics.processes() 

        preconditioner = []
        solver = []
        theta = []

        prcs.set(numerics_global_OGS_FEM_MPI.flowProcess, numerics_global_OGS_FEM_MPI.massFlag, numerics_global_OGS_FEM_MPI.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_MPI.coupledFlag, numerics_global_OGS_FEM_MPI.lumpingFlag, numerics_global_OGS_FEM_MPI.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_MPI.theta)
        solver.append(numerics_flow_OGS_FEM_MPI.solver)
        preconditioner.append(numerics_flow_OGS_FEM_MPI.precond)
        
        if numerics_global_OGS_FEM_MPI.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_MPI.theta)
            solver.append(numerics_mass_OGS_FEM_MPI.solver)
            preconditioner.append(numerics_mass_OGS_FEM_MPI.precond)

        if numerics_global_OGS_FEM_MPI.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_MPI.theta)
            solver.append(numerics_heat_OGS_FEM_MPI.solver)
            preconditioner.append(numerics_heat_OGS_FEM_MPI.precond)

        self.setNum( globNum, solver, preconditioner, theta ) 

    def getNumDataFromModules_OGS_FEM_PETSC( self ):
 
        globNum = numerics.Global()
        prcs = numerics.processes() 

        preconditioner = []
        solver = []
        theta = []

        prcs.set(numerics_global_OGS_FEM_PETSC.flowProcess, numerics_global_OGS_FEM_PETSC.massFlag, numerics_global_OGS_FEM_PETSC.heatFlag)
        globNum.set(prcs, numerics_global_OGS_FEM_PETSC.coupledFlag, numerics_global_OGS_FEM_PETSC.lumpingFlag, numerics_global_OGS_FEM_PETSC.nonlinearFlag)
        
        theta.append(numerics_flow_OGS_FEM_PETSC.theta)
        solver.append(numerics_flow_OGS_FEM_PETSC.solver)
        preconditioner.append(numerics_flow_OGS_FEM_PETSC.precond)
        
        if numerics_global_OGS_FEM_PETSC.massFlag == '1':
            theta.append(numerics_mass_OGS_FEM_PETSC.theta)
            solver.append(numerics_mass_OGS_FEM_PETSC.solver)
            preconditioner.append(numerics_mass_OGS_FEM_PETSC.precond)

        if numerics_global_OGS_FEM_PETSC.heatFlag == '1':
            theta.append(numerics_heat_OGS_FEM_PETSC.theta)
            solver.append(numerics_heat_OGS_FEM_PETSC.solver)
            preconditioner.append(numerics_heat_OGS_FEM_PETSC.precond)

        self.setNum( globNum, solver, preconditioner, theta ) 


    #################################################################
    #  SimulationData:getProcessingDataFromFiles
    #  Task:
    #       Put processing data (parallel, ...) from module into SimData     

           
    def getProcessingDataFromModule( self, configuration  ):

        if configuration == "OGS_FEM":
            self.getProcessingDataFromModule_OGS_FEM()
        elif configuration == "OGS_FEM_SP":
            self.getProcessingDataFromModule_OGS_FEM_SP()
        elif configuration == "OGS_FEM_MKL":
            self.getProcessingDataFromModule_OGS_FEM_MKL()
        elif configuration == "OGS_FEM_MPI":
            self.getProcessingDataFromModule_OGS_FEM_MPI()
        elif configuration == "OGS_FEM_PETSC":
            self.getProcessingDataFromModule_OGS_FEM_PETSC()


    def getProcessingDataFromModule_OGS_FEM( self ):
 
        proc = processing.Processing()

        proc.set( prc_OGS_FEM.numberOfCPUs, prc_OGS_FEM.mode )

        self.setProcessing( proc )  

    def getProcessingDataFromModule_OGS_FEM_SP( self ):
 
        proc = processing.Processing()

        proc.set( prc_OGS_FEM_SP.numberOfCPUs, prc_OGS_FEM_SP.mode )

        self.setProcessing( proc )  

    def getProcessingDataFromModule_OGS_FEM_MKL( self ):
 
        proc = processing.Processing()

        proc.set( prc_OGS_FEM_MKL.numberOfCPUs, prc_OGS_FEM_MKL.mode )

        self.setProcessing( proc )  

    def getProcessingDataFromModule_OGS_FEM_MPI( self ):
 
        proc = processing.Processing()

        proc.set( prc_OGS_FEM_MPI.numberOfCPUs, prc_OGS_FEM_MPI.mode )

        self.setProcessing( proc )  

    def getProcessingDataFromModule_OGS_FEM_PETSC( self ):
 
        proc = processing.Processing()

        proc.set( prc_OGS_FEM_PETSC.numberOfCPUs, prc_OGS_FEM_PETSC.mode )

        self.setProcessing( proc )  
        
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

    def writeProcessingData( self, configuration ):   

        self.writeDataFile( 'prc_' + configuration + '.py', 0, 0, 0 )

    #################################################################
    #  SimulationData:writeNumData
    #  Task:
    #      calls member function writeDataFile to 
    #      write files with numerics data (flow, mass, heat separately)
    #      which can be transfered to remote computer
    #              item always sim containing type, case configuration
      
    def writeNumData( self, configuration ):    
                   
        self.writeDataFile( 'numerics_global_' + configuration + '.py', 0, 0, 0 )

        i = 0
        for process in self.__numerics._processes: # loop over flow, mass, heat
            self.writeDataFile( 'numerics_' + process + '_' + configuration + '.py', self.__solver[i], self.__preconditioner[i], self.__theta[i] )
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
            if self.__numerics._coupledFlag == '1':
                fileStream.write( '\n$OVERALL_COUPLING\n' )
                fileStream.write( ' ' + configurationShared.coupling_iterations_min + ' ' + configurationShared.coupling_iterations_max + '\n' )

            self.writeProcessIntoNumFile( fileStream, 0 ) # flow
            if self.__numerics._prcs._massFlag == '1':
                self.writeProcessIntoNumFile( fileStream, 1 )           
            if self.__numerics._prcs._heatFlag == '1':
                self.writeProcessIntoNumFile( fileStream, 2 )              
            fileStream.write( '\n#STOP\n' )          
            fileStream.close()
            
    
                                                       
    #################################################################
    #  SimulationData:writeProcessIntoNumFile
    #  Task:
    #      called by writeNum for each process
    #      Reads numerics data file and writes num data for a selected process into file
    #

    def writeProcessIntoNumFile( self, fileStream, processId ):

        fileStream.write( '\n#NUMERICS\n' )
        #  PCS
        fileStream.write( ' $PCS_TYPE\n' )
        if processId == 0:
            fileStream.write( '  ' + self.__numerics._prcs._flow  + '\n' )
        elif processId == 1:
            fileStream.write( '  MASS_TRANSPORT\n' )
        elif processId == 2:
            fileStream.write( '  HEAT_TRANSPORT\n' )
        # LUMPING
        if self.__numerics._lumpingFlag == '1' and processId == 0:   # only flow gets lumped
            fileStream.write( ' $ELE_MASS_LUMPING\n' )
            fileStream.write( '  1\n' )
        # LINEAR SOLVER
        fileStream.write( ' $LINEAR_SOLVER\n' )
        if self.__processing._mode == 'mpi_nodes':
            fileStream.write( '; method precond error_tolerance max_iterations theta\n' )  
            fileStream.write( '  petsc ' + self.__solver[processId] + '  ' + self.__preconditioner[processId] + '  ' + configurationShared.tollerance_linear  + '  ' + configurationShared.maxIterations_linear + ' 1. \n' )                
        elif self.__processing._mode == 'omp':  # matrix storage is 4
            fileStream.write( '; method norm error_tolerance max_iterations theta precond storage\n' )
            fileStream.write( self.__solver[processId] + '  ' + configurationShared.norm  + ' ' + configurationShared.tollerance_linear + '  ' + configurationShared.maxIterations_linear + '  ' + self.__theta[processId]  + '   ' + self.__preconditioner[processId]  + ' 4\n' )
        elif self.__processing._mode == 'sequential' or self.__processing._mode == 'mpi_elements':
             fileStream.write( '; method norm error_tolerance max_iterations theta precond storage\n' )
             fileStream.write( '  ' + self.__solver[processId] + '  ' + configurationShared.norm + '  ' + configurationShared.tollerance_linear + '  ' + configurationShared.maxIterations_linear + '  ' 
                              + self.__theta[processId] + '  ' + self.__preconditioner[processId] + '  ' + '2' + '\n' )
        else:
             utilities.message( type='ERROR', text='Mode ' + self.__processing._mode + ' not supported' )
        # NONLINEAR SOLVER
        if self.__numerics._nonlinearFlag == '1':
            fileStream.write( ' $NON_LINEAR_ITERATIONS\n' )
            fileStream.write( ';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n' )
            fileStream.write( '  PICARD LMAX ' + configurationShared.maxIterations_nonlinear  + ' 0.0 ' + configurationShared.tollerance_nonlinear + '\n' )
        # NUMBER OF GAUSS POINTS
        fileStream.write( ' $ELE_GAUSS_POINTS\n' )
        fileStream.write( '  ' + configurationShared.numberOfGaussPoints + '\n' )
        # COUPLING
        if self.__numerics._coupledFlag == '1':
            fileStream.write( '$COUPLING_CONTROL\n' )
            fileStream.write( ' LMAX ' + configurationShared.tollerance_nonlinear + '\n' )


    #################################################################
    #  SimulationData:writeData
    #  Task:
    #      called by member function writeData 
    #      to write numerics or parallelization data into a file
    #

      
    def writeDataFile( self, fileName, solver, precond, theta ):

        try:
            fileStream = open( configurationCustomized.rootDirectory + '\\testingEnvironment\\scripts\\icbc\\temp\\' + fileName, 'w' )
        except OSError as err:
            message.console( type='ERROR', text='OS error: {0}'.format(err) )
        else:
            utilities.message( type='INFO', text='Writing ' + configurationCustomized.location + ' ' + fileName )
            if fileName.find('numerics_global') > -1:
                #fileStream.write( 'coupling_iterations_min = \'' + configurationShared.coupling_iterations_min + '\' \n' )
                #fileStream.write( 'coupling_iterations_max = \'' + configurationShared.coupling_iterations_max + '\' \n' )
                fileStream.write( 'flowProcess = \'' + self.__numerics._prcs._flow  + '\' \n' )
                fileStream.write( 'massFlag = \'' + self.__numerics._prcs._massFlag + '\' \n' )
                fileStream.write( 'heatFlag = \'' + self.__numerics._prcs._heatFlag + '\' \n\n' )
                fileStream.write( 'coupledFlag = \'' + self.__numerics._coupledFlag + '\' \n' )
                fileStream.write( 'lumpingFlag = \'' + self.__numerics._lumpingFlag + '\' \n' )
                fileStream.write( 'nonlinearFlag = \'' + self.__numerics._nonlinearFlag + '\' \n' )
            elif fileName.find('prc') > -1:
                fileStream.write( 'numberOfCPUs = \'' + self.__processing._numberOfCPUs + '\' \n' )
                fileStream.write( 'mode = \'' + self.__processing._mode + '\' \n' )
            else:
                #fileStream.write( 'maxIterations_linear = \'' + configurationShared.maxIterations_linear + '\' \n' )
                #fileStream.write( 'maxIterations_nonlinear = \'' + configurationShared.maxIterations_nonlinear + '\' \n' )
                #fileStream.write( 'norm = \'' + configurationShared.norm + '\' \n' )
                #fileStream.write( 'tollerance_linear = \'' + configurationShared.tollerance_linear + '\' \n' )
                #fileStream.write( 'tollerance_nonlinear = \'' + configurationShared.tollerance_nonlinear + '\' \n' )
                fileStream.write( 'solver = \'' + str(solver) + '\' \n' )
                fileStream.write( 'precond = \''+  str(precond) + '\'\n' )
                #fileStream.write( 'matrixStorage = \'sparse\'\n' )
                #fileStream.write( 'numberOfGaussPoints = \'' + configurationShared.numberOfGaussPoints + '\'\n' )
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
        if self.__processing._mode == 'sequential':            
            ncpus = '1'              
            command = ' '
            place = 'group=host'
        elif self.__processing._mode == 'omp':            
            ncpus = self.__processing._numberOfCPUs
            ompthreads = self.__processing._numberOfCPUs      
            command = ' '
            place = 'group=host'
        elif self.__processing._mode == 'mpi_elements' or self.__processing._mode == 'mpi_nodes':  # parallel
            ncpus = self.__processing._numberOfCPUs
            command = 'mpirun -r rsh -machinefile $PBS_NODEFILE -n ' + ncpus + ' '
            place = 'scatter'
        else: 
           utilities.message( type='ERROR', notSupported='Mode ' + self.__processing._mode )
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
                fileStream.writelines( ':ompthreads=' + ncpus )
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
               if self.__processing._mode == 'mpi_elements': # for OGS_FEM_MPI, ...
                   subprocess.Popen( partitionScript + ' ' + self.__processing._numberOfCPUs + ' -e -asci ' + directory, shell=True )     
               if self.__processing._mode == 'mpi_nodes':    # for OGS_FEM_PETSC
                   subprocess.Popen( partitionScript + ' ' + self.__processing._numberOfCPUs + ' -n -binary ' + directory, shell=True )                                                                    
           except:
               utilities.message( type='ERROR', text='%s' % sys.exc_info()[0]  )
        else:
            utilities.message( type='ERROR', text='Mesh file missing' )              
