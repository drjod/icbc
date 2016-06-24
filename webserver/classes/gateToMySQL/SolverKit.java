package gateToMySQL;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;



public class SolverKit {

	private ArrayList<HashMap<String,String>> solverTableList;
	private ArrayList<HashMap<String,String>> preconditionerTableList;
	
	private HashMap<String,String> configurationsTable;
		
	public SolverKit() {
		solverTableList = new ArrayList<HashMap<String,String>>();
		preconditionerTableList = new ArrayList<HashMap<String,String>>();
		configurationsTable = new HashMap<String,String>();
	}
	
	public ArrayList<HashMap<String,String>> getSolverTableList() {
		return solverTableList;
	}

	public ArrayList<HashMap<String,String>> getPreconditionerTableList() {
		return preconditionerTableList;
	}
		
	public HashMap<String, String> getConfigurationsTable() {
		return configurationsTable;
	}
	
	public String configurationId2Name(String configurationsID) {		
		return configurationsTable.get(configurationsID);
	}
	
	
	public void getDataFromDatabase(User user) {
		
		System.out.println("Setting up solverKit");
		
		DbManager database = new DbManager();
		database.connect("root", user.getPassword() );
		
		ResultSet configurationsSet = database.query("SELECT * FROM configurations");
		
		ResultSet runningSolverSet, runningPreconditionerSet; // depend on configuration
		String solverTableName, preconditionerTableName;
	
		HashMap<String,String> solverTable, preconditionerTable; 
	
		try {
			configurationsSet.first();
				configurationsSet.previous();
			
			while (configurationsSet.next()) {
				configurationsTable.put(configurationsSet.getString("id"), 
						                configurationsSet.getString("name"));	
						
				solverTableName = configurationsSet.getString("solver_table_name");  // solver and preconditioner table depends on configuration
				preconditionerTableName = configurationsSet.getString("preconditioner_table_name");
				//System.out.println( solverTableName);
				//System.out.println( preconditionerTableName);
				
				solverTable = new HashMap<String,String>();
				preconditionerTable = new HashMap<String,String>();
				
				runningSolverSet = database.query("SELECT * FROM " + solverTableName);
				while (runningSolverSet.next()) {
				    solverTable.put( runningSolverSet.getString("id"), runningSolverSet.getString("name"));
				    //System.out.println( runningSolverSet.getString("specification"));
				    //System.out.println( runningSolverSet.getString("name"));
				}
				runningPreconditionerSet = database.query("SELECT * FROM " + preconditionerTableName);				
				while (runningPreconditionerSet.next())
					preconditionerTable.put( runningPreconditionerSet.getString("id"), runningPreconditionerSet.getString("name"));				
					
				solverTableList.add(solverTable);
				preconditionerTableList.add(preconditionerTable);
				
				solverTable = null;
				preconditionerTable = null;		
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//for ( String elem : solverTableList.get(0).keySet() )
		//	  System.out.println( elem );
		
		//System.out.println(solverTableList.get(0).get("2"));
		/*String name;
		 * Enumeration enumeration = solverTableList.get(0).keys();
		  while (enumeration.hasMoreElements())
		  {
			  name = (String) enumeration.nextElement();
			  System.out.println(name + " " + solverTableList.get(0).get(name));
		  }*/


	}
	
}
