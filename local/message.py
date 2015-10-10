import sys
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

def console ( type='ERROR', text='', notSupported='' ):

    if configurationShared.verbosity > 0:
        if notSupported is not '':
            message = notSupported + ' is not supported'
        else:    
            message = text    
          
        if type == 'INFO':
            intext = ''
        else:
            intext = ' in ' + sys._getframe(1).f_code.co_name   
            
        print(type + intext +  ' - ' + message )