package gateToMySQL;

import java.util.ArrayList;

import com.sun.xml.internal.bind.v2.schemagen.xmlschema.List;

public class ProcessNumerics {
	
	private String theta;
	private ArrayList<String> solverList;      // depend on configuration
	private ArrayList<String>  preconditionerList;

	public ProcessNumerics() {
		solverList = new ArrayList<String>(); 
		preconditionerList = new ArrayList<String>(); 
	}
	
	public ArrayList<String> getSolverList() {
		return solverList;
	}
	
	public ArrayList<String> getPreconditionerList() {
		return preconditionerList;
	}
	
	public String getTheta() {
		return theta;
	}

	public void setTheta(String theta) {
		this.theta = theta;
	}

	public void addToSolverList(String item) {
		solverList.add(item);
	}

	public void addToPreconditionerList(String item) {
		preconditionerList.add(item);
	}

	public void setSolver(int ndx, String value) {
		this.solverList.set(ndx, value);
	}

	public void setPreconditioner(int ndx, String value) {
		this.preconditionerList.set(ndx, value);
	}
	
	public String getSolver(int ndx) {
		return this.solverList.get(ndx);
	}

	public String getPreconditioner(int ndx) {
		return this.preconditionerList.get(ndx);
	}

}
