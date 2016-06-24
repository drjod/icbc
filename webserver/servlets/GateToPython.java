package servlets;

import gateToMySQL.*;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.apache.tomcat.jni.File;

/**
 * Servlet implementation class Build
 */
@WebServlet("/GateToPython")   // 
public class GateToPython extends HttpServlet {
	private static final long serialVersionUID = 1L;

      
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		String operation = request.getParameter("operation");
		HttpSession session = request.getSession();
		SubjectsSetup subjects = (SubjectsSetup)session.getAttribute("subjects");
		SolverKit solverKit = (SolverKit)session.getAttribute("solverKit");
		
		String computer = subjects.getSelectedComputerInstance().getName();
		String code = subjects.getSelectedCode();
		String branch = subjects.getSelectedBranch();
		String configurationSet = request.getParameter("configurationSet");
		String[] splittedConfigurationSet = configurationSet.split(",");
		
		for(String config : splittedConfigurationSet) {
			
			String configName = solverKit.configurationId2Name(config);
			System.out.println( operation + " " + code + " "  + branch + " " + configName + " on " + computer );
			
		    try {
		        Process p =  Runtime.getRuntime().exec("cmd /c F:\\testingEnvironment\\scripts\\icbc\\automaticTesting\\run.bat " 
		                           + operation + " " +  computer + " " + code + " " + branch + " " + configName );
		        System.out.println("manual scheduler for application.."+p);
		    } catch(Exception e) {  
		    	System.out.println(e);
		    }
	   
		}
	    response.sendRedirect("menu.jsp");
	    
	}

}
