package gateToMySQL;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class SubjectsSetup {

	private String selectedCode;  // names
	private String selectedBranch;  // names
	private String selectedComputer;  // id
	private String selectedConfiguration;  // id
	
	private ArrayList<String> codesList;
	private ArrayList<String> branchesList;
	private ArrayList<Computer> computerList;

	
	public SubjectsSetup() {
			
		selectedCode = new String();
		selectedBranch = new String();

		selectedComputer = "0"; // initialize - default
		selectedConfiguration = "0";
		
		codesList = new ArrayList<String>();
		branchesList = new ArrayList<String>();
		computerList = new ArrayList<Computer>();
	}
	
	public ArrayList<String> getCodesList() {
		return codesList;
	}

	public ArrayList<String> getBranchesList() {
		return branchesList;
	}

	public ArrayList<Computer> getComputerList() {
		return computerList;
	}
	
	public String getSelectedConfiguration() {
		return selectedConfiguration;
	}

	public String getSelectedCode() {
		return selectedCode;
	}

	public String getSelectedBranch() {
		return selectedBranch;
	}

	public String getSelectedComputer() { // provides the computer id
		return selectedComputer;
	}
	
	public Computer getSelectedComputerInstance() {
		for( Computer computer: computerList )
			if( computer.getId().equals(selectedComputer))
				return computer;
		
		System.out.println("ERROR in getSelectedComputerInstance()");
		return null;
	}
	

	public void setSelectedCode(String selectedCode) {
		this.selectedCode = selectedCode;
	}

	
	public void setSelectedBranch(String selectedBranch) {
		this.selectedBranch = selectedBranch;
	}
	
	public void setSelectedComputer(String selectedComputer) {
		System.out.println("set comp " + selectedComputer);
		this.selectedComputer = selectedComputer;
	}

	public void setSelectedConfiguration(String selectedConfiguration) {
		this.selectedConfiguration = selectedConfiguration;
	}

	public Boolean getDataFromDatabase(User user) {
		
		DbManager database = new DbManager();	
	    database.connect("root", user.getPassword() );
	    Computer computer;
	    
	    ResultSet resultSet = database.query("SELECT * FROM superuser WHERE name=\"" + user.getName() + "\"");	
	   	ResultSet resultSet1;
	   	
		try {
			while(resultSet.next()) {
				// superuser exists
				resultSet1 = database.query("SELECT * FROM computer WHERE id=\"" + 
				                   resultSet.getString("computer_id") + "\"");// computer of superuser 
				while(resultSet1.next()) { 
					computer = new Computer();
					computer.setId(resultSet1.getString("id"));
					computer.setName(resultSet1.getString("name"));
					computer.getDataFromDatabase(user); // configure configurations
					//System.out.println("comp " + resultSet1.getString("name"));
					computerList.add(computer);
				}
			}
			
			if(computerList.isEmpty())
				return false; // superuser not known - is not a user
		
			// codes and branches are independent of computer etc.
			resultSet = database.query("SELECT * FROM codes");
			while(resultSet.next()) {
				codesList.add(resultSet.getString("name"));
				if(resultSet.getString("id").equals("0"))
					selectedCode = resultSet.getString("name"); // initialize - set default
			}
			resultSet = database.query("SELECT * FROM branches");
			while(resultSet.next()) {
				branchesList.add(resultSet.getString("name"));
				if(resultSet.getString("id").equals("0"))
					selectedBranch = resultSet.getString("name"); // initialize - set default
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		  
		database.disconnect(); 
		
		return true;
		
		//for(String configuration: configurationsList)
		//	System.out.println(configuration);

		
	}
	
}