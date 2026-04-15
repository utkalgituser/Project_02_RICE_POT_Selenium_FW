# OpenCart Selenium Automation Framework

## Overview
This is an enterprise-grade Selenium WebDriver automation framework built for testing the OpenCart web application. It utilizes Java, Maven, TestNG, and adheres heavily to the Page Object Model (POM) design pattern to ensure maintainability, scalability, and clean code architecture.

## Tech Stack
- **Language**: Java
- **Build Tool**: Maven
- **Core Automation Engine**: Selenium WebDriver
- **Test Runner**: TestNG
- **Data Parsing**: Jackson Databind (JSON)
- **Reporting**: Allure Framework

## Key Features
- **Page Object Model (POM)**: Strict separation of UI element definitions and test logics. Custom unchecked exceptions securely encapsulate failures natively without propagating structural checked `Exception` chaining into test cases.
- **Dynamic JSON Data Providers**: Implements TestNG's `@DataProvider` combined with Jackson to read test execution data externally from JSON files (`src/test/resources/testdata.json`). No users or IDs are hardcoded!
- **Element interactions Strategy**: Explicit Wait wrappers using localized `ElementUtil` coupled natively with `By` locators instead of standard `@FindBy` implementations. This isolates WebDriver dependency issues and unifies interaction timeouts set in `AppConstants`.
- **Sensitive Log Masking**: Includes Base64 data decoding mechanism seamlessly coupled with data masking (`test***@email.com`) when transferring configuration datasets (credentials) to prevent report or logging linkage leaks.
- **Reporting**: Interactive test dashboards generation powered by Allure representations securely attaching directly to TestNG events dynamically through `aspectjweaver`.
- **External Framework Configurations**: A robust configurations approach utilizing `config.properties` ensures parameters like base URLs or test data paths remain thoroughly segregated from compiled logic.

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

Optionally, you can generate and visualize your detailed tests run locally using the Allure server metrics (Ensure the Allure CLI is installed locally):
```bash
allure serve allure-results
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
