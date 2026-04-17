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
scripts/
└── generate_test_plan.py  # Python script — generates the DOCX test plan
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

---

# Test Plan Generator — OpenCart Login Module

> Enterprise-grade test documentation suite for the OpenCart authentication module, built on the **RICEPOT** prompt-engineering framework.

---

## What This Project Does

This project produces a fully structured, enterprise-quality test plan for the OpenCart Login, Registration, Forgot Password, and Session Management flows. It covers:

- Functional & regression test cases (45 scenarios)
- Security testing — OWASP Top 10 (SQLi, XSS, CSRF, brute force)
- Performance testing — JMeter load profiles (1000 concurrent users)
- Accessibility testing — WCAG 2.1 AA compliance
- Cross-browser / cross-device compatibility matrix

---

## Project Structure

```
├── scripts/
│   └── generate_test_plan.py          # Python script — generates the DOCX test plan
├── TEST_PLAN_OpenCart_Login.docx      # Enterprise master test plan (generated output)
├── RICEPOT.md                         # RICEPOT prompt-engineering framework guide
└── README.md                          # This file
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- `python-docx` library

```bash
pip install python-docx
```

### Generate the Test Plan

```bash
cd Project_02_RICE_POT_Selenium_FW
python scripts/generate_test_plan.py
```

Output: `TEST_PLAN_OpenCart_Login.docx` in the project root.

---

## Deliverables

| # | File | Format | Description |
|---|---|---|---|
| D-01 | `TEST_PLAN_OpenCart_Login.docx` | DOCX | Enterprise master test plan — all sections |
| D-02 | `RICEPOT.md` | Markdown | RICEPOT framework reference |
| D-03 | `scripts/generate_test_plan.py` | Python | Automation script for DOCX generation |

---

## Test Plan Sections at a Glance

| Section | Content |
|---|---|
| Document Control | Version history, distribution list, approvals |
| Executive Summary | Scope, AUT details, testing initiative overview |
| Business Objectives | 6 measurable objectives with success metrics |
| Scope | In/out of scope, assumptions, dependencies |
| Test Strategy | 5 test levels, 7 test types, automation strategy |
| Test Environment | Browser/OS matrix, infrastructure, CI/CD setup |
| Test Data Management | Account categories, security payloads, GDPR governance |
| Test Cases | 45 test cases across Login, Register, Forgot Password, Session, Accessibility |
| Entry & Exit Criteria | 6 entry gates, 8 exit gates |
| Defect Management | Severity SLAs, lifecycle, mandatory JIRA fields |
| Risk Register | 8 risks with probability, impact, and mitigation |
| RACI Matrix | Roles across QA, Dev, Security, DevOps, Product |
| Schedule | 10 milestones from April 17 – May 12, 2026 |
| Tools | 14 tools catalogued (Selenium, JMeter, ZAP, Axe, BrowserStack) |
| Deliverables | 10 deliverables with owners and due dates |
| Sign-off | Approval block for VP sign-off |

---

## Application Under Test

| Detail | Value |
|---|---|
| Application | OpenCart Demo |
| Login URL | `https://naveenautomationlabs.com/opencart/index.php?route=account/login` |
| Auth Type | Session-based, cookie-driven |
| Key Endpoints | `/account/login`, `/account/register`, `/account/forgotten` |

---

## Framework

This project uses the **RICEPOT** prompt-engineering framework to generate comprehensive test coverage:

| Letter | Stands For | Purpose |
|---|---|---|
| R | Role | Define the QA persona (e.g., Architect, 15+ YOE) |
| I | Instructions | Specify what to analyse and generate |
| C | Context | Application details, endpoints, auth mechanism |
| E | Expected Output | Table format — TC_ID, Scenario_ID, Endpoint, etc. |
| P | Persona | Meticulous, enterprise-focused, compliance-ready |
| O | Output Format | DOCX for formal delivery; Markdown for traceability |
| T | Tone | Formal, technical, compliance-ready |

See [RICEPOT.md](RICEPOT.md) for the full framework reference.

---

## Reusing This for Other Projects

1. Update the AUT details in `scripts/generate_test_plan.py` (URL, endpoints, module names).
2. Replace the test case rows in sections 7.1–7.5 with your new scenarios.
3. Update the RACI matrix, schedule, and deliverables sections.
4. Run `python scripts/generate_test_plan.py` to regenerate the DOCX.

See [RICEPOT.md](RICEPOT.md) for how to re-prompt an LLM to generate new test cases for a different module.
