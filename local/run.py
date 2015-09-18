import gateToMySQL
import environment



gateToMySQL = gateToMySQL.GateToMySQL( 'root','***','localhost','testing_environment' )

environment = environment.Environment( gateToMySQL )
environment.select()

environment.run()

del gateToMySQL 




