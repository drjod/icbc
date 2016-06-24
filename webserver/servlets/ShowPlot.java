package servlets;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import gateToMySQL.SubjectsSetup;

/**
 * Servlet implementation class ShowPlot
 */
@WebServlet("/ShowPlot")
public class ShowPlot extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		String typeToPlot = request.getParameter("typeToPlot");
		System.out.println( typeToPlot );
		
		HttpSession session = request.getSession();
		SubjectsSetup subjects = (SubjectsSetup)session.getAttribute("subjects");
		
		String computer = subjects.getSelectedComputerInstance().getName();
		String code = subjects.getSelectedCode();
		String branch = subjects.getSelectedBranch();
				
		response.setContentType("image/jpeg");  
		ServletOutputStream out;  
		out = response.getOutputStream();  
		FileInputStream fin = new FileInputStream("f:\\testingEnvironment\\" + computer + "\\" + code + "\\" + branch + "\\examples\\plots\\results_" + typeToPlot + ".jpg");
		
		BufferedInputStream bin = new BufferedInputStream(fin);  
		BufferedOutputStream bout = new BufferedOutputStream(out);  
		int ch =0; ;  
		while((ch=bin.read())!=-1)  
		{  
		    bout.write(ch);  
		}  
		      
		bin.close();  
		fin.close();  
		bout.close();  
	    out.close();  	
	}


}
