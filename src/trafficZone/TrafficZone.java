package trafficZone;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class TrafficZone {  
	private String regionCode;
	private String trafficZoneNumber;
	private String road = "True";
	private String railway = "True";
	private String river = "True";
	private String clusterType = "aggloEuc";
	private List<LatiLongitude> latiLongitudeList = new ArrayList<LatiLongitude>();
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

	    return latiLongitudeList;
	}

	public void setLatiLongitudeList(List<LatiLongitude> latiLongitudeList) {
	    this.latiLongitudeList = latiLongitudeList;
	}
	
	public String getClusterType() {
		return clusterType;
	}
	
	public void setClusterType(String clusterType) {
		this.clusterType = clusterType;
	}
	
	public List<LatiLongitude> computationsTrafficZone(String regionCode, int partitionNum, boolean road, boolean railway, boolean river) throws IOException{
    	/** 输入参数传给Parser，再通过Parser获取 Python 模块生成的经纬度对列表*/
		
		String[] regionCodeList = {"4","5","6","7","8","9","11","12","13","14","15","16","17","18","19","20","21","22","23"};
		if(!Arrays.asList(regionCodeList).contains(regionCode)){
			System.out.println("请输入正确的区域代码（4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23）");
			return latiLongitudeList;
		}
		if(partitionNum>500 || partitionNum <1){
			System.out.println("请输入正确的分区数量（0<partitionNum<500）");
			return latiLongitudeList;			
		}
		
		this.setRegionCode(regionCode);
    	this.setTrafficZoneNumber(Integer.toString(partitionNum));
		String head = new File(".").getCanonicalPath();
    	String tail = "\\TrafficZonePy\\py\\generate_partition.py";
    	String regCode = regionCode;
    	String partition = Integer.toString(partitionNum);
    	String roadFlag = (road==true)?"True":"False";
    	String railwayFlag = (railway==true)?"True":"False";
    	String riverFlag = (river==true)?"True":"False";
    	String cluster = this.clusterType;
    	
    	String lst = Parser.exeCmd("python "+head+tail+" "+regCode+" "+partition+" "+roadFlag+" "+railwayFlag+" "+riverFlag+" "+cluster);
    	lst = lst.replace("[","").replace("]", "");
    	String[] splt_lst = lst.split(",");
    	for(int i=0;i<(splt_lst.length)/2;i++) {
    		LatiLongitude coord = new LatiLongitude();
    		coord.setLongitude(Double.valueOf(splt_lst[i]));
    		coord.setLatitude(Double.valueOf(splt_lst[i+1]));
    		latiLongitudeList.add(coord);
    	}
    	this.setLatiLongitudeList(latiLongitudeList);

		return latiLongitudeList;
	}
	
}