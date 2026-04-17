# OpenCart Login Dashboard – Master Test Plan

## 1. Test Plan ID
**TP-OPENCART-LOGIN-001**  
**Version:** 1.0  
**Date:** April 17, 2026  
**Author:** QA Automation Lead

## 2. Introduction
This plan defines the **testing strategy** for OpenCart’s login module, covering **functional, performance, security, and accessibility** validations.

## 3. Objectives
- Validate **login, register, forgot password** flows.  
- Ensure **sub-2s page load** performance.  
- Confirm **OWASP compliance** (SQLi, XSS, brute force).  
- Guarantee **WCAG 2.1 AA accessibility**.

## 4. Scope
- **In Scope:** Login, Register, Forgot Password, Session Management.  
- **Out of Scope:** Post-login shopping cart, payment gateway.

## 5. Test Strategy
- **Functional Automation:** Selenium + TestNG.  
- **Performance:** JMeter load tests (1000 concurrent users).  
- **Security:** OWASP ZAP scans.  
- **Accessibility:** Axe + manual screen reader checks.

## 6. Test Environment
- Browsers: Chrome, Firefox, Safari, Edge.  
- Mobile: iOS Safari, Android Chrome.  
- Infrastructure: Staging mirror with isolated DB.

## 7. Test Data
- Valid/Invalid accounts.  
- Accounts with expired/locked states.  
- Injection payloads (`' OR 1=1`, `<script>alert(1)</script>`).  

## 8. Test Scenarios
| **Scenario ID** | **Description** | **Validation** |
|-----------------|-----------------|----------------|
| TS_01 | Valid Login | Redirect to dashboard |
| TS_02 | Invalid Login | Error message |
| TS_03 | Forgot Password | Reset email |
| TS_04 | Brute Force | Account lock |
| TS_05 | Accessibility | WCAG compliance |

## 9. Entry Criteria
- Code complete, deployed to staging.  
- Test data provisioned.  
- Automation framework initialized.

## 10. Exit Criteria
- 100% test execution.  
- ≥95% pass rate.  
- Zero Sev-1/Sev-2 defects.  
- Security scans clear.  
- Performance <2s validated.

## 11. Risk & Mitigation
| **Risk** | **Impact** | **Mitigation** |
|----------|------------|----------------|
| SSO downtime | High | Mock IdP responses |
| Performance degradation | High | CDN optimization |
| Security gaps | Critical | Shift-left OWASP scans |

## 12. Deliverables
- Master Test Plan  
- RTM  
- Automation Scripts  
- Performance & Security Reports  
- Final Sign-off Report
