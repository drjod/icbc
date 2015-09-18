import subprocess

class Operation:
 
    __cType = ""
    __cCase = ""
    __cConfiguration = ""
    
    __operations = []
    __root_directory_executables = ""
    __root_directory_examples = ""
    __directory_example = ""
    __examplesName = ""
    
    __selectedOperation = ""
    
    
    
    def __init__( self, cComputer, cCode, cBranch, operating_system="windows" ):
        self.__cComputer = cComputer
        self.__cCode = cCode
        self.__cBranch = cBranch
        self.__operating_system = operating_system
        print (operating_system)
        
    def configureGlobal( self):
    
        self.__operations[:] = []
        self.__operations.append("(r)un")
        # add operations here
      
        ##
        if self.__cComputer == "local":
            self.__root_directory = "F:\\"  #   "C:\\Users\\delfs\\Desktop\\"            
            # self.__root_directory_examples = "C:\\Users\\delfs\\Desktop\\"            
        elif self.__cComputer == "rzcluster":
            self.__root_directory = "work_j/sungw389"                    
        elif self.__cComputer == "NEC":
            self.__root_directory = "sfs/fs5/home-sh/sungw389"                                
        elif self.__cComputer == "Lokstedt":
            self.__root_directory = "home/jens"                                    
        else:
            print ( "ERROR - No operation for computer " +str(self.__cComputer) )
            
        if self.__operating_system == "windows":    
            self.__root_directory_examples = self.__root_directory + self.__cCode + "\\"  + self.__cBranch   + "\\examples\\files\\" 
        else:
            self.__root_directory_examples = self.__root_directory + self.__cCode + "/"  + self.__cBranch   + "/examples/files/"        
               
        self.__examplesName = "testCase"    
        
                
    def select( self ):
 
        print ( "\nSelect operation:\n" )           
        for operation in self.__operations:
            print ( operation )
                       
        self.__selectedOperation = input( '\n' )    
        
            
    def configureExample( self):
    
        if self.__operating_system == "windows":    
            self.__directory_example = self.__root_directory_examples + self.__cType + "\\" + self.__cCase + "\\" + self.__cConfiguration + "\\"     
        else:      
            self.__directory_example = self.__root_directory_examples + self.__cType + "/" + self.__cCase + "/" + self.__cConfiguration + "/"     
           
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
        if self.__operating_system == "windows":    
            executable = self.__root_directory + self.__cCode + "\\"  + self.__cBranch   +  "\\executables\\" + self.__cCode + "_" + self.__cComputer + "_" + self.__cConfiguration + ".exe" 
      
            with open ('output.txt', 'wb') as f:
                subprocess.check_call(executable + " " + self.__directory_example + self.__examplesName, stdout=f)   
        else:
            with open ('output.txt', 'wb') as f:
                subprocess.check_call( self.__directory_example + "run.bat", stdout=f)                      
            
    
             
        
        
        
        
