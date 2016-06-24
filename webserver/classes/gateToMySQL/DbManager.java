package gateToMySQL;

import java.sql.*;
import java.io.*;


public class DbManager {
	String URL = "jdbc:mysql://localhost:3306/testing_environment";
	String driver = "com.mysql.jdbc.Driver";
	
	Connection connection = null;
	PreparedStatement statement = null;
	ResultSet result = null;

	
	public DbManager() {
		try { Class.forName(driver).newInstance(); } 
		catch (InstantiationException e) { e.printStackTrace(); } 
		catch (IllegalAccessException e) { e.printStackTrace(); } 
		catch (ClassNotFoundException e) { e.printStackTrace(); } 
	}
	
    public void connect(String _username, String _password){
    	System.out.println("Connecting - " + URL);
    	try{
			connection = DriverManager.getConnection( URL, _username, _password); 
		}
		catch(SQLException e)
	    {
			e.printStackTrace(); 
	    }	
	}
    
    public void disconnect(){
		System.out.println("Closing connection - " + URL);
		try {
			connection.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		connection = null;
	}
	
	public ResultSet query(String SQLcommand) {
		System.out.println("Executing query " + SQLcommand);
		try{
			statement=connection.prepareStatement(SQLcommand);
			result = statement.executeQuery();	
			//statement.close();
		}
		catch(SQLException e)
	    {
			e.printStackTrace(); 
	    }
		return result;
	}
	
	public void update(String SQLcommand) {
		
		System.out.println("Executing query" + SQLcommand);
		try{
			statement=connection.prepareStatement(SQLcommand);
			statement.executeUpdate();	
			//statement.close();
		}
		catch(SQLException e)
	    {
			e.printStackTrace(); 
	    }
	}
	

	public void updateTextField(String parameter, String value, String exampleId) {	
		
		update ( "UPDATE cases SET " + parameter + "=\"" + value + "\" WHERE id=\"" + exampleId2caseId( exampleId )+"\"" );	
	}
	
	
	public void updateCheckbox(String parameter, String value, String exampleId) {	
		
		String tableValue = new String();
		
		if( value  != null)
			tableValue = "1"; // checked
		else 
			tableValue= "0";  // unchecked 
		
		update ( "UPDATE cases SET " + parameter + "=" + tableValue + " WHERE id=\"" + exampleId2caseId( exampleId )+"\""  );	
	}
	
	public String exampleId2caseId(String exampleId) {	
		
		String caseId = new String();
		
		ResultSet caseSet = query ("SELECT * from examples WHERE id=" + exampleId );
		try {
			caseSet.next();  // only one
			caseId = caseSet.getString("case_id");
		} catch (SQLException e) {
			e.printStackTrace();
		} 
		return caseId;
		
	}	
	
}
