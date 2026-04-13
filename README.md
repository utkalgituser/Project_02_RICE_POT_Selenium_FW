# OpenCart Selenium Automation Framework

## Overview
This is an enterprise-grade Selenium WebDriver automation framework built for testing the OpenCart web application. It utilizes Java, Maven, TestNG, and adheres heavily to the Page Object Model (POM) design pattern to ensure maintainability, scalability, and clean code architecture.

## Tech Stack
- **Language**: Java
- **Build Tool**: Maven
- **Core Automation Engine**: Selenium WebDriver
- **Test Runner**: TestNG
- **Data Parsing**: Jackson Databind (JSON)

## Key Features
- **Page Object Model (POM)**: Strict separation of UI element definitions and test logics. Custom unchecked exceptions securely encapsulate failures natively without propagating structural checked `Exception` chaining into test cases.
- **Dynamic JSON Data Providers**: Implements TestNG's `@DataProvider` combined with Jackson to read test execution data externally from JSON files (`src/test/resources/testdata.json`). No users or IDs are hardcoded!
- **External Framework Configurations**: A robust configurations approach utilizing `config.properties` ensures parameters like base URLs or test data paths remain thoroughly segregated from compiled logic.

## Project Structure
```text
src/
├── main/java/
│   ├── factory/          # Core abstractions (DriverFactory for Webdriver management)
│   ├── pages/            # Page classes containing WebElements and interaction methods (OpenCartLoginPage, OpenCartMyAccountPage)
│   └── utils/            # Shared utilities (ConfigReader, JSON TestDataUtils)
├── test/java/
│   └── tests/            # TestNG test scripts validating page functionality (ValidLoginTest, InvalidLoginTest)
└── test/resources/
    ├── config.properties # Contains framework level keys/values linking URL paths and configurations
    └── testdata.json     # JSON payload array structuring data-driven validation tests
```

## Running the Tests
To execute all tests via Maven, open your terminal at the root path of the project and execute:

```bash
mvn clean test
```

## Configuration & Setup
1. **Configuring target URL**: Ensure the `url` property is pointing to your environment correctly within `src/test/resources/config.properties`.
2. **Handling Data Sets**: To add additional datasets for parameterized assertions, append items into `src/test/resources/testdata.json` underneath the `validLogins` or `invalidLogins` arrays. The tests automatically iterate across newly provided user inputs.
