package utils;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.testng.annotations.DataProvider;

import java.io.File;
import java.io.IOException;

public class TestDataUtils {

    @DataProvider(name = "validLoginData")
    public static Object[][] getValidLoginData() {
        return readJsonData("validLogins");
    }

    @DataProvider(name = "invalidLoginData")
    public static Object[][] getInvalidLoginData() {
        return readJsonData("invalidLogins");
    }

    private static Object[][] readJsonData(String dataArrayName) {
        // Read file path dynamically from config.properties
        String filePath = ConfigReader.getProperty("testdata.json.path");
        ObjectMapper mapper = new ObjectMapper();
        
        try {
            JsonNode rootNode = mapper.readTree(new File(filePath));
            JsonNode dataArray = rootNode.get(dataArrayName);
            
            if (dataArray == null || !dataArray.isArray()) {
                throw new RuntimeException("Could not find array '" + dataArrayName + "' in JSON file.");
            }
            
            Object[][] data = new Object[dataArray.size()][2];
            for (int i = 0; i < dataArray.size(); i++) {
                JsonNode node = dataArray.get(i);
                data[i][0] = node.get("username").asText();
                data[i][1] = node.get("password").asText();
            }
            
            return data;
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to read JSON test data from: " + filePath, e);
        }
    }
}
