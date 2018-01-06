package trafficZone;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Parser {
	/**  解析调用算法的 Python 接口 */
    public static String exeCmd(String commandStr) {
    	/** 命令行执行函数，获取 Python 的执行结果 */
        BufferedReader br = null;  
        try {
            Process p = Runtime.getRuntime().exec(commandStr);  
            br = new BufferedReader(new InputStreamReader(p.getInputStream()));  
            String line = null;  
            StringBuilder sb = new StringBuilder();  
            while ((line = br.readLine()) != null) {  
                sb.append(line + "\n");  
            }  
            return sb.toString();
        } catch (Exception e) {  
            e.printStackTrace();
            return "0";
        }   
        finally  
        {  
            if (br != null)  
            {  
                try {  
                    br.close();  
                } catch (Exception e) {  
                    e.printStackTrace();  
                }  
            }  
        }  
    }
    
    public static void main(String[] args) throws IOException { 
    	System.out.println("None");
    }  
}