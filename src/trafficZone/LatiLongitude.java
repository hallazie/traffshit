package trafficZone;

public class LatiLongitude {
	private double latitude;
	private double longitude;

	public LatiLongitude() {
	}

	public LatiLongitude(double latitude, double longitude) {
	    this.latitude = latitude;
	    this.longitude = longitude;
	}

	public double getLatitude() {
	    return latitude;
	}

	public void setLatitude(double latitude) {
	    this.latitude = latitude;
	}

	public double getLongitude() {
	    return longitude;
	}

	public void setLongitude(double longitude) {
	    this.longitude = longitude;
	}

}
