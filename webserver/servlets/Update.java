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
 * Servlet implementation class Update
 */
@WebServlet("/Update")
public class Update extends HttpServlet {
	private static final long serialVersionUID = 1L;
       

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
	
		System.out.println("Update database");
		
		HttpSession session = request.getSession();
		ExamplesSetup examples = (ExamplesSetup)session.getAttribute("examples");
		SolverKit solverKit = (SolverKit)session.getAttribute("solverKit");
        User user = (User)session.getAttribute("user" );
		
        examples.setSelectedConfiguration(request.getParameter("configuration"));

		for(int i= 0; i < examples.getProblemList().size(); i++ ) {
			examples.getProblemList().get(i).setState(request.getParameter("state_"+ Integer.toString(i)));
			examples.getProblemList().get(i).setLumpingFlow(request.getParameter("lumping_flow_"+ Integer.toString(i)));
			
			examples.getProblemList().get(i).getProcesses().get(0).setTheta(request.getParameter("theta_flow_"+ Integer.toString(i)));	
			examples.getProblemList().get(i).getProcesses().get(1).setTheta(request.getParameter("theta_heat_"+ Integer.toString(i)));	
			examples.getProblemList().get(i).getProcesses().get(2).setTheta(request.getParameter("theta_mass_"+ Integer.toString(i)));	
			
			examples.getProblemList().get(i).getProcesses().get(0).setSolver(
					Integer.parseInt(examples.getSelectedConfiguration()), request.getParameter("solver_flow_"+ Integer.toString(i)));
			examples.getProblemList().get(i).getProcesses().get(1).setSolver(
					Integer.parseInt(examples.getSelectedConfiguration()), request.getParameter("solver_heat_"+ Integer.toString(i)));
			examples.getProblemList().get(i).getProcesses().get(2).setSolver(
					Integer.parseInt(examples.getSelectedConfiguration()), request.getParameter("solver_mass_"+ Integer.toString(i)));
			
			examples.getProblemList().get(i).getProcesses().get(0).setPreconditioner(
					Integer.parseInt(examples.getSelectedConfiguration()), request.getParameter("preconditioner_flow_"+ Integer.toString(i)));
			examples.getProblemList().get(i).getProcesses().get(1).setPreconditioner(
					Integer.parseInt(examples.getSelectedConfiguration()), request.getParameter("preconditioner_heat_"+ Integer.toString(i)));
			examples.getProblemList().get(i).getProcesses().get(2).setPreconditioner(
					Integer.parseInt(examples.getSelectedConfiguration()), request.getParameter("preconditioner_mass_"+ Integer.toString(i)));
		}

        examples.updateDatabase(user, solverKit);

		response.sendRedirect("menu.jsp");
		
	}

}
