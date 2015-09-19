import subprocess

class Operation:
 
    __cType = ""
    __cCase = ""
    __cConfiguration = ""
    
    __operations = []
    __root_directory = "C:\\"
    __root_directory_examples = ""
    
    __directory_example = ""
    __examplesName = ""
    
    __selectedOperation = ""
      
    def __init__( self, cComputer, cCode, cBranch, operating_system ):
        self.__cComputer = cComputer
        self.__cCode = cCode
        self.__cBranch = cBranch
        self.__operating_system = operating_system
        print(operating_system)
        
    def configureGlobal( self):
    
        self.__operations[:] = []
        self.__operations.append("(r)un")
        # add operations here
        if self.__operating_system == "windows":
            self.__root_directory_examples = self.__root_directory + "testingEnvironment\\" + self.__cCode + "\\" + self.__cBranch + "\\examples\\"
        elif self.__operating_system == "linux": 
            self.__root_directory_examples = self.__root_directory + "testingEnvironment/" + self.__cCode + "/" + self.__cBranch + "/examples/"
        else:
            print("ERROR - Operating system " + self.__operating_system + " not supported")
           
        self.__examplesName = "testCase"   
        
                
    def select( self ):
 
        print( "\nSelect operation:\n" )           
        for operation in self.__operations:
            print( operation )
                       
        self.__selectedOperation = input( '\n' )    
        
            
    def configureExample( self):
    
        if self.__operating_system == "windows":    
            self.__directory_example = self.__root_directory_examples + self.__cType + "\\" + self.__cCase + "\\"# + self.__cConfiguration + "\\"     
        elif self.__operating_system == "linux":       
            self.__directory_example = self.__root_directory_examples + self.__cType + "/" + self.__cCase + "/" #+ self.__cConfiguration + "/"     
        else:
            print("ERROR - Operating system " + self.__operating_system + " not supported")
                       
    def operate( self, cType, cCase, cConfiguration ):
        self.__cType = cType
        self.__cCase = cCase
        self.__cConfiguration = cConfiguration        
        
        self.configureExample()
        
        if self.__selectedOperation == "r":
            self.run()   
        else:
            print ("ERROR - Operation not supported") 
                       
    def run( self ):          
        if self.__operating_system == "windows":    
            executable = self.__root_directory + "testingEnvironment\\" + self.__cCode + "\\"  + self.__cBranch   +  "\\releases\\" + self.__cCode + "_" + self.__cBranch + "_" + "windows" + "_" + self.__cConfiguration + ".exe" 
          
        print(executable)
        print(self.__directory_example)
        with open ('output.txt', 'wb') as f:
            if self.__operating_system == "windows":  
                subprocess.check_call(executable + " " + self.__directory_example + self.__examplesName, stdout=f)   
            elif self.__operating_system == "linux":
                subprocess.check_call("qsub " + self.__directory_example + "run.bat", stdout=f)               
            else:
                print("ERROR - Operating system " + self.__operating_system + " not supported")
        
             
        
        
        
        
