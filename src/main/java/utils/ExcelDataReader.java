package utils;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.DataFormatter;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.jspecify.annotations.NonNull;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Objects;

/**
 * Generic utility to read test data from Excel (.xlsx) files.
 * <p>
 * Reads a specified sheet from the workbook and returns all data rows
 * (excluding the header row) as a 2D Object array, ready for TestNG DataProvider consumption.
 * </p>
 */
public class ExcelDataReader {

    /**
     * Reads all data rows from a given sheet in an Excel workbook.
     *
     * @param filePath  absolute or relative path to the .xlsx file
     * @param sheetName the name of the sheet to read
     * @return a 2D Object array where each row is a set of test parameters
     * @throws RuntimeException if the file or sheet cannot be read
     */
    public static Object[][] readExcelData(@NonNull String filePath, @NonNull String sheetName) {
        Objects.requireNonNull(filePath, "filePath must not be null");
        Objects.requireNonNull(sheetName, "sheetName must not be null");

        try (FileInputStream fis = new FileInputStream(filePath);
             Workbook workbook = new XSSFWorkbook(fis)) {

            Sheet sheet = workbook.getSheet(sheetName);
            if (sheet == null) {
                throw new RuntimeException(
                        "Sheet '" + sheetName + "' not found in Excel file: " + filePath);
            }

            // getLastRowNum() returns the 0-based index of the last row — handles sparse/gapped sheets correctly.
            // getPhysicalNumberOfRows() only counts written rows and would undercount when blank rows exist mid-sheet.
            int lastRowNum = sheet.getLastRowNum();
            if (lastRowNum < 1) {
                throw new RuntimeException(
                        "Sheet '" + sheetName + "' has no data rows (only header or empty).");
            }

            // First row is treated as header — determine column count from it
            Row headerRow = sheet.getRow(0);
            if (headerRow == null) {
                throw new RuntimeException(
                        "Header row (row 0) is missing in sheet: '" + sheetName + "'");
            }
            int totalCols = headerRow.getPhysicalNumberOfCells();

            // Data rows: indices 1 through lastRowNum (inclusive) → lastRowNum total data rows
            Object[][] data = new Object[lastRowNum][totalCols];
            DataFormatter formatter = new DataFormatter();

            for (int i = 1; i <= lastRowNum; i++) {
                Row row = sheet.getRow(i);
                for (int j = 0; j < totalCols; j++) {
                    Cell cell = (row != null) ? row.getCell(j) : null;
                    data[i - 1][j] = getCellValue(cell, formatter);
                }
            }

            return data;

        } catch (IOException e) {
            throw new RuntimeException(
                    "Failed to read Excel test data from: " + filePath, e);
        }
    }

    /**
     * Extracts the cell value as a String regardless of the cell's actual type.
     * Numeric cells are formatted to avoid trailing ".0" for whole numbers.
     *
     * @param cell      the Excel cell (may be null)
     * @param formatter a reusable DataFormatter instance
     * @return the cell value as a trimmed String, or empty string if null
     */
    private static @NonNull String getCellValue(Cell cell, @NonNull DataFormatter formatter) {
        if (cell == null) {
            return "";
        }

        return Objects.requireNonNull(formatter.formatCellValue(cell).trim());
    }
}
