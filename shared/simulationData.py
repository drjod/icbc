import configurationShared
import fileinput
import numerics_flow, numerics_mass, numerics_heat, numerics_coupling, imp

class processes:
    _flow = 'NO_FLOW'
    _massFlag = '0'
    _heatFlag = '0'

class solver:
    _linear = ''
    _precond = ''
    _matrixStorage = ''

class iterations:
    _tollerance_linear = 0.0
    _maxIterations_linear = 0

    _tollerance_nonlinear = 0.0
    _maxIterations_nonlinear = 0
    _norm = ''

class CouplingNumerics:

    def __init__( self ):
        imp.reload( numerics_coupling )

        self.__coupling_iterations_min = coupling_iterations_min
        self.__coupling_iterations_max = coupling_iterations_max 

    def write( self, f ):
        f.write( '\n$OVERALL_COUPLING\n' )
        f.write( ' ' + str( self.__coupling_iterations_min ) + ' ' + str( self.__coupling_iterations_max ) + '\n' )

class ProcessNumerics:
    
    def __init__( self, processType ):
        self.__processType = processType

        self.__solver = solver()
        self.__iterations = iterations()
        self. __numberOfGaussPoints = 0

        if processType == 'flow':
            imp.reload( numerics_flow )
            self.setFlow()
        elif processType == 'mass':
            imp.reload( numerics_mass )
            self.setMass( )
        elif processType == 'heat':
            imp.reload( numerics_heat )
            self.setHeat()
        else:
            message.console( type='ERROR', text='Process type ' + processType + ' not supported' ) 

    def getSolver( self ):
        return __solver

    def getIterations( self ):
        return __iterations

    ###########################
    # relaxation: 0
    # for omp solver 805 and matrixStorage 4

    def write( self, f, simulationData ):
        f.write( '\n#NUMERICS\n' )
        f.write( ' $PCS_TYPE\n' )
        if self.__processType == 'flow':
            f.write( '  ' + simulationData.getFlowProcess() + '\n' )
        elif self.__processType == 'mass':
            f.write( '  MASS_TRANSPORT\n' )
        elif self.__processType == 'heat':
            f.write( '  HEAT_TRANSPORT\n' )
        else:
            message.console( type='ERROR', text='Process type ' + self.__processType + ' not supported' )     
        if self.__processType == 'flow' and simulationData.getLumpingFlag() == '1':
            f.write( ' $ELE_MASS_LUMPING\n' )
            f.write( '  1\n' )
        # solver
        f.write( ' $LINEAR_SOLVER\n' )
        if simulationData.getProcessing() == 'mpi_nodes':
            f.write( '; method precond error_tolerance max_iterations theta\n' )  
            f.write( '  petsc bcgs asm ' + str( self.__iterations._tollerance_linear ) + ' ' + str( self.__iterations._maxIterations_linear ) + ' 1. \n' )                
        elif  simulationData.getProcessing() == 'omp':
            f.write( '; method norm error_tolerance max_iterations theta precond storage\n' )
            f.write( '  805 ' + self.__iterations._norm + ' ' + str( self.__iterations._tollerance_linear ) + ' ' + str( self.__iterations._maxIterations_linear ) + ' 1.0  ' + str( configurationShared.preconditioner2number[self.__solver._precond] ) + '4\n' )
        else:
            f.write( '; method norm error_tolerance max_iterations theta precond storage\n' )
            f.write( '  ' + str( configurationShared.solver2number[self.__solver. _linear] ) + ' ' + self.__iterations._norm + ' ' + str( self.__iterations._tollerance_linear ) + ' ' + str( self.__iterations._maxIterations_linear ) + ' 1.0  ' + str( configurationShared.preconditioner2number[self.__solver._precond] ) + ' ' + str( configurationShared.matrixStorage2number[self.__solver._matrixStorage] ) + '\n' )
        # linearization
        if simulationData.getNonlinearFlag() == '1':
            f.write( ' $NON_LINEAR_ITERATIONS\n' )
            f.write( ';type -- error_method -- max_iterations -- relaxation -- tolerance(s)\n' )
            f.write( '  PICARD LMAX ' + str( self.__iterations._maxIterations_nonlinear ) + ' 0.0 ' + str( self.__iterations._tollerance_nonlinear ) + '\n' )
        f.write( ' $ELE_GAUSS_POINTS\n' )
        f.write( '  ' + str( self.__numberOfGaussPoints ) + '\n' )
        # coupling
        if simulationData.getCoupledFlag() == '1':
            f.write( '\n$COUPLING_CONTROL\n' )
            f.write( ' LMAX ' + str( self.__iterations._tollerance_nonlinear ) + '\n' )
            


    def setFlow( self ):

        self.__iterations._maxIterations_linear = numerics_flow.maxIterations_linear
        self.__iterations._maxIterations_nonlinear = numerics_flow.maxIterations_nonlinear
        self.__iterations._norm = numerics_flow.norm
        self.__iterations._tollerance_linear = numerics_flow.tollerance_linear 
        self.__iterations._tollerance_nonlinear = numerics_flow.tollerance_nonlinear

        self.__solver._linear = numerics_flow.linear
        self.__solver._precond = numerics_flow.precond
        self.__solver._matrixStorage = numerics_flow.matrixStorage

        self.__numberOfGaussPoints = numerics_flow.numberOfGaussPoints

    def setMass( self ):

        self.__iterations._maxIterations_linear = numerics_mass.maxIterations_linear
        self.__iterations._maxIterations_nonlinear = numerics_mass.maxIterations_nonlinear
        self.__iterations._norm = numerics_mass.norm
        self.__iterations._tollerance_linear = numerics_mass.tollerance_linear 
        self.__iterations._tollerance_nonlinear = numerics_mass.tollerance_nonlinear

        self.__solver._linear = numerics_mass.linear
        self.__solver._precond = numerics_mass.precond
        self.__solver._matrixStorage = numerics_mass.matrixStorage

        self.__numberOfGaussPoints = numerics_mass.numberOfGaussPoints
        
    def setHeat( self ):

        self.__iterations._maxIterations_linear = numerics_heat.maxIterations_linear
        self.__iterations._maxIterations_nonlinear = numerics_heat.maxIterations_nonlinear
        self.__iterations._norm = numerics_heat.norm
        self.__iterations._tollerance_linear = numerics_heat.tollerance_linear 
        self.__iterations._tollerance_nonlinear = numerics_heat.tollerance_nonlinear

        self.__solver._linear = numerics_heat.linear
        self.__solver._precond = numerics_heat.precond
        self.__solver._matrixStorage = numerics_heat.matrixStorage

        self.__numberOfGaussPoints = numerics_heat.numberOfGaussPoints     

#################################################################
#  class: SimulationData
#  Task:
#      used in operations partition mesh, writeFiles
# 

class SimulationData:

    def __init__( self, flowProcess, massProcessFlag, heatProcessFlag, coupledFlag, processing, numberOfCPUs, lumpingFlag, nonlinearFlag ):

        self.__processes = processes
        self.__processes._flow = flowProcess
        self.__processes._massFlag = massProcessFlag
        self.__processes._heatFlag = heatProcessFlag

        self.__coupledFlag = coupledFlag   # 0, 1
        self.__processing = processing   # sequential, mpi_elements, mpi_nodes, omp
        self.__numberOfCPUs = numberOfCPUs
        self.__lumpingFlag = lumpingFlag   # 0, 1
        self.__nonlinearFlag = nonlinearFlag   # 0, 1

    def getFlowProcess( self ):
        return self.__processes._flow 
    def getMassProcessFlag( self ):
        return self.__processes._massFlag 
    def getHeatProcessFlag( self ):
        return self.__processes._heatFlag 
    def getCoupledFlag( self ):
        return self.__coupledFlag 
    def getProcessing( self ):
        return self.__processing
    def getNumberOfCPUs( self ):
        return self.__numberOfCPUs
    def getLumpingFlag( self ):
        return self.__lumpingFlag
    def getNonlinearFlag( self ):
        return self.__nonlinearFlag

    def set( self, flowProcess, massProcessFlag, heatProcessFlag, coupledFlag, processing, numberOfCPUs, lumpingFlag, nonlinearFlag ):

        self.__processes._flow = flowProcess
        self.__processes._massFlag = massProcessFlag 
        self.__processes._heatFlag = heatProcessFlag 
        self.__coupledFlag = coupledFlag
        self.__processing = processing
        self.__numberOfCPUs = numberOfCPUs          
        self.__lumpingFlag = lumpingFlag
        self.__nonlinearFlag = nonlinearFlag


    def writeNumerics( self, directory ):
        

        f = open( directory + configurationShared.examplesName + '.num', 'w' )
        if self.__coupledFlag == '1': 
            coupling = CouplingNumerics()
            coupling.write( f )
            del coupling
        flow = ProcessNumerics( 'flow')       
        flow.write( f, self )
        del flow
        if self.__processes._massFlag == '1':
            mass = ProcessNumerics( 'mass')       
            mass.write( f, self )
            del mass
        if self.__processes._heatFlag == '1':
            heat = ProcessNumerics( 'heat')       
            heat.write( f, self )  
            del heat    
        f.write( '\n#STOP\n' )          
        f.close()


    #################################################################################

      
