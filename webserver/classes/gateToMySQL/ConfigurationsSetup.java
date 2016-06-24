package gateToMySQL;

import java.util.ArrayList;
import java.util.HashMap;

public class ConfigurationsSetup {
	
	HashMap<Integer,String> configurationsTable;
	
	public ConfigurationsSetup() {}
	
	public void defineConfigurationsTable(ArrayList<String> configurationsList) {
		
		configurationsTable = new HashMap<Integer,String>();
		
		for(Integer i = 0; i < configurationsList.size(); i++ ) 
			configurationsTable.put(i, configurationsList.get(i));		
	}
		
	public HashMap<Integer, String> getConfigurationsTable() {
		return configurationsTable;
	}
	
}
