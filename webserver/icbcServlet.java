package icbcServlet;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;


/**
 * Servlet implementation class DisplayImage
 */
@WebServlet(description = "post tecplot jpg", urlPatterns = { "/DisplayImage" })
public class icbcServlet extends HttpServlet {
	
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

		String code = request.getParameter("code");
		String branch = request.getParameter("branch");
		String example = request.getParameter("example");
		String computer = request.getParameter("computer");
		
		response.setContentType("image/jpeg");  
		ServletOutputStream out;  
		out = response.getOutputStream();  
		FileInputStream fin = new FileInputStream("f:\\testingEnvironment\\" + computer + "\\" + code + "\\" + branch + "\\examples\\plots\\results_" + example + ".jpg");
		
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
