package servlets;

import gateToMySQL.*;
import java.io.IOException;
import java.util.ArrayList;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Servlet implementation class Entry
 */
@WebServlet("/Entry")
public class Entry extends HttpServlet {
	private static final long serialVersionUID = 1L;
       

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
				
		//System.out.println("logged in as " + request.getParameter("userName"));
	
		User user= new User(request.getParameter("userName"), request.getParameter("password") );
		SubjectsSetup subjects = new SubjectsSetup();
		SolverKit solverKit = new SolverKit();
		ExamplesSetup examples = new ExamplesSetup();
		
		if(!subjects.getDataFromDatabase(user))
			response.sendRedirect("login.jsp");  // causes error
			
		solverKit.getDataFromDatabase(user);
		examples.getDataFromDatabase(user, solverKit.getConfigurationsTable());		
		
		//Computer computer = subjects.getSelectedComputerInstance();
		
		
		HttpSession session = request.getSession();
		session.setAttribute("subjects", subjects );
		session.setAttribute("examples", examples );
		session.setAttribute("solverKit", solverKit );
		session.setAttribute("user", user );
		
		System.out.println("subject config " + subjects.getSelectedConfiguration());
		
		response.sendRedirect("menu.jsp");
				
	}

}



