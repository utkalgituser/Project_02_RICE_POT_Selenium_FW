# 📝 Pull Request Reviewer Checklist

Use this checklist when reviewing PRs to ensure consistency, quality, and clarity.

---

## ✅ General Review
- [ ] PR title is clear and descriptive
- [ ] PR description explains motivation, changes, and benefits
- [ ] Linked issues or references are included (if applicable)
- [ ] Commit messages follow convention (e.g., `feat:`, `fix:`, `docs:`)

---

## 🔧 Code Quality
- [ ] Code follows project style and naming conventions
- [ ] No obvious duplication or unnecessary complexity
- [ ] Proper error/exception handling is implemented
- [ ] Logging/debugging statements are appropriate (not excessive)

---

## 🧪 Testing
- [ ] Unit tests are added/updated for new functionality
- [ ] Tests cover edge cases and failure scenarios
- [ ] All tests pass locally and in CI/CD pipeline
- [ ] No flaky or unstable tests introduced

---

## 📂 Documentation
- [ ] README or relevant docs updated with new changes
- [ ] Inline comments explain complex logic
- [ ] Configuration changes are documented
- [ ] Contribution guidelines followed

---

## 🔀 Merge Readiness
- [ ] Branch is up to date with `main`
- [ ] No merge conflicts
- [ ] CI/CD checks are green
- [ ] Reviewer comments addressed

---

## 🟢 Approval Comments (Examples)
- “Looks great, thanks for the clear commit message and documentation updates.”
- “Code changes are clean and tests pass. Approved.”
- “Good job implementing JSON data provider and exception handling. This will improve maintainability.”

---

## ⚠️ Request Changes Comments (Examples)
- “Please add unit tests for the new JSON data provider to ensure coverage.”
- “Consider breaking down the Page Object assertions into smaller reusable methods for clarity.”
- “Exception handling looks good, but can you document the custom exceptions in the README?”

---

## 💡 Suggestions (Non-blocking)
- “Nice work! You might want to add contribution guidelines in the README for future collaborators.”
- “Could we standardize naming conventions in the utilities package for consistency?”
- “Adding logging around exception handling would make debugging easier.”
