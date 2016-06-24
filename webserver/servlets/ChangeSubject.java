package servlets;

import gateToMySQL.*;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Servlet implementation class ChangeSubject
 */
@WebServlet("/ChangeSubject")
public class ChangeSubject extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		String computer = request.getParameter("computer");
		 
		String code = request.getParameter("code");
		String branch = request.getParameter("branch");
		String configuration = request.getParameter("configurationSet");
		
		System.out.println("Change subject - selected " + computer + " "
				 + code + " " + branch + " " + configuration);
		
		HttpSession session = request.getSession();
		SubjectsSetup subjects = (SubjectsSetup)session.getAttribute("subjects");
		
		subjects.setSelectedComputer(computer);
		subjects.setSelectedCode(code);
		subjects.setSelectedBranch(branch);
		subjects.setSelectedConfiguration(configuration); 
		
		response.sendRedirect("menu.jsp");
	}

}
