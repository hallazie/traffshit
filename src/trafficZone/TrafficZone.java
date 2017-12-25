package trafficZone;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class TrafficZone {  
	private String regionCode;
	private String trafficZoneNumber;
	private String road = "True";
	private String railway = "True";
	private String river = "True";
	private List<LatiLongitude> latiLongitudeList;
	public TrafficZone() {
	}
	public TrafficZone(String regionCode, String trafficZoneNumber, List<LatiLongitude> latiLongitudeList) {
	    this.regionCode = regionCode;
	    this.trafficZoneNumber = trafficZoneNumber;
	    this.latiLongitudeList = latiLongitudeList;
	}
	public String getRegionCode() {
	    return regionCode;
	}

	public void setRegionCode(String regionCode) {
	    this.regionCode = regionCode;
	}

	public String getTrafficZoneNumber() {
	    return trafficZoneNumber;
	}

	public void setTrafficZoneNumber(String trafficZoneNumber) {
	    this.trafficZoneNumber = trafficZoneNumber;
	}
	
	public String getRoadFlag() {
	    return road;
	}

	public void setRoadFlag(String road) {
	    this.road = road;
	}
	
	public String getRailwayFlag() {
	    return railway;
	}

	public void setRailwayFlag(String railway) {
	    this.railway = railway;
	}

	public String getRiverFlag() {
	    return river;
	}

	public void setRiverFlag(String river) {
	    this.river = river;
	}

	public List<LatiLongitude> getLatiLongitudeList() throws IOException {

    	String head = new File(".").getCanonicalPath();
    	String tail = "\\TrafficZonePy\\py\\generate_partition.py";
    	String regCode = this.regionCode;
    	String partition = this.trafficZoneNumber;
    	String road = this.road;
    	String railway = this.railway;
    	String river = this.river;
    	
    	String lst = Parser.exeCmd("python "+head+tail+" "+regCode+" "+partition+" "+road+" "+railway+" "+river);
    	
    	lst = lst.replace("[","").replace("]", "");
    	String[] splt_lst = lst.split(",");
    	for(int i=0;i<(splt_lst.length)/2;i++) {
    		LatiLongitude coord = new LatiLongitude();
    		coord.setLongitude(Double.valueOf(splt_lst[i]));
    		coord.setLatitude(Double.valueOf(splt_lst[i+1]));
    		latiLongitudeList.add(coord);
    	}	
	    return latiLongitudeList;
	}

	public void setLatiLongitudeList(List<LatiLongitude> latiLongitudeList) {
	    this.latiLongitudeList = latiLongitudeList;
	}


}