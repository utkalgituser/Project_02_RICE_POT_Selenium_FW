package utils;

import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * One-time utility to generate the testdata.xlsx file.
 * Run this class once via its main method to create the Excel data file.
 * This class is NOT used during test execution.
 */
public class ExcelTestDataGenerator {

    public static void main(String[] args) {
        // Resolve path relative to project root, regardless of working directory
        Path projectRoot = resolveProjectRoot();
        String outputPath = projectRoot.resolve("src/test/resources/testdata.xlsx").toString();

        try (Workbook workbook = new XSSFWorkbook()) {

            // --- Sheet 1: ValidLogins ---
            Sheet validSheet = workbook.createSheet("ValidLogins");
            Row validHeader = validSheet.createRow(0);
            validHeader.createCell(0).setCellValue("username");
            validHeader.createCell(1).setCellValue("password");

            Row validRow1 = validSheet.createRow(1);
            validRow1.createCell(0).setCellValue("uvden8wx6@mozmail.com");
            validRow1.createCell(1).setCellValue("xyz@123");

            // --- Sheet 2: InvalidLogins ---
            Sheet invalidSheet = workbook.createSheet("InvalidLogins");
            Row invalidHeader = invalidSheet.createRow(0);
            invalidHeader.createCell(0).setCellValue("username");
            invalidHeader.createCell(1).setCellValue("password");

            Row invalidRow1 = invalidSheet.createRow(1);
            invalidRow1.createCell(0).setCellValue("invalid.user@opencart.com");
            invalidRow1.createCell(1).setCellValue("WrongPassword123");

            Row invalidRow2 = invalidSheet.createRow(2);
            invalidRow2.createCell(0).setCellValue("another.invalid@opencart.com");
            invalidRow2.createCell(1).setCellValue("password1234");

            // Write to file
            try (FileOutputStream fos = new FileOutputStream(outputPath)) {
                workbook.write(fos);
            }

            System.out.println("Excel test data file created successfully at: " + outputPath);

        } catch (IOException e) {
            throw new RuntimeException("Failed to generate Excel test data file.", e);
        }
    }

    /**
     * Walks up from the current working directory to find the project root
     * (identified by the presence of {@code pom.xml}).
     * Falls back to CWD if not found.
     */
    private static Path resolveProjectRoot() {
        Path current = Paths.get("").toAbsolutePath();
        Path check = current;
        while (check != null) {
            if (new File(check.toFile(), "pom.xml").exists()) {
                return check;
            }
            check = check.getParent();
        }
        // Fallback: assume CWD is the project root
        return current;
    }
}
