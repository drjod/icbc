<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%@ page import="gateToMySQL.SubjectsSetup" %>
<%@ page import="gateToMySQL.ExamplesSetup" %>
<%@ page import="gateToMySQL.ConfigurationsSetup" %>
<%@ page import="gateToMySQL.SolverKit" %>
<%@ page import="java.util.HashMap"%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Menu</title>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.js" type="text/javascript"> </script>


<script type = "text/javascript">

function showPlot(type)
{
	
	document.location.href="ShowPlot?typeToPlot=" + type;
}

</script>

</head>

<%---------------------------------------------------------------------------------------%>

<body>


<jsp:useBean id='subjects' class='gateToMySQL.SubjectsSetup' scope='session' /> 
<jsp:useBean id='examples' class='gateToMySQL.ExamplesSetup' scope='session' />
<jsp:useBean id='solverKit' class='gateToMySQL.SolverKit' scope='session' /> 

<%--<jsp:getProperty property="caseList" name="examples"/>--%>



<%---------------------------------------------------------------------------------------%>
<%--------------------- FORM: EXAMPLE TABLE ---------------------------------------------%>
<%---------------------------------------------------------------------------------------%>

<form name="table" method="post" action="Update"> 


<h2> Testing menu </h2>

<select name="computer" id='computer' > 
<c:forEach var="current" items="${subjects.computerList}" >
<option value="${current.id}" id="${current.id}" 
<c:if test="${current.id == subjects.selectedComputer}"> selected="selected" </c:if> > 
<c:out value="${current.name}" /> </option>
</c:forEach>
</select>

<select name="code" id="code" > 
<c:forEach items="${subjects.codesList}" var="current">
<option value="${current}" id="${current}" 
<c:if test="${current == subjects.selectedCode}"> selected="selected" </c:if> > 
<c:out value="${current}" /> </option>
</c:forEach>
</select>

<select name="branch" id="branch" > 
<c:forEach items="${subjects.branchesList}" var="current">
<option value="${current}" id="${current}" 
<c:if test="${current == subjects.selectedBranch}"> selected="selected" </c:if> > 
<c:out value="${current}" /> </option>
</c:forEach>
</select>

<select name="configurationSet" id="configurationSet" multiple size=5 > 
<c:forEach var="current" items="${subjects.selectedComputerInstance.configurationsList}"> 
<option value="${current}" id="${current}" 
<c:if test="${current == subjects.selectedConfiguration}"> selected="selected" </c:if> > 
 <c:out value="${solverKit.configurationId2Name(current)}"/>
</option>
 </c:forEach>
</select>


<input type="button" value="Build" name="build" id="build" >
<input type="button" value="Simulate" name="simulate" id="simulate" >
<input type="button" value="Plot" name="plot" id="plot" >



<br/> <br/> <br/> <br/>

<h2> Benchmark table </h2>
<input type="submit" value="Update database" name="submit" > 

<select name="configuration" id="configuration" >  <%-- id for AJAX --%>
<c:forEach var="config" items="${solverKit.configurationsTable}"> 
<option value="${config.key}" id="${config.key}" 
<c:if test="${config.key == examples.selectedConfiguration}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${config.value}"/>
</option>
 </c:forEach>
</select>


<%------------------------------------------------------------------------------------------%>
<%--------------------- TABLE: BENCHMARK TABLE ---------------------------------------------%>

<table border="1">
<c:forEach var="i" begin="0" end="${examples.caseList.size()-1}" >
 <tr>
  <%-- Counter column --%>
<td><c:out value="${i}"/> </td>
  <%-- state column --%>
<td> 
<input type="checkbox" name="state_${i}" value="1" 
<c:if test="${examples.problemList[i].state == 1}"> checked="checked" </c:if> >  
</td>
 <%-- Type column --%>
<td> <c:if test="${examples.typeList[i] != examples.typeList[i-1]}" >  <%-- addresses -1 --%>
<input type="button" value="view" name="view" id="view" onClick="showPlot('${examples.typeList[i]}')" >
    <c:out value="${examples.typeList[i]}"/>
</c:if> </td>
 <%-- Case column --%>
<td><c:out value="${examples.caseList[i]}"/></td>
<%-- Flow process (coupled) column --%>
 <td><c:out value="${examples.problemList[i].flowProcess}"/>
 <c:if test="${examples.problemList[i].coupledFlag == 1}" >
    <c:out value="COUPLED"/> </c:if> </td> 
 <%-- Numerics flow column --%>
<td> 
<select name="solver_flow_${i}"  >
<c:forEach var="entry" items="${solverKit.solverTableList[examples.selectedConfiguration]}"> 
<option id="${entry.value}" value="${entry.key}" 
<c:if test="${entry.key == examples.problemList[i].processes[0].solverList[examples.selectedConfiguration]}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${entry.value}"/>
</option>
 </c:forEach>
</select>

<select name="preconditioner_flow_${i}"  >
<c:forEach var="entry" items="${solverKit.preconditionerTableList[examples.selectedConfiguration]}"> 
<option id="${entry.value}" value="${entry.key}" 
 <c:if test="${entry.key == examples.problemList[i].processes[0].preconditionerList[examples.selectedConfiguration]}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${entry.value}"/>
</option>
 </c:forEach>
</select>

<input type="text" name="theta_flow_${i}" value="${examples.problemList[i].processes[0].theta}" size="2" >

<input type="checkbox" name="lumping_flow_${i}" value="1" 
<c:if test="${examples.problemList[i].lumpingFlow == 1}"> checked="checked" </c:if> >  
</td>
 <%-- Numerics heat column --%>
<td>
<c:if test="${examples.problemList[i].heatFlag == 1}" >
 
<select name="solver_heat_${i}"  >
<c:forEach var="entry" items="${solverKit.solverTableList[examples.selectedConfiguration]}"> 
<option id="${entry.value}" value="${entry.key}"
<c:if test="${entry.key == examples.problemList[i].processes[1].solverList[examples.selectedConfiguration]}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${entry.value}"/>
</option>
 </c:forEach>
</select>

<select name="preconditioner_heat_${i}"  >
<c:forEach var="entry" items="${solverKit.preconditionerTableList[examples.selectedConfiguration]}"> 
<option id="${entry.value}" value="${entry.key}" 
 <c:if test="${entry.key == examples.problemList[i].processes[1].preconditionerList[examples.selectedConfiguration]}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${entry.value}"/>
</option>
 </c:forEach>
</select>

<input type="text" name="theta_heat_${i}" value="${examples.problemList[i].processes[1].theta}" size="2" >
</c:if> </td>
 <%-- Numerics mass column --%>
<td> 
<c:if test="${examples.problemList[i].massFlag == 1}" >

<select name="solver_mass_${i}"  >
<c:forEach var="entry" items="${solverKit.solverTableList[examples.selectedConfiguration]}"> 
<option id="${entry.value}" value="${entry.key}" 
<c:if test="${entry.key == examples.problemList[i].processes[2].solverList[examples.selectedConfiguration]}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${entry.value}"/>
</option>
 </c:forEach>
</select>

<select name="preconditioner_mass_${i}"  >
<c:forEach var="entry" items="${solverKit.preconditionerTableList[examples.selectedConfiguration]}"> 
<option id="${entry.value}" value="${entry.key}" 
 <c:if test="${entry.key == examples.problemList[i].processes[2].preconditionerList[examples.selectedConfiguration]}"> selected="selected" </c:if> >  <%-- OGS_FEM --%>
 <c:out value="${entry.value}"/>
</option>
 </c:forEach>
</select>

<input type="text" name="theta_mass_${i}" value="${examples.problemList[i].processes[2].theta}" size="2" >
</c:if> </td>
 
</tr>
</c:forEach>
</table>

</form>

<script type="text/javascript">

$(document).ready(function() {
    $('#build').click(
    	    function(event){
    	    	var operation = 'building';
    	    	var configurationSet = $('#configurationSet').val();	   
    	    $.ajax({
    	    type : "POST",
    	    url : "GateToPython",
    	    data : "operation=" + operation + "&configurationSet=" + configurationSet,
    	    success : function(msg) {
    	    	return true;
    	    },
    	    error : function(e) {
    	    	return false;
    	    }
    	    })
    	    });	
    
    $('#simulate').click(
    	    function(event){
    	    	var operation = 'simulating'
    	    	var configurationSet = $('#configurationSet').val();	
    	    $.ajax({
    	    type : "POST",
    	    url : "GateToPython",
    	    data : "operation=" + operation + "&configurationSet=" + configurationSet,
    	    success : function(msg) {
    	    	return true;
    	    },
    	    error : function(e) {
    	    	return false;
    	    }
    	    })
    	    });	
   
    $('#plot').click(
    	    function(event){
    	    	var operation = 'plotting'
    	    	var configurationSet = $('#configurationSet').val();	
    	    $.ajax({
    	    type : "POST",
    	    url : "GateToPython",
    	    data : "operation=" + operation + "&configurationSet=" + configurationSet,
    	    success : function(msg) {
    	    	return true;
    	    },
    	    error : function(e) {
    	    	return false;
    	    }
    	    })
    	    });	
    
    
    // drop boxes for subject
    $('#computer').change(
    function(event){
    	var computer = $('#computer').val();
    	var code = $('#code').val();
    	var branch = $('#branch').val();
    	var configurationSet = $('#configurationSet').val();        	
    	$.ajax({
    type : "POST",
    url : "ChangeSubject",
    data : "computer=" + computer + "&code=" + code + "&branch=" + branch + "&configurationSet=" + configurationSet,
    success : function(msg) {
    	return true;
    },
    error : function(e) {
    	return false;
    }
    })
    });	 

    $('#code').change(
    	    function(event){
    	    	var computer = $('#computer').val();
    	    	var code = $('#code').val();
    	    	var branch = $('#branch').val();
    	    	var configurationSet = $('#configurationSet').val();    	    	
    	    	$.ajax({
    	    type : "POST",
    	    url : "ChangeSubject",
    	    data : "computer=" + computer + "&code=" + code + "&branch=" + branch + "&configurationSet=" + configurationSet,    	    
    	    success : function(msg) {
    	    	return true;
    	    },
    	    error : function(e) {
    	    	return false;
    	    }
    	    })
    	    });	    
    
    $('#branch').change(
    	    function(event){
    	    	var computer = $('#computer').val();
    	    	var code = $('#code').val();
    	    	var branch = $('#branch').val();
    	    	var configurationSet = $('#configurationSet').val();    	    	
    	    	$.ajax({
    	    type : "POST",
    	    url : "ChangeSubject",
    	    data : "computer=" + computer + "&code=" + code + "&branch=" + branch + "&configurationSet=" + configurationSet,    	    
    	    success : function(msg) {
    	    	return true;
    	    },
    	    error : function(e) {
    	    	return false;
    	    }
    	    })
    	    });	 
    
    $('#configurationSet').change(   		
    	    function(event){
    	    	var computer = $('#computer').val();
    	    	var code = $('#code').val();
    	    	var branch = $('#branch').val();
    	    	var configurationSet = $('#configurationSet').val();    	    	
    	    	$.ajax({
    	    type : "POST",
    	    url : "ChangeSubject",
    	    data : "computer=" + computer + "&code=" + code + "&branch=" + branch + "&configurationSet=" + configurationSet,    	    
    	    success : function(msg) {
    	    	return true;
    	    },
    	    error : function(e) {
    	    	return false;
    	    }
    	    })
    	    });	   
    
});
</script>

</body>
</html>