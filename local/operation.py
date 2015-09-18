import subprocess

class Operation:
 
    __cType = ""
    __cCase = ""
    __cConfiguration = ""
    
    __operations = []
    __root_directory_executables = ""
    __root_directory_examples = ""
    __directory_example = ""
    
    __selectedOperation = ""
    
    def __init__( self, cComputer, cCode, cBranch ):
        self.__cComputer = cComputer
        self.__cCode = cCode
        self.__cBranch = cBranch
   
    def configureGlobal ( self):
        self.__operations.append("(r)un")
      
        ##
        if self.__cComputer == "local":
            self.__root_directory_executables = "C:\\Users\\delfs\\Desktop\\"            
            self.__root_directory_examples = "C:\\Users\\delfs\\Desktop\\"            
        elif self.__cComputer == "rzcluster":
            self.__root_directory_executables = "sungw389/home" 
            self.__root_directory_examples =  "sungw389/work_j"                    
        elif self.__cComputer == "NEC":
            self.__root_directory_executables = "sungw389/home"
            self.__root_directory_examples = "sungw389/work"                     
        elif self.__cComputer == "Lokstedt":
            self.__root_directory_executables = "jens/home"
            self.__root_directory_examples = "jens/work"                                    
        else:
            print ( "ERROR - No operation for computer " +str(self.__cComputer) )
            
        examplesName = "testCase"    
        
                
    def select( self ):
 
        print ( "\nSelect operation:\n" )           
        for operation in self.__operations:
            print ( operation )
                       
        self.__selectedOperation = input( '\n' )    
        
            
    def configureExample( self):
    
        self.__directory_example = self.__root_directory_examples + self.__cCode+ "\\"  + self.__cBranch + "\\examples\\" + self.__cType + "\\" + self.__cCase + "\\" + self.__cConfiguration + "\\"     
       
            
    def operate ( self, cType, cCase, cConfiguration ):
        self.__cType = cType
        self.__cCase = cCase
        self.__cConfiguration = cConfiguration        
        
        self.configureExample()
        
        if self.__selectedOperation == "r":
            self.run()   
        else:
            print ("ERROR - Operation not supported") 
                       
    def run ( self ):          
        executable = self.__root_directory_executables + self.__cCode+ "\\"  + self.__cBranch   +  "\\Release\\" + self.__cConfiguration  + "\\" + self.__cCode + "_" + self.__cComputer + "_" + self.__cConfiguration + ".exe" 
 
        with open ('output.txt', 'wb') as f:
            subprocess.check_call(executable + " " + self.__directory_example + examplesName, stdout=f)   
            
    
             
        
        
        
        