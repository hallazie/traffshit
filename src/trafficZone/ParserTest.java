package trafficZone;

import java.io.File;
import java.io.IOException;

import org.junit.Test;

public class ParserTest {
	/* 测试Parser是否正常解析 */
	@Test
	public void testExeCmd() {
		String head = null;
		try {
			head = new File(".").getCanonicalPath();
		} catch (IOException e) {
			e.printStackTrace();
		}
    	String tail = "\\TrafficZonePy\\py\\unit_test.py";
    	String res = Parser.exeCmd("python "+head+tail);
    	assert(res.substring(0, 12).equals("hello world!"));
	}
	
}
