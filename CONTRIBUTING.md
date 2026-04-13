# Contributing to Project_02_RICE_POT_Selenium_FW

Thank you for considering contributing! This document outlines the process and standards for contributions.

## 🚀 Getting Started
- Fork the repository and clone your fork locally.
- Install dependencies using Maven (`mvn clean install`).
- Run tests with `mvn test` to ensure everything works before making changes.

## 🌱 Branching Strategy
- Create feature branches from `main`.
- Use clear branch names: `feature/data-provider`, `bugfix/login-page`, `docs/update-readme`.

## 📝 Commit Guidelines
- Follow [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation updates
  - `test:` for adding or updating tests
- Example: `feat: implement JSON data provider`

## 🔀 Pull Request Process
- Ensure your branch is up to date with `main`.
- Push your branch and open a PR against `main`.
- Fill in the PR template (motivation, changes, testing, future work).
- All tests must pass before requesting review.
- Address reviewer comments promptly.

## 🎯 Code Standards
- Follow Java coding conventions.
- Use Page Object Model (POM) for Selenium tests.
- Avoid hardcoded waits; prefer explicit waits.

## 🧪 Testing
- Add unit tests for new features.
- Run regression suite before submitting PR.
- Ensure exception handling is covered in tests.

## 🐛 Reporting Issues
- Use the issue tracker to report bugs.
- Include steps to reproduce, expected vs actual behavior, and logs/screenshots.
