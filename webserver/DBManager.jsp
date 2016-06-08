<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %>
<% Class.forName("com.mysql.jdbc.Driver"); %>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>
<form method="post" action="DisplayImage">

<%!
public class DbManager {
	String URL = "jdbc:mysql://localhost:3306/testing_environment";

	
	Connection connection = null;
	PreparedStatement statement = null;
	ResultSet result = null;

	
	public DbManager() {}
	
    public void connect(String _username, String _password){
    	System.out.println("Connecting to database testing_environment");
    	try{
			connection = DriverManager.getConnection( URL, _username, _password); 
		}
		catch(SQLException e)
	    {
			e.printStackTrace(); 
	    }	
	}
    
    public void disconnect(){
		System.out.println("Closing connection to database testing_environment");
		try {
			connection.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		connection = null;
	}
	
	public ResultSet query(String SQLcommand) {
		System.out.println("Executing query" + SQLcommand);
		try{
			statement=connection.prepareStatement(SQLcommand);
			result = statement.executeQuery();	
		}
		catch(SQLException e)
	    {
			e.printStackTrace(); 
	    }
		return result;
	}
}
%>

<%
DbManager database = new DbManager();
database.connect(request.getParameter("userName"), request.getParameter("password"));

ResultSet types= database.query("SELECT * FROM types");
ResultSet computer= database.query("SELECT * FROM computer"); 
ResultSet code= database.query("SELECT * FROM codes");
ResultSet branch= database.query("SELECT * FROM branches");
%>
<h3>Select </h3>
	
<h4>Code - branch- computer </h4>	
<select name="code">			       
<%while(code.next()) {%>
  <option value=<%=code.getString("name")%> ><%=code.getString("name")%>  </option>
<%} %>			  
</select>   


<select name="branch">			       
<%while(branch.next()) {%>
  <option value=<%=branch.getString("name")%> ><%=branch.getString("name")%>  </option>
<%} %>			  
</select> 


<select name="computer">			       
<%while(computer.next()) {%>
  <option value=<%=computer.getString("name")%>><%=computer.getString("name")%>  </option>
<%} %>			  
</select> 

			                              
<h4>Example type: </h4>
<%while(types.next()) {%>
  <input type="radio" name="example" value=<%=types.getString("name")%>><%=types.getString("name")%> <br>
<%} %>
<input type="submit" />
</form>
</body>
</html>
