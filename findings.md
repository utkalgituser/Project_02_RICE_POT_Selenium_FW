# Findings

## Research
- The application will be a Node.js/TypeScript backend with a React frontend.
- It needs to connect to multiple LLM APIs: Ollama, LM Studio, Grok, OpenAI, Claude, and Gemini.

## Discoveries
- Core Purpose: Generate API and web app test cases (both functional and non-functional) based on Jira requirements.
- Input Modality: Users will input Jira requirements via copy-paste into a chat/text interface.
- Output Modality: The tool will generate and format test cases in Jira format. 

## Constraints
- The UI must have a Settings window to configure the different LLM APIs.
- Must halt execution until Blueprint is approved (Protocol 0).

## OpenCart Feature: JSON Data Provider & Exception Handling
- **Objective:** Convert hardcoded credentials into a dynamic JSON-driven Data Provider, implement POM assertions, and eliminate boilerplate checked exception propagation.
- **Files Modified / Created** (in `feature/data-provider` branch):
  - `pom.xml`: Added `jackson-databind` dependency for JSON parsing.
  - `src/test/resources/config.properties`: Added dynamic path property `testdata.json.path`.
  - `src/test/resources/testdata.json`: Created to hold structured test credentials.
  - `src/main/java/utils/TestDataUtils.java`: Created to parse JSON into TestNG's `@DataProvider`.
  - `src/main/java/pages/OpenCartLoginPage.java`: Swapped `throws Exception` for unchecked `RuntimeException`, modified `doLogin` to return `OpenCartMyAccountPage`.
  - `src/main/java/pages/OpenCartMyAccountPage.java`: Created POM class mapped to "My Account" specific WebElements for validation.
  - `src/test/java/tests/ValidLoginTest.java`: Hooked up the JSON DataProvider, stripped checked exceptions, and updated assertion logic to utilize `OpenCartMyAccountPage`.
  - `src/test/java/tests/InvalidLoginTest.java`: Hooked up the JSON DataProvider and stripped checked exceptions.
  - `README.md`: Produced comprehensive framework documentation.

## GitHub Community Standards
- **Objective:** Introduce structured contribution guidelines and pull request templates.
- **Files Added:**
  - `CONTRIBUTING.md`: Base guidelines for open-source and team contributions.
  - `.github/ISSUE_TEMPLATE/ISSUE_TEMPLATE.md`: Standardized bug and feature requests.
  - `.github/PULL_REQUEST_TEMPLATE.md`: Template for PR motivation and changes.
  - `.github/REVIEWER_CHECKLIST.md`: Verification checklist for PR reviewers.

## OpenCart Feature: Reporting & Advanced Setup
- **Objective:** Introduce Allure Reporting frameworks, replace PageFactory (`@FindBy`) with standard `By` locators for Page classes, encapsulate explicit waits in a dedicated utility, and handle test data securely using Base64 decode execution and masked logging.
- **Files Modified / Created:**
  - `pom.xml`: Integrated `allure-testng` dependency and updated `maven-surefire-plugin` with `aspectjweaver`.
  - `src/main/java/utils/AppConstants.java`: Centralized application constants such as timeout lengths and page titles.
  - `src/main/java/utils/ElementUtil.java`: Built a wrapper encapsulating custom explicit waits around `By` locators for safe driver interactions.
  - `src/main/java/pages/OpenCartLoginPage.java`: Transitioned to `By` bindings. Implemented `decodeData(String)` Base64 decryption for sensitive strings, and `maskEmail(String)` for secure logging reports. Javadoc documentation generated.
  - `src/main/java/pages/OpenCartMyAccountPage.java`: Transitioned to `By` bindings utilizing `ElementUtil`. Javadoc documentation generated.
