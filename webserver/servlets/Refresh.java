package servlets;

import gateToMySQL.*;
import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Servlet implementation class Refresh
 */
@WebServlet("/Refresh")
public class Refresh extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		String selectedConfiguration=request.getParameter("configuration");
		System.out.println("Refresh configuration in example table - selected " + selectedConfiguration);
		response.getWriter().append("Served at: ").append(request.getContextPath());
		
		HttpSession session = request.getSession();
		ExamplesSetup examples = (ExamplesSetup)session.getAttribute("examples" );
		examples.setSelectedConfiguration(selectedConfiguration);
		
        response.sendRedirect("menu.jsp");
	}

}
