package gateToMySQL;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class Computer {
	private String id;
	private String name;
	private ArrayList<String> configurationsList; // contains ids
	
	public Computer() {
		name = new String();
		configurationsList = new ArrayList<String>();
	}
	
	public String getId() {
		return id;
	}

	public String getName() {
		return name;
	}
	
	public ArrayList<String> getConfigurationsList() {
		return configurationsList;
	}

	public void setId(String id) {
		this.id = id;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public void getDataFromDatabase(User user) {  // sets configurationList
		
		DbManager database = new DbManager();
		database.connect("root", user.getPassword() );
		
		ResultSet resultSet;
		String id = "-1";
		try {
			resultSet = database.query("SELECT * FROM computer WHERE name=\"" + name + "\"" );
		
			if(resultSet.next()) {
				id =resultSet.getString("id");
 			    resultSet =  database.query("SELECT * FROM modi WHERE computer_id=\"" + id + "\"" );	
 			    while (resultSet.next())
 			    	configurationsList.add(resultSet.getString("configuration_id"));
			}	
			else 
				System.out.println("error");
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		System.out.println("computer " +  name);
		for (String conf : configurationsList )
			System.out.println(conf);
	
		database.disconnect();
	}
	
}
