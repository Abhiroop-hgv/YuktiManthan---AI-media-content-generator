# Tests Directory

This directory contains all test files for the project.

## Structure

```
tests/
├── unit/               # Unit tests
├── integration/        # Integration tests
├── fixtures/          # Test data and fixtures
└── conftest.py       # pytest configurations
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file.py

# Run with coverage
pytest --cov=.
```

## Writing Tests

- Follow the AAA pattern (Arrange, Act, Assert)
- Use meaningful test names
- One assertion per test when possible
- Use fixtures for common setup

## Test Categories

1. Unit Tests
   - Test individual components
   - Mock external dependencies

2. Integration Tests
   - Test component interactions
   - Test API integrations

3. End-to-End Tests
   - Test complete workflows
   - Minimal mocking

## Mocking

- Use pytest-mock for mocking
- Mock external APIs in tests
- Don't mock the system under test
