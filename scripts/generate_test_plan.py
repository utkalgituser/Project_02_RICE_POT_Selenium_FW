"""
Enterprise Test Plan Generator — OpenCart Login Module
Generates a fully formatted DOCX test plan using python-docx.
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BLUE   = RGBColor(0x1F, 0x35, 0x64)   # heading / table header
MID_BLUE    = RGBColor(0x2E, 0x74, 0xB5)   # sub-heading accent
LIGHT_BLUE  = RGBColor(0xD6, 0xE4, 0xF0)   # table header fill
ALT_ROW     = RGBColor(0xF2, 0xF7, 0xFB)   # alternating row fill
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
BLACK       = RGBColor(0x00, 0x00, 0x00)
DARK_GREY   = RGBColor(0x40, 0x40, 0x40)


# ── Helpers ──────────────────────────────────────────────────────────────────

def set_cell_bg(cell, rgb: RGBColor):
    """Apply a solid background colour to a table cell."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    hex_color = str(rgb)  # RGBColor.__str__ returns 6-char hex e.g. "1F3564"
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_cell_border(cell, **kwargs):
    """Add borders to a single cell. kwargs: top, bottom, left, right."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        border = OxmlElement(f"w:{side}")
        border.set(qn("w:val"), kwargs.get(side, "single"))
        border.set(qn("w:sz"), "4")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), "2E74B5")
        tcBorders.append(border)
    tcPr.append(tcBorders)


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    run = p.runs[0] if p.runs else p.add_run(text)
    run.font.color.rgb = DARK_BLUE if level == 1 else MID_BLUE
    run.font.bold = True
    run.font.size = Pt(16 if level == 1 else 13 if level == 2 else 11)
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after  = Pt(4)
    return p


def add_paragraph(doc, text, bold=False, italic=False, size=10, color=DARK_GREY, indent=0):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.space_after = Pt(4)
    return p


def add_table(doc, headers, rows, col_widths=None):
    """Add a styled table with header row and alternating row colours."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    # Header row
    hdr_row = table.rows[0]
    for i, hdr in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(hdr)
        run.font.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = WHITE
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_bg(cell, DARK_BLUE)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Data rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        bg = ALT_ROW if r_idx % 2 == 0 else WHITE
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = ""
            run = cell.paragraphs[0].add_run(str(val))
            run.font.size = Pt(9)
            run.font.color.rgb = DARK_GREY
            set_cell_bg(cell, bg)

    # Column widths
    if col_widths:
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                if i < len(col_widths):
                    cell.width = Inches(col_widths[i])

    doc.add_paragraph()  # spacer
    return table


def add_divider(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "2E74B5")
    pBdr.append(bottom)
    pPr.append(pBdr)


# ── Document Bootstrap ────────────────────────────────────────────────────────

doc = Document()

# Page margins
section = doc.sections[0]
section.left_margin   = Cm(2.54)
section.right_margin  = Cm(2.54)
section.top_margin    = Cm(2.54)
section.bottom_margin = Cm(2.54)

# Default body font
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(10)


# ── Cover Page ────────────────────────────────────────────────────────────────

doc.add_paragraph()
doc.add_paragraph()

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title_p.add_run("ENTERPRISE MASTER TEST PLAN")
run.font.size = Pt(26)
run.font.bold = True
run.font.color.rgb = DARK_BLUE

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = sub_p.add_run("OpenCart Login Module — Authentication & Security")
run2.font.size = Pt(14)
run2.font.italic = True
run2.font.color.rgb = MID_BLUE

doc.add_paragraph()

meta = [
    ("Document ID",  "TP-OPENCART-LOGIN-001"),
    ("Version",      "2.0"),
    ("Status",       "APPROVED"),
    ("Created",      "April 17, 2026"),
    ("Author",       "QA Automation Architect"),
    ("Reviewed By",  "Engineering Lead, Security Lead, Product Owner"),
    ("Approved By",  "VP Engineering"),
    ("Next Review",  "July 17, 2026"),
]
meta_table = doc.add_table(rows=len(meta), cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (k, v) in enumerate(meta):
    r = meta_table.rows[i]
    c0 = r.cells[0]; c1 = r.cells[1]
    c0.text = ""; c1.text = ""
    rk = c0.paragraphs[0].add_run(k)
    rk.font.bold = True; rk.font.size = Pt(10); rk.font.color.rgb = DARK_BLUE
    rv = c1.paragraphs[0].add_run(v)
    rv.font.size = Pt(10); rv.font.color.rgb = DARK_GREY
    set_cell_bg(c0, LIGHT_BLUE)
    c0.width = Inches(2.2); c1.width = Inches(3.8)

doc.add_page_break()


# ── Version History ───────────────────────────────────────────────────────────

add_heading(doc, "Document Control", level=1)
add_heading(doc, "Version History", level=2)
add_table(doc,
    headers=["Version", "Date", "Author", "Summary of Changes"],
    rows=[
        ["1.0", "April 17, 2026", "QA Lead", "Initial draft"],
        ["2.0", "April 17, 2026", "QA Architect", "Enterprise expansion — security, performance, accessibility, full RTM"],
    ],
    col_widths=[0.8, 1.4, 1.5, 4.3]
)

add_heading(doc, "Distribution List", level=2)
add_table(doc,
    headers=["Name / Role", "Department", "Access Level"],
    rows=[
        ["QA Automation Team",  "Quality Assurance",  "Full Read/Write"],
        ["Development Team",    "Engineering",         "Read"],
        ["Product Owner",       "Product Management",  "Read"],
        ["Security Team",       "InfoSec",             "Full Read/Write"],
        ["DevOps / CI-CD",      "Infrastructure",      "Read"],
        ["Compliance Officer",  "Legal/Compliance",    "Read"],
    ],
    col_widths=[2.5, 2.5, 2.5]
)
add_divider(doc)


# ── 1. Executive Summary ──────────────────────────────────────────────────────

add_heading(doc, "1. Executive Summary", level=1)
add_paragraph(doc,
    "This document defines the Enterprise Master Test Plan for the OpenCart Login Module, "
    "covering the complete authentication surface — Login, Registration, Forgot Password, and Session Management. "
    "The plan is aligned with ISTQB standards, OWASP Top 10, and WCAG 2.1 AA compliance requirements.",
    size=10
)
add_paragraph(doc,
    "The testing initiative spans functional, regression, integration, performance, security, and accessibility "
    "test types, executed across a multi-browser, multi-device environment using an automated-first strategy "
    "with manual validation for exploratory and accessibility coverage.",
    size=10
)
add_paragraph(doc, "Application Under Test:", bold=True, size=10)
add_paragraph(doc, "URL: https://naveenautomationlabs.com/opencart/index.php?route=account/login", size=10, indent=0.3)
add_paragraph(doc, "Modules: /account/login  |  /account/register  |  /account/forgotten", size=10, indent=0.3)
add_divider(doc)


# ── 2. Business Objectives ────────────────────────────────────────────────────

add_heading(doc, "2. Business Objectives", level=1)
add_table(doc,
    headers=["#", "Objective", "Success Metric"],
    rows=[
        ["BO-01", "Ensure all authentication flows function correctly",          "100% pass rate on critical paths"],
        ["BO-02", "Protect users from credential attacks and injection",          "Zero Sev-1 security findings post-release"],
        ["BO-03", "Deliver sub-2s page load under peak load",                    "P95 response time < 2000ms at 1000 concurrent users"],
        ["BO-04", "Comply with WCAG 2.1 AA accessibility standards",             "Zero critical accessibility violations"],
        ["BO-05", "Ensure cross-browser and cross-device parity",                "Consistent behaviour across all tier-1 browsers/devices"],
        ["BO-06", "Enable repeatable, CI-integrated regression coverage",        "100% automation of regression suite"],
    ],
    col_widths=[0.7, 3.8, 3.5]
)
add_divider(doc)


# ── 3. Scope ──────────────────────────────────────────────────────────────────

add_heading(doc, "3. Scope", level=1)
add_heading(doc, "3.1  In Scope", level=2)
add_table(doc,
    headers=["Module", "Features Covered"],
    rows=[
        ["Login",               "Valid login, invalid credentials, empty fields, remember me, redirect post-login"],
        ["Registration",        "New account creation, duplicate email, field validation, password rules"],
        ["Forgot Password",     "Email submission, reset link delivery, expired link, invalid email"],
        ["Session Management",  "Session expiry, concurrent sessions, cookie handling, logout"],
        ["Security",            "SQLi, XSS, CSRF, brute force, account lockout, HTTPS enforcement"],
        ["Performance",         "Load, stress, spike, and soak testing on auth endpoints"],
        ["Accessibility",       "WCAG 2.1 AA — keyboard navigation, ARIA labels, contrast, screen reader"],
        ["API / Network",       "HTTP status codes, response headers, cookie attributes, redirect chains"],
    ],
    col_widths=[2.0, 6.0]
)

add_heading(doc, "3.2  Out of Scope", level=2)
for item in [
    "Post-login shopping cart and product catalog workflows",
    "Payment gateway and checkout flows",
    "Admin panel authentication",
    "Third-party OAuth / SSO integrations (deferred to TP-002)",
    "Database-level migration testing",
]:
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(item)
    run.font.size = Pt(10)
    run.font.color.rgb = DARK_GREY

doc.add_paragraph()

add_heading(doc, "3.3  Assumptions", level=2)
for item in [
    "Staging environment is a production mirror with anonymized data",
    "Test data accounts are pre-provisioned by the DevOps team",
    "OWASP ZAP is licensed and configured in the CI pipeline",
    "No feature flags affect the login module during test execution",
]:
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(item)
    run.font.size = Pt(10)
    run.font.color.rgb = DARK_GREY

doc.add_paragraph()

add_heading(doc, "3.4  Dependencies", level=2)
add_table(doc,
    headers=["Dependency", "Owner", "Required By"],
    rows=[
        ["Staging environment availability",                      "DevOps",                "Sprint start"],
        ["Test data provisioning (valid/invalid/locked accounts)", "QA Lead",               "Sprint start"],
        ["OWASP ZAP integration in Jenkins",                      "Security Lead",          "Week 1"],
        ["JMeter performance scripts baseline",                   "Performance Engineer",   "Week 2"],
        ["Axe accessibility plugin configured",                   "QA Automation",          "Week 1"],
    ],
    col_widths=[3.5, 2.0, 2.5]
)
add_divider(doc)


# ── 4. Test Strategy ──────────────────────────────────────────────────────────

add_heading(doc, "4. Test Strategy", level=1)
add_heading(doc, "4.1  Testing Levels", level=2)
add_table(doc,
    headers=["Level", "Description", "Responsibility"],
    rows=[
        ["Unit Testing",        "Component-level validation of form validators, input sanitizers",          "Dev Team"],
        ["Integration Testing", "End-to-end auth flow with backend APIs and session store",                 "QA Automation"],
        ["System Testing",      "Full module testing across browsers, devices, and environments",           "QA Team"],
        ["Regression Testing",  "Automated re-execution after every code change",                          "CI/CD Pipeline"],
        ["UAT",                 "Stakeholder sign-off on business-critical flows",                         "Product Owner"],
    ],
    col_widths=[1.8, 4.0, 2.2]
)

add_heading(doc, "4.2  Test Types", level=2)
add_table(doc,
    headers=["Type", "Tool", "Scope"],
    rows=[
        ["Functional",      "Selenium WebDriver + TestNG",  "All login/register/forgot password scenarios"],
        ["API Testing",     "REST Assured / Postman",       "Endpoint validation — status codes, headers, payloads"],
        ["Performance",     "Apache JMeter",                "1000 concurrent users, load/stress/soak profiles"],
        ["Security",        "OWASP ZAP, Burp Suite",        "SQLi, XSS, CSRF, brute force, session fixation"],
        ["Accessibility",   "Axe-core, NVDA screen reader", "WCAG 2.1 AA compliance"],
        ["Compatibility",   "BrowserStack",                 "Cross-browser and cross-device matrix"],
        ["Exploratory",     "Manual / session-based",       "Edge cases, UX defects, error message accuracy"],
    ],
    col_widths=[1.8, 2.5, 3.7]
)

add_heading(doc, "4.3  Automation Strategy", level=2)
add_table(doc,
    headers=["Parameter", "Value"],
    rows=[
        ["Framework",          "Page Object Model (POM) with TestNG and Selenium"],
        ["Language",           "Java 17"],
        ["Reporting",          "Allure Reports"],
        ["CI Integration",     "Jenkins pipeline triggered on every pull request"],
        ["Parallel Execution", "TestNG parallel suite across Chrome, Firefox, Edge"],
        ["Data-Driven",        "Apache POI for Excel-based test data injection"],
        ["Coverage Target",    "85% automation of all identified test cases"],
    ],
    col_widths=[2.5, 5.5]
)
add_divider(doc)


# ── 5. Test Environment ───────────────────────────────────────────────────────

add_heading(doc, "5. Test Environment", level=1)
add_heading(doc, "5.1  Browser / OS Matrix", level=2)
add_table(doc,
    headers=["Browser", "Version", "OS", "Priority"],
    rows=[
        ["Chrome",         "Latest stable", "Windows 11, macOS Ventura",  "P1"],
        ["Firefox",        "Latest stable", "Windows 11, macOS Ventura",  "P1"],
        ["Microsoft Edge", "Latest stable", "Windows 11",                 "P1"],
        ["Safari",         "17+",           "macOS Ventura, iOS 17",      "P2"],
        ["Chrome Mobile",  "Latest",        "Android 14",                 "P2"],
    ],
    col_widths=[2.0, 1.5, 3.0, 1.5]
)

add_heading(doc, "5.2  Infrastructure", level=2)
add_table(doc,
    headers=["Component", "Specification"],
    rows=[
        ["Test Server",        "Staging environment — isolated DB, mirrored production config"],
        ["CI Server",          "Jenkins (self-hosted), triggered on PR merge"],
        ["Selenium Grid",      "Docker-based Selenium Grid 4 with 4 nodes"],
        ["Performance Server", "JMeter distributed mode — 2 injector nodes"],
        ["Security Scanner",   "OWASP ZAP 2.14 — CI integration via CLI API"],
        ["Test Management",    "JIRA + Zephyr Scale"],
        ["Defect Tracking",    "JIRA (project: OPENCART-QA)"],
    ],
    col_widths=[2.5, 5.5]
)
add_divider(doc)


# ── 6. Test Data Management ───────────────────────────────────────────────────

add_heading(doc, "6. Test Data Management", level=1)
add_heading(doc, "6.1  Account Categories", level=2)
add_table(doc,
    headers=["Data Category", "Description", "Source"],
    rows=[
        ["Valid User",          "Active account with confirmed email",                   "Pre-provisioned by DevOps"],
        ["Invalid User",        "Non-existent email address",                            "Generated by test framework"],
        ["Locked Account",      "Account locked after 5 failed attempts",               "Pre-provisioned"],
        ["Expired Session",     "Session token past TTL",                               "Simulated via timestamp manipulation"],
        ["Unverified Email",    "Registered but email not confirmed",                   "Pre-provisioned"],
        ["Admin User",          "Admin-level credentials",                              "Pre-provisioned (restricted access)"],
    ],
    col_widths=[2.0, 3.5, 2.5]
)

add_heading(doc, "6.2  Security Payloads", level=2)
add_table(doc,
    headers=["Payload Type", "Sample Value", "Purpose"],
    rows=[
        ["SQL Injection",  "' OR '1'='1",                       "Login bypass attempt"],
        ["SQL Injection",  "admin'--",                           "Comment injection"],
        ["XSS Stored",     "<script>alert('XSS')</script>",     "Persistent script injection"],
        ["XSS Reflected",  "\"><img src=x onerror=alert(1)>",  "Reflected injection via URL param"],
        ["Null Byte",      "admin%00",                          "Null byte termination"],
        ["Long String",    "10,000-character password",          "Buffer overflow check"],
        ["Unicode",        "test@example.com (unicode name)",   "Unicode handling"],
    ],
    col_widths=[2.0, 3.0, 3.0]
)

add_heading(doc, "6.3  Data Governance", level=2)
for item in [
    "All test data resides in an isolated staging DB — no production data used.",
    "PII is anonymized per GDPR Article 25 (privacy by design).",
    "Test data is reset to baseline state after every test run via DB snapshot restore.",
]:
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(item)
    run.font.size = Pt(10)
    run.font.color.rgb = DARK_GREY
doc.add_paragraph()
add_divider(doc)


# ── 7. Test Cases ─────────────────────────────────────────────────────────────

add_heading(doc, "7. Test Scenarios & Test Cases", level=1)

# ── 7.1 Login
add_heading(doc, "7.1  Login (/account/login)", level=2)
add_table(doc,
    headers=["TC_ID", "Scenario_ID", "Test Case Name", "Method", "Payload", "Exp. Status", "Validation"],
    rows=[
        ["TC_001", "TS_01", "Valid Login — Registered User",              "POST", "{valid_email, valid_password}",          "200", "Redirect to /account/account, session cookie set"],
        ["TC_002", "TS_01", "Valid Login — Remember Me Checked",          "POST", "{valid_email, valid_password, remember}", "200", "Persistent cookie set with 30-day expiry"],
        ["TC_003", "TS_02", "Invalid Login — Wrong Password",             "POST", "{valid_email, wrong_password}",          "401", "Error message displayed, no credential detail leaked"],
        ["TC_004", "TS_02", "Invalid Login — Unregistered Email",         "POST", "{unknown_email, any_password}",          "401", "Generic error — no account enumeration"],
        ["TC_005", "TS_02", "Empty Email Field",                          "POST", "{empty, valid_password}",                "400", "Inline validation error on email field"],
        ["TC_006", "TS_02", "Empty Password Field",                       "POST", "{valid_email, empty}",                   "400", "Inline validation error on password field"],
        ["TC_007", "TS_02", "Both Fields Empty",                          "POST", "{empty, empty}",                         "400", "Both field validation errors displayed simultaneously"],
        ["TC_008", "TS_02", "Email — Invalid Format (no @)",              "POST", "{invalidemail, password}",               "400", "Client-side validation fires before form submission"],
        ["TC_009", "TS_04", "Brute Force — 5 Consecutive Failures",       "POST", "{valid_email, wrong_password} x5",       "429", "Account lock triggered, lockout message shown"],
        ["TC_010", "TS_04", "Brute Force — Lock Duration Enforced",       "GET",  "—",                                     "200", "Account locked for configured duration (15 min)"],
        ["TC_011", "TS_07", "SQL Injection in Email Field",               "POST", "' OR '1'='1",                           "400", "Login fails, no DB error exposed, security event logged"],
        ["TC_012", "TS_07", "XSS in Password Field",                      "POST", "<script>alert(1)</script>",             "400", "Script not executed, input sanitized"],
        ["TC_013", "TS_08", "HTTPS Enforcement",                          "GET",  "—",                                     "301", "HTTP redirects to HTTPS, HSTS header present"],
        ["TC_014", "TS_08", "Secure Cookie Attributes",                   "POST", "Valid login",                           "200", "Cookie has Secure, HttpOnly, SameSite=Strict flags"],
        ["TC_015", "TS_08", "CSRF Token Validation",                      "POST", "Request without CSRF token",            "403", "Request rejected with CSRF protection error"],
    ],
    col_widths=[0.7, 0.9, 2.2, 0.7, 1.6, 0.9, 2.0]
)

# ── 7.2 Registration
add_heading(doc, "7.2  Registration (/account/register)", level=2)
add_table(doc,
    headers=["TC_ID", "Scenario_ID", "Test Case Name", "Method", "Payload", "Exp. Status", "Validation"],
    rows=[
        ["TC_016", "TS_09", "Valid New Registration",                     "POST", "All required fields valid",                   "200", "Success page, confirmation email sent"],
        ["TC_017", "TS_09", "Duplicate Email Registration",               "POST", "{existing_email, ...}",                       "400", "Error: E-Mail Address is already registered"],
        ["TC_018", "TS_09", "Password Below Minimum (< 4 chars)",         "POST", "{..., password: 'ab'}",                       "400", "Validation error on password field"],
        ["TC_019", "TS_09", "Password Above Maximum (> 20 chars)",        "POST", "{..., password: 21-char string}",             "400", "Validation error on password field"],
        ["TC_020", "TS_09", "Password Mismatch (confirm field)",          "POST", "{..., password != confirm}",                  "400", "Error: Password confirmation does not match"],
        ["TC_021", "TS_09", "Missing All Required Fields",                "POST", "All fields empty",                            "400", "All required field errors displayed simultaneously"],
        ["TC_022", "TS_09", "Privacy Policy Not Agreed",                  "POST", "{agree: false}",                              "400", "Checkbox validation error shown"],
        ["TC_023", "TS_07", "XSS in First Name Field",                    "POST", "{firstname: '<script>alert(1)</script>'}",    "400", "Input sanitized, script not stored or rendered"],
        ["TC_024", "TS_09", "Special Characters in Name Fields",          "POST", "{firstname: \"O'Brien\"}",                   "200", "Name stored and displayed correctly"],
        ["TC_025", "TS_09", "Unicode Characters in Email",                "POST", "Unicode email address",                      "400", "Handled per RFC 5322 compliance"],
    ],
    col_widths=[0.7, 0.9, 2.3, 0.7, 1.6, 0.9, 2.0]
)

# ── 7.3 Forgot Password
add_heading(doc, "7.3  Forgot Password (/account/forgotten)", level=2)
add_table(doc,
    headers=["TC_ID", "Scenario_ID", "Test Case Name", "Method", "Payload", "Exp. Status", "Validation"],
    rows=[
        ["TC_026", "TS_03", "Valid Registered Email Submission",          "POST", "{registered_email}",     "200", "Success message shown, reset email dispatched"],
        ["TC_027", "TS_03", "Unregistered Email — No Enumeration",        "POST", "{unknown_email}",        "200", "Same generic success message (no account enumeration)"],
        ["TC_028", "TS_03", "Empty Email Field",                          "POST", "{empty}",                "400", "Validation error displayed"],
        ["TC_029", "TS_03", "Invalid Email Format",                       "POST", "{not-an-email}",         "400", "Client-side validation fires"],
        ["TC_030", "TS_03", "Reset Link — Valid Token",                   "GET",  "?code=valid_token",      "200", "Password reset form presented"],
        ["TC_031", "TS_03", "Reset Link — Expired Token",                 "GET",  "?code=expired_token",    "400", "Error: Reset link has expired"],
        ["TC_032", "TS_03", "Reset Link — Tampered Token",                "GET",  "?code=tampered_token",   "400", "Error: Invalid reset token"],
        ["TC_033", "TS_03", "New Password — Meets Policy",                "POST", "{new_valid_password}",   "200", "Password updated, redirect to login"],
        ["TC_034", "TS_03", "New Password — Below Minimum",               "POST", "{password: 'ab'}",       "400", "Validation error on new password field"],
    ],
    col_widths=[0.7, 0.9, 2.3, 0.7, 1.6, 0.9, 2.0]
)

# ── 7.4 Session Management
add_heading(doc, "7.4  Session Management", level=2)
add_table(doc,
    headers=["TC_ID", "Scenario_ID", "Test Case Name", "Method", "Payload", "Exp. Status", "Validation"],
    rows=[
        ["TC_035", "TS_06", "Session Expiry — Idle Timeout",              "GET",  "Request after idle timeout",       "302", "Redirect to login page"],
        ["TC_036", "TS_06", "Explicit Logout",                            "GET",  "/account/logout",                  "302", "Session destroyed, cookie cleared, redirect to home"],
        ["TC_037", "TS_06", "Back Button After Logout",                   "GET",  "Browser back navigation",          "302", "Cached page not accessible, re-prompts login"],
        ["TC_038", "TS_06", "Concurrent Session — Same Account",          "POST", "Login from second browser",        "200", "Prior session invalidated OR both sessions allowed per policy"],
        ["TC_039", "TS_06", "Session Fixation Attack",                    "POST", "Pre-set session ID in cookie",     "200", "New session ID issued after successful login"],
    ],
    col_widths=[0.7, 0.9, 2.3, 0.7, 1.8, 0.9, 1.8]
)

# ── 7.5 Accessibility
add_heading(doc, "7.5  Accessibility", level=2)
add_table(doc,
    headers=["TC_ID", "Scenario_ID", "Test Case Name", "Tool", "Standard", "Validation"],
    rows=[
        ["TC_040", "TS_05", "Keyboard Navigation — Login Form",           "Manual + Axe",  "WCAG 2.1 SC 2.1.1", "All interactive elements reachable via Tab"],
        ["TC_041", "TS_05", "ARIA Labels on Form Fields",                 "Axe-core",      "WCAG 2.1 SC 1.3.1", "All inputs have aria-label or associated label"],
        ["TC_042", "TS_05", "Error Messages — Screen Reader Accessible",  "NVDA + manual", "WCAG 2.1 SC 3.3.1", "Errors announced by screen reader on focus"],
        ["TC_043", "TS_05", "Colour Contrast Ratio",                      "Axe-core",      "WCAG 2.1 SC 1.4.3", "Minimum 4.5:1 ratio for normal text"],
        ["TC_044", "TS_05", "Focus Indicator Visible",                    "Manual",        "WCAG 2.1 SC 2.4.7", "Focus ring visible on all interactive elements"],
        ["TC_045", "TS_05", "Form Labels — Not Placeholder Only",         "Manual",        "WCAG 2.1 SC 1.3.1", "Placeholders not used as sole label mechanism"],
    ],
    col_widths=[0.7, 0.9, 2.3, 1.2, 1.5, 2.4]
)
add_divider(doc)


# ── 8. Entry & Exit Criteria ──────────────────────────────────────────────────

add_heading(doc, "8. Entry Criteria", level=1)
add_table(doc,
    headers=["#", "Criterion", "Verified By"],
    rows=[
        ["EC-01", "Feature code complete and deployed to staging",              "Dev Lead sign-off"],
        ["EC-02", "Staging DB seeded with all required test data",              "DevOps confirmation"],
        ["EC-03", "Automation framework initialised and smoke tests pass",      "QA Lead"],
        ["EC-04", "OWASP ZAP integrated into CI pipeline",                      "Security Lead"],
        ["EC-05", "JMeter baseline scripts reviewed and approved",              "Performance Engineer"],
        ["EC-06", "All blockers from previous sprint resolved",                 "Scrum Master"],
    ],
    col_widths=[0.9, 5.0, 2.1]
)

add_heading(doc, "9. Exit Criteria", level=1)
add_table(doc,
    headers=["#", "Criterion", "Target"],
    rows=[
        ["XC-01", "Test execution completion",   "100% of planned test cases executed"],
        ["XC-02", "Pass rate",                   ">= 95% overall; 100% on P1 critical paths"],
        ["XC-03", "Open Sev-1 defects",          "Zero"],
        ["XC-04", "Open Sev-2 defects",          "Zero (or formally accepted with waiver)"],
        ["XC-05", "Security scan result",        "No Critical or High OWASP findings"],
        ["XC-06", "Performance validation",      "P95 response < 2000ms at 1000 concurrent users"],
        ["XC-07", "Accessibility",               "Zero WCAG 2.1 AA critical violations"],
        ["XC-08", "Sign-off obtained",           "Product Owner and Engineering Lead approved"],
    ],
    col_widths=[0.9, 3.5, 3.6]
)
add_divider(doc)


# ── 10. Defect Management ─────────────────────────────────────────────────────

add_heading(doc, "10. Defect Management", level=1)
add_heading(doc, "10.1  Severity Classification", level=2)
add_table(doc,
    headers=["Severity", "Definition", "Examples", "SLA (Fix)"],
    rows=[
        ["Sev-1 — Critical", "System unusable, data loss, security breach",   "Login always fails, SQL injection succeeds",        "Same day"],
        ["Sev-2 — High",     "Major functionality broken, no workaround",     "Forgot password email never sent",                  "2 business days"],
        ["Sev-3 — Medium",   "Feature degraded, workaround exists",           "Wrong error message text",                          "Current sprint"],
        ["Sev-4 — Low",      "Cosmetic or minor UX issue",                    "Button alignment, typo in label",                   "Next sprint"],
    ],
    col_widths=[1.6, 2.5, 2.5, 1.4]
)

add_heading(doc, "10.2  Defect Lifecycle", level=2)
add_paragraph(doc, "New  →  Assigned  →  In Progress  →  Fixed  →  In Verification  →  Closed", size=10, indent=0.3)
add_paragraph(doc, "                                          ↘  Rejected / Won't Fix", size=10, indent=0.3)
doc.add_paragraph()

add_heading(doc, "10.3  Mandatory Defect Fields (JIRA)", level=2)
for item in [
    "Summary, Severity, Priority, Environment, Build version",
    "Steps to Reproduce (numbered, precise)",
    "Expected Result vs Actual Result",
    "Screenshot / Video (mandatory for UI defects)",
    "Logs / Network HAR (mandatory for API/security defects)",
]:
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(item)
    run.font.size = Pt(10)
    run.font.color.rgb = DARK_GREY
doc.add_paragraph()
add_divider(doc)


# ── 11. Risk Register ─────────────────────────────────────────────────────────

add_heading(doc, "11. Risk Register", level=1)
add_table(doc,
    headers=["Risk ID", "Risk Description", "Prob.", "Impact", "Severity", "Mitigation Strategy"],
    rows=[
        ["R-01", "Staging environment instability causes test delays",             "Med",  "High",     "High",     "Daily smoke test; rollback procedure documented"],
        ["R-02", "Security scan false positives block CI pipeline",               "Low",  "Medium",   "Medium",   "Whitelist known FPs; manual triage by Security Lead"],
        ["R-03", "Performance regressions missed before release",                 "Med",  "High",     "High",     "JMeter gates in CI; alert on >10% latency increase"],
        ["R-04", "Test data corruption across parallel runs",                     "Med",  "Medium",   "Medium",   "DB snapshot restore after every full run"],
        ["R-05", "Browser compatibility gaps in Safari / iOS",                    "Low",  "Medium",   "Medium",   "BrowserStack dedicated Safari run pre-release"],
        ["R-06", "Brute force lockout mechanism absent from implementation",      "Low",  "Critical", "Critical", "Sev-1 defect raised immediately if not implemented"],
        ["R-07", "WCAG non-compliance flagged by legal/compliance",               "Low",  "High",     "High",     "Axe-core scan in CI; block merge on critical violations"],
        ["R-08", "Third-party CDN downtime affecting test runs",                  "Low",  "Medium",   "Medium",   "Tests use internal staging CDN as fallback"],
    ],
    col_widths=[0.7, 2.5, 0.6, 0.8, 0.9, 2.5]
)
add_divider(doc)


# ── 12. RACI Matrix ───────────────────────────────────────────────────────────

add_heading(doc, "12. RACI Matrix", level=1)
add_paragraph(doc, "R = Responsible  |  A = Accountable  |  C = Consulted  |  I = Informed", size=9, italic=True)
doc.add_paragraph()
add_table(doc,
    headers=["Activity", "QA Lead", "QA Engineers", "Dev Team", "Security", "DevOps", "Product Owner"],
    rows=[
        ["Test Plan authoring",          "R/A", "C",   "C",   "C", "I", "A"],
        ["Test case design",             "A",   "R",   "C",   "C", "I", "I"],
        ["Test environment setup",       "I",   "I",   "C",   "I", "R/A", "I"],
        ["Execution — functional",       "A",   "R",   "I",   "I", "I", "I"],
        ["Execution — security",         "C",   "C",   "I",   "R/A", "I", "I"],
        ["Execution — performance",      "A",   "R",   "I",   "I", "R", "I"],
        ["Defect triage",                "A",   "R",   "R",   "C", "I", "I"],
        ["Defect resolution",            "I",   "C",   "R/A", "C", "C", "I"],
        ["Sign-off",                     "C",   "I",   "C",   "C", "I", "R/A"],
    ],
    col_widths=[2.5, 0.9, 1.1, 0.9, 0.9, 0.8, 1.2]
)
add_divider(doc)


# ── 13. Schedule & Milestones ─────────────────────────────────────────────────

add_heading(doc, "13. Test Schedule & Milestones", level=1)
add_table(doc,
    headers=["Milestone", "Target Date", "Owner", "Status"],
    rows=[
        ["Test plan approved",                    "April 17, 2026",  "QA Lead",              "Done"],
        ["Environment ready",                     "April 20, 2026",  "DevOps",               "Pending"],
        ["Test case design complete",             "April 22, 2026",  "QA Team",              "Pending"],
        ["Automation scripts — login module",     "April 25, 2026",  "QA Automation",        "Pending"],
        ["Functional test execution",             "Apr 28–May 2",    "QA Team",              "Pending"],
        ["Security scan execution",               "May 2, 2026",     "Security Team",        "Pending"],
        ["Performance test execution",            "May 5, 2026",     "QA / DevOps",          "Pending"],
        ["Accessibility audit",                   "May 6, 2026",     "QA Team",              "Pending"],
        ["Defect fix & retest cycle",             "May 7–9, 2026",   "Dev + QA",             "Pending"],
        ["Final sign-off",                        "May 12, 2026",    "Product Owner",        "Pending"],
    ],
    col_widths=[3.0, 1.6, 1.8, 1.6]
)
add_divider(doc)


# ── 14. Tools & Infrastructure ────────────────────────────────────────────────

add_heading(doc, "14. Tools & Infrastructure Summary", level=1)
add_table(doc,
    headers=["Category", "Tool", "Version", "Purpose"],
    rows=[
        ["Automation",        "Selenium WebDriver",    "4.x",   "Browser automation"],
        ["Test Framework",    "TestNG",                "7.x",   "Test orchestration, parallel execution"],
        ["Build",             "Maven",                 "3.9.x", "Dependency management, CI integration"],
        ["Reporting",         "Allure Reports",        "2.x",   "Test execution reports"],
        ["API Testing",       "REST Assured",          "5.x",   "REST endpoint validation"],
        ["Performance",       "Apache JMeter",         "5.6",   "Load, stress, spike testing"],
        ["Security",          "OWASP ZAP",             "2.14",  "Automated DAST scanning"],
        ["Security (manual)", "Burp Suite Community",  "Latest","Manual proxy/intercept testing"],
        ["Accessibility",     "Axe-core",              "4.x",   "WCAG 2.1 automated scanning"],
        ["Accessibility",     "NVDA",                  "Latest","Screen reader validation"],
        ["Cross-browser",     "BrowserStack",          "—",     "Multi-browser/mobile testing"],
        ["CI/CD",             "Jenkins",               "LTS",   "Pipeline automation"],
        ["Test Management",   "JIRA + Zephyr Scale",   "Cloud", "Test cases, cycles, coverage"],
        ["Version Control",   "Git / GitHub",          "—",     "Source and test code management"],
    ],
    col_widths=[1.8, 2.2, 1.0, 3.0]
)
add_divider(doc)


# ── 15. Deliverables ─────────────────────────────────────────────────────────

add_heading(doc, "15. Deliverables", level=1)
add_table(doc,
    headers=["#", "Deliverable", "Format", "Owner", "Due Date"],
    rows=[
        ["D-01", "Enterprise Master Test Plan",          "DOCX",         "QA Lead",           "April 17, 2026"],
        ["D-02", "Requirements Traceability Matrix",     "Markdown/Excel","QA Lead",           "April 22, 2026"],
        ["D-03", "RICEPOT Framework Document",           "Markdown",     "QA Architect",      "April 17, 2026"],
        ["D-04", "Selenium Automation Test Suite",       "Java/Maven",   "QA Automation",     "April 25, 2026"],
        ["D-05", "Allure Execution Report — Functional", "HTML",         "QA Team",           "May 2, 2026"],
        ["D-06", "JMeter Performance Report",            "HTML/JTL",     "Performance Eng",   "May 5, 2026"],
        ["D-07", "OWASP ZAP Security Report",            "HTML/XML",     "Security Lead",     "May 2, 2026"],
        ["D-08", "Accessibility Audit Report",           "HTML/PDF",     "QA Team",           "May 6, 2026"],
        ["D-09", "Final Test Summary Report",            "DOCX",         "QA Lead",           "May 12, 2026"],
        ["D-10", "Release Sign-off Document",            "PDF",          "Product Owner",     "May 12, 2026"],
    ],
    col_widths=[0.5, 2.8, 1.4, 1.6, 1.7]
)
add_divider(doc)


# ── 16. Sign-off ─────────────────────────────────────────────────────────────

add_heading(doc, "16. Approval & Sign-off", level=1)
add_table(doc,
    headers=["Role", "Name", "Signature", "Date"],
    rows=[
        ["QA Automation Architect", "", "", ""],
        ["Engineering Lead",        "", "", ""],
        ["Security Lead",           "", "", ""],
        ["Product Owner",           "", "", ""],
        ["VP Engineering",          "", "", ""],
    ],
    col_widths=[2.5, 2.0, 2.0, 1.5]
)

doc.add_paragraph()
footer_p = doc.add_paragraph()
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer_p.add_run(
    "Generated using the RICEPOT Framework — Role · Instructions · Context · Expected Output · Persona · Output Format · Tone"
)
run.font.size = Pt(8)
run.font.italic = True
run.font.color.rgb = MID_BLUE


# ── Save ─────────────────────────────────────────────────────────────────────

output_path = "TEST_PLAN_OpenCart_Login.docx"
doc.save(output_path)
print(f"[OK] Saved: {output_path}")
