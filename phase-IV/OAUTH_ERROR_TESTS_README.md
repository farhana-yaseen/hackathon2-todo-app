# OAuth Error Testing Suite

This directory contains tools to test error scenarios in GitHub and Google OAuth authentication flows.

## Files:

### test_oauth_errors.py
- **Purpose**: Comprehensive documentation of all possible OAuth error scenarios
- **Format**: Educational/test planning document
- **Content**: All edge cases and error conditions that should theoretically be tested

### test_oauth_errors_practical.py
- **Purpose**: Executable test script that can run against a live API
- **Format**: Runnable Python script
- **Content**: Practical tests that verify actual API behavior for error handling

## Usage:

For planning and understanding: `test_oauth_errors.py`
For actual testing: `test_oauth_errors_practical.py`

The separation allows for comprehensive test planning while maintaining executable tests that can be run in CI/CD environments.