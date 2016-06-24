package gateToMySQL;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;



public class ExamplesSetup {

	private ArrayList<String> typeList;
	private ArrayList<String> caseList;
	private ArrayList<Problem> problemList;
	
    private String selectedConfiguration; // id
	
	public ExamplesSetup(){

		typeList = new ArrayList<String>();
		caseList = new ArrayList<String>();
		problemList = new ArrayList<Problem>();
	
		selectedConfiguration = "0"; // initialize - default
	}
	
	public ArrayList<String> getTypeList() {
		return typeList;
	}

	public ArrayList<String> getCaseList() {
		return caseList;
	}
	
	public ArrayList<Problem> getProblemList() {
		return problemList;
	}

	public String getSelectedConfiguration() {
		return selectedConfiguration;
	}
	
	public void setSelectedConfiguration(String selectedConfiguration) {
		this.selectedConfiguration = selectedConfiguration;
	}
	

	public void getDataFromDatabase(User user, HashMap<String,String> configurationsTable) {
		
		DbManager database = new DbManager();
		database.connect("root", user.getPassword() );

		ResultSet examplesSet = database.query("SELECT * FROM examples");		
		ResultSet typeItem, caseItem, flowProcessItem;    // depend on example - latter used for type, flowProcess

		Problem problem;
		
		try {
			while (examplesSet.next()) {	
				
				// EXAMPLE-SPECIFIC DATA BASE QUERIES - type, case, flowProcess, solverList, preconditionerList - list entries depend on configuration
				typeItem =  database.query("SELECT * FROM types WHERE id=\"" + examplesSet.getString("type_id") + "\"" );	
				caseItem =  database.query("SELECT * FROM cases WHERE id=\"" + examplesSet.getString("case_id") + "\"" );
				if (typeItem.next() && caseItem.next()) 
				{
					typeList.add(typeItem.getString("name"));
					caseList.add(caseItem.getString("name"));
				    flowProcessItem =  database.query("SELECT * FROM flow_processes WHERE id=\"" + caseItem.getString("flow_id") + "\"" ); 
				    if (flowProcessItem.next()) {						
				    	
				    	//System.out.println(flowProcessItem.getString("name"));
				    	problem = new Problem();
					    //for(String configuration: configurationsList) {
					    for (HashMap.Entry<String, String> config : configurationsTable.entrySet()) {
					    	problem.addToSolverList(caseItem.getString("solver_flow_" + config.getValue()), 
					    			caseItem.getString("solver_heat_" + config.getValue()), 
					    			caseItem.getString("solver_mass_" + config.getValue()));	
					    	//System.out.println(config +  " " + caseItem.getString("solver_flow_" + config.getValue() ));
					    	problem.addToPreconditionerList(caseItem.getString("preconditioner_flow_" + config.getValue()), 
					    			caseItem.getString("preconditioner_heat_" + config.getValue()), 
					    			caseItem.getString("preconditioner_mass_" + config.getValue()));					    	
					    }
				    	
						problem.setValues(caseItem.getString("state"), flowProcessItem.getString("name"), caseItem.getString("lumping_flow"), 
						        caseItem.getString("heat_flag"), caseItem.getString("mass_flag"), caseItem.getString("coupled_flag"),
				                caseItem.getString("theta_flow"), caseItem.getString("theta_heat"), caseItem.getString("theta_mass")
                                 );
						problemList.add(problem);
						problem = null;
					}				
				}
					
			}
		} 
		catch (SQLException e) {
			e.printStackTrace();
		}
		
		//for (Problem item: problemList )
		//	System.out.println(item.getCoupledFlag());
	    //for (String item: flowProcessList)
	    //	System.out.println(item);
	
	    //for (String _case: caseList)
	    //	System.out.println(_case);
	    
	    database.disconnect(); 				
	}
	

	public void updateDatabase(User user, SolverKit solverKit) {
		
	    DbManager database = new DbManager();
        database.connect("root", user.getPassword() );
        
    	for(int i= 0; i < getProblemList().size(); i++ )
    		getProblemList().get(i).updateDatabase(database, solverKit, selectedConfiguration, Integer.toString(i));
    		
		database.disconnect(); 		
			
	}
	
	
}