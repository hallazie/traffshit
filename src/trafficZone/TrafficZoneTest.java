package trafficZone;

import java.io.IOException;
import java.util.List;

import org.junit.Test;

public class TrafficZoneTest {

	@Test
	public void testGetRegionCode() {
		TrafficZone testZone = new TrafficZone();
		testZone.setRegionCode("10");
		String res = testZone.getRegionCode();
		assert(res.equals("10"));
	}

	@Test
	public void testSetRegionCode() {
		TrafficZone testZone = new TrafficZone();
		testZone.setRegionCode("10");
		String res = testZone.getRegionCode();
		assert(res.equals("10"));
	}

	@Test
	public void testComputationsTrafficZone() {
		TrafficZone testZone = new TrafficZone();
		List<LatiLongitude> latiLongitudeList = null;
		try {
			latiLongitudeList = testZone.computationsTrafficZone("1000", 10, true, true, true);
		} catch (IOException e) {
			latiLongitudeList = null;
		}
		assert(latiLongitudeList.size()==0);
	}
}
