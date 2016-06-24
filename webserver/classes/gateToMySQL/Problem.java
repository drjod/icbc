package gateToMySQL;

import java.util.Arrays;
import java.util.List;



public class Problem {

	private String state;  // 1: active, 0 inactive
	
	private String flowProcess;
	private String lumpingFlow;

	private String heatFlag;
	private String massFlag;
    private String coupledFlag;	
    
    ProcessNumerics process = new ProcessNumerics();
    ProcessNumerics process1 = new ProcessNumerics();
    ProcessNumerics process2 = new ProcessNumerics();
	List<ProcessNumerics> processes = Arrays.asList(process, process1, process2);

	//private SolverKit solverKit;
	
	public Problem() {

		state = new String();
		
		flowProcess = new String();
		lumpingFlow = new String();
		
		heatFlag = new String();
		massFlag = new String();
		coupledFlag = new String();
		
		//solverKit = new SolverKit();
	}

	public String getState() {
		return state;
	}
	
	public String getFlowProcess() {
		return flowProcess;
	}
	
	public String getLumpingFlow() {
		return lumpingFlow;
	}
	
	public void setState(String value) {
		this.state = value;
	}

	public void setLumpingFlow(String value) {
		this.lumpingFlow = value;
	}

	public String getHeatFlag() {
		return heatFlag;
	}

	public String getMassFlag() {
		return massFlag;
	}
	
	public String getCoupledFlag() {
		return coupledFlag;
	}
	
	public List<ProcessNumerics> getProcesses() {
		return processes;
	}

	public void addToSolverList(String item_flow, String item_heat, String item_mass) {
		processes.get(0).addToSolverList(item_flow);
		processes.get(1).addToSolverList(item_heat);
		processes.get(2).addToSolverList(item_mass);		
	}

	public void addToPreconditionerList(String item_flow, String item_heat, String item_mass) {
		processes.get(0).addToPreconditionerList(item_flow);
		processes.get(1).addToPreconditionerList(item_heat);
		processes.get(2).addToPreconditionerList(item_mass);		
	}	
	
	//public SolverKit getSolverKit() {
	//	return solverKit;
	//}

	public void setValues(String stateItem, String flowProcessItem, String lumpingFlowItem, String heatFlagItem, String massFlagItem, String coupledFlagItem,
			String item_flow, String item_heat, String item_mass) {
		this.state = stateItem;
		this.flowProcess = flowProcessItem;
		this.lumpingFlow = lumpingFlowItem;
		this.heatFlag = heatFlagItem;
		this.massFlag = massFlagItem;	
		this.coupledFlag = coupledFlagItem;	
		
		processes.get(0).setTheta(item_flow);
		processes.get(1).setTheta(item_heat);
		processes.get(2).setTheta(item_mass);	
	}
	
	public void updateDatabase(DbManager database, SolverKit solverKit, String selectedConfiguration, String ndx) {
		
	    database.updateCheckbox( "state", state, ndx);
	    database.updateCheckbox( "lumping_flow", lumpingFlow, ndx);	
	    
	    database.updateTextField( "theta_flow", getProcesses().get(0).getTheta(), ndx); 
	    database.updateTextField( "theta_heat", getProcesses().get(1).getTheta(), ndx); 
	    database.updateTextField( "theta_mass", getProcesses().get(2).getTheta(), ndx); 
	    
	    database.updateTextField( "solver_flow_" + solverKit.configurationId2Name(selectedConfiguration), 
	    		getProcesses().get(0).getSolverList().get(Integer.parseInt(selectedConfiguration)), ndx); 
	    database.updateTextField( "solver_heat_" + solverKit.configurationId2Name(selectedConfiguration), 
	    		getProcesses().get(1).getSolverList().get(Integer.parseInt(selectedConfiguration)), ndx); 
	    database.updateTextField( "solver_mass_" + solverKit.configurationId2Name(selectedConfiguration), 
	    		getProcesses().get(2).getSolverList().get(Integer.parseInt(selectedConfiguration)), ndx); 
	    
	    database.updateTextField( "preconditioner_flow_" + solverKit.configurationId2Name(selectedConfiguration), 
	    		getProcesses().get(0).getPreconditionerList().get(Integer.parseInt(selectedConfiguration)), ndx); 
	    database.updateTextField( "preconditioner_heat_" + solverKit.configurationId2Name(selectedConfiguration), 
	    		getProcesses().get(1).getPreconditionerList().get(Integer.parseInt(selectedConfiguration)), ndx); 
	    database.updateTextField( "preconditioner_mass_" + solverKit.configurationId2Name(selectedConfiguration), 
	    		getProcesses().get(2).getPreconditionerList().get(Integer.parseInt(selectedConfiguration)), ndx); 
			
	}
	

}