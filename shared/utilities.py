import sys, os, shutil, platform
import configurationShared

#################################################################
#  error
#  Task:
#      prints message on console if verbosity > 0
#  Options:
#      Info: only text
#      Warning: text and name of function where call is from
#      Error: text and name of function where call is from      
#  Parameter:
#      type (string): ['INFO', 'WARNING', 'ERROR']
#      text (string): message
#      notSupported (string): prints '*** is not supported' (option to text)   
#

def message ( type= 'ERROR', text= None, notSupported= None ):

    if configurationShared.verbosity > 0:
        if not notSupported:
            message = text    
        else:
            message = notSupported + ' is not supported'
                  
        if type == 'INFO':
            intext = ''
        else:
            intext = ' in function ' + sys._getframe(1).f_code.co_name   
            
        print(type + intext +  ' - ' + message )

#################################################################

def unix2dos( file ):            
    infile = open(file,'r') 
    outfile = open( 'dos_' + file, 'w') 
    for line in infile: 
         line = line.rstrip() + '\r\n' 
         outfile.write(line) 
    infile.close() 
    outfile.close()         
    shutil.move('dos_' + file, file) 

def dos2unix( file ): 
    text = open(file, 'rb').read().replace('\r\n', '\n')
    open(file, 'wb').write(text)


#################################################################
#  adaptPath
#  Task:
#      converts windows path into linux (unix) according to platform where script runs
#
        
def adaptPath( path ):   
    if platform.system() == 'Windows':  
        return path  
    elif platform.system() == 'Linux':
        return path.replace( '\\', '/' )              
    else:
        message( type='ERROR', notSupported=platform.system() )
            
#################################################################
#  adaptPathSelectedComputer
#  Task:
#      converts windows path into linux (unix) and vice verca according to platform of selected computer
#      used for plotting operations (all local while simulation operations might be remote)
        
def adaptPathSelectedComputer( path, operatingSystem ):   
    if operatingSystem == 'windows':  
        return path.replace( '/', '\\' )   
    elif operatingSystem == 'linux':
        return path.replace( '\\', '/' )              
    else:
        message.console( type='ERROR', notSupported=operatingSystem )

#################################################################
#  generate Folder
#  Task:
#     called if folder is missing 
#        
        
def generateFolder( root, folderList ):  
     
    path = root  
    for folder in folderList:   
        path =  adaptPath( path + folder + '\\'  )
        
        try:
            os.stat( path )
        except:
            os.mkdir( path ) 

#################################################################
#  Remove file
#  Task:
#     Remove file if exists 
#        

def removeFile( fileName):

    try:
        os.remove(fileName)
        message( type='INFO', text='Removing ' + fileName )
    except OSError:
        pass        