# OpenCart Selenium Automation Framework

## Overview
This is an enterprise-grade Selenium WebDriver automation framework built for testing the OpenCart web application. It utilizes Java, Maven, TestNG, and adheres heavily to the Page Object Model (POM) design pattern to ensure maintainability, scalability, and clean code architecture.

## Tech Stack
- **Language**: Java
- **Build Tool**: Maven
- **Core Automation Engine**: Selenium WebDriver
- **Test Runner**: TestNG
- **Data Parsing**: Jackson Databind (JSON), Apache POI (Excel)

## Key Features
- **Page Object Model (POM)**: Strict separation of UI element definitions and test logics. Custom unchecked exceptions securely encapsulate failures natively without propagating structural checked `Exception` chaining into test cases.
- **Configurable Data Providers**: Implements TestNG's `@DataProvider` with support for both **JSON** and **Excel (.xlsx)** data sources. The active source is controlled by a single property (`testdata.source`) in `config.properties`. Defaults to **JSON** — any unrecognized or missing value automatically falls back to JSON.
- **External Framework Configurations**: A robust configurations approach utilizing `config.properties` ensures parameters like base URLs, test data paths, and data source type remain thoroughly segregated from compiled logic.

## Project Structure
```text
src/
├── main/java/
│   ├── factory/          # Core abstractions (DriverFactory for WebDriver management)
│   ├── pages/            # Page classes containing WebElements and interaction methods
│   └── utils/            # Shared utilities:
│       ├── ConfigReader.java          # Reads key-value pairs from config.properties
│       ├── TestDataUtils.java         # Configurable DataProvider (JSON / Excel routing)
│       ├── ExcelDataReader.java       # Generic Excel (.xlsx) reader using Apache POI
│       └── ExcelTestDataGenerator.java # One-time utility to generate testdata.xlsx
├── test/java/
│   └── tests/            # TestNG test scripts (ValidLoginTest, InvalidLoginTest)
└── test/resources/
    ├── config.properties  # Framework-level configuration (URLs, data source, paths)
    ├── testdata.json      # JSON test data (validLogins / invalidLogins arrays)
    └── testdata.xlsx      # Excel test data (ValidLogins / InvalidLogins sheets)
```

## Running the Tests
To execute all tests via Maven, open your terminal at the root path of the project and execute:

```bash
mvn clean test
```

## Configuration & Setup
1. **Configuring target URL**: Ensure the `url` property is pointing to your environment correctly within `src/test/resources/config.properties`.

2. **Switching Data Source**: Set the `testdata.source` property in `config.properties`:
   ```properties
   # Use JSON (default):
   testdata.source=json

   # Use Excel:
   testdata.source=excel
   ```
   > **Note:** Only `json` and `excel` are recognized values. Any other value (including typos) will automatically default to JSON.

3. **Handling JSON Data Sets**: To add additional datasets, append items into `src/test/resources/testdata.json` underneath the `validLogins` or `invalidLogins` arrays. The tests automatically iterate across newly provided user inputs.

4. **Handling Excel Data Sets**: Edit `src/test/resources/testdata.xlsx` directly. Each sheet (`ValidLogins`, `InvalidLogins`) must have a header row (`username`, `password`) followed by data rows. Sheet names are configurable in `config.properties`:
   ```properties
   testdata.excel.path=src/test/resources/testdata.xlsx
   testdata.excel.sheet.validLogins=ValidLogins
   testdata.excel.sheet.invalidLogins=InvalidLogins
   ```
