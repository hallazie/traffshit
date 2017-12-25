package trafficZone;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Parser {  
    public static String exeCmd(String commandStr) {  
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