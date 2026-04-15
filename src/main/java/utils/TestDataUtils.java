package utils;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.testng.annotations.DataProvider;

import java.io.File;
import java.io.IOException;

/**
 * Centralized TestNG DataProvider class.
 * <p>
 * Supports both <b>JSON</b> and <b>Excel</b> data sources, configurable
 * through {@code config.properties} via the key {@code testdata.source}.
 * </p>
 *
 * <h3>Configuration keys used:</h3>
 * <ul>
 *   <li>{@code testdata.source} — {@code json} or {@code excel} (default: json)</li>
 *   <li>{@code testdata.json.path} — path to the JSON file</li>
 *   <li>{@code testdata.excel.path} — path to the Excel (.xlsx) file</li>
 *   <li>{@code testdata.excel.sheet.validLogins} — sheet name for valid login data</li>
 *   <li>{@code testdata.excel.sheet.invalidLogins} — sheet name for invalid login data</li>
 * </ul>
 */
public class TestDataUtils {

    private static final String SOURCE_JSON = "json";
    private static final String SOURCE_EXCEL = "excel";

    @DataProvider(name = "validLoginData")
    public static Object[][] getValidLoginData() {
        String source = getDataSource();
        if (SOURCE_EXCEL.equalsIgnoreCase(source)) {
            String filePath = ConfigReader.getProperty("testdata.excel.path");
            String sheetName = ConfigReader.getProperty("testdata.excel.sheet.validLogins");
            return ExcelDataReader.readExcelData(filePath, sheetName);
        }
        return readJsonData("validLogins");
    }

    @DataProvider(name = "invalidLoginData")
    public static Object[][] getInvalidLoginData() {
        String source = getDataSource();
        if (SOURCE_EXCEL.equalsIgnoreCase(source)) {
            String filePath = ConfigReader.getProperty("testdata.excel.path");
            String sheetName = ConfigReader.getProperty("testdata.excel.sheet.invalidLogins");
            return ExcelDataReader.readExcelData(filePath, sheetName);
        }
        return readJsonData("invalidLogins");
    }

    /**
     * Resolves the active data source from config.
     * Only {@code "json"} and {@code "excel"} are valid values.
     * Any unrecognized, missing, or blank value defaults to {@code "json"}.
     */
    private static String getDataSource() {
        String source = ConfigReader.getProperty("testdata.source", SOURCE_JSON);
        if (SOURCE_EXCEL.equalsIgnoreCase(source.trim())) {
            return SOURCE_EXCEL;
        }
        return SOURCE_JSON;
    }

    /**
     * Reads test data from a JSON file.
     *
     * @param dataArrayName the JSON array key (e.g. "validLogins", "invalidLogins")
     * @return 2D Object array for TestNG DataProvider
     */
    private static Object[][] readJsonData(String dataArrayName) {
        String filePath = ConfigReader.getProperty("testdata.json.path");
        ObjectMapper mapper = new ObjectMapper();

        try {
            JsonNode rootNode = mapper.readTree(new File(filePath));
            JsonNode dataArray = rootNode.get(dataArrayName);

            if (dataArray == null || !dataArray.isArray()) {
                throw new RuntimeException(
                        "Could not find array '" + dataArrayName + "' in JSON file.");
            }

            Object[][] data = new Object[dataArray.size()][2];
            for (int i = 0; i < dataArray.size(); i++) {
                JsonNode node = dataArray.get(i);
                data[i][0] = node.get("username").asText();
                data[i][1] = node.get("password").asText();
            }

            return data;
        } catch (IOException e) {
            throw new RuntimeException(
                    "Failed to read JSON test data from: " + filePath, e);
        }
    }
}
