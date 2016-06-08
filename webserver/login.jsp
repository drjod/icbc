<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>
<form name="login" method="post" action="DBManager.jsp">
<table border="0">
<tbody>
 <tr>
  <td>User name:</td>
  <td><input type="text" name="userName" value="root" size="20"> </td>
  </tr>
   <tr>
  <td>Password:</td>
    <td><input type="password" name="password"  size="20"> </td>
  </tr>
  </tbody>
</table> 
<input type="reset" value="Clear" name="clear" >
<input type="submit" value="Submit" name="submit" >
</form>
</body>
</html>
