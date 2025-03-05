# CryptoQA Automation Testing Framework

## Overview
CryptoQA is a Python - based automation testing framework specifically designed for weather forecast applications. This framework adopts the BDD (Behavior - Driven Development) methodology, uses pytest - bdd for test case management, supports automated testing on both Android and iOS platforms, and provides comprehensive API testing support.

## Tech Stack
- Python 3.x
- pytest
- pytest - bdd
- pytest - html
- uiautomator2
- PyYAML
- colorama
- requests

## Project Structure
```
CryptoQA/
├── common/                 # Common utility classes
│   ├── automation_config.py    # Configuration management
│   ├── custom_logger.py        # Logging utility
│   └── locate_type.py          # Element location types
├── features/              # BDD feature files
├── page/                 # Page objects
│   ├── android/              # Android pages
│   │   ├── home_page.py         # Home page
│   │   └── ninth_day_forecast_page.py  # Nine - day forecast page
│   └── common/               # Common base page class
├── test_case/            # Test cases
│   ├── test_weather_forecast.py  # UI test cases
│   └── test_api.py            # API test cases
├── test_environment_config/  # Test environment configuration
├── utils/                # Utility functions
├── log/                  # Log files
├── image/                # Screenshot files
├── report/               # Test reports
└── requirements.txt      # Dependency list
```

## Installation
### Prerequisites
- Python 3.x
- Android device or emulator (for Android testing)
- iOS device (for iOS testing)

### Setup Steps
1. Clone the repository
```bash
git clone [repository_url]
cd CryptoQA
```
2. Create and activate a virtual environment
```bash
python -m venv.venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source.venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration
1. Create an `automation_local.yaml` file in the `test_environment_config` directory.
2. Configure test device information:
```yaml
serial_no: "device_serial_number"
platform: "android"  # or "ios"
```

## Usage
### Running Tests
```bash
# Run all tests
pytest

# Run a specific test file
pytest test_case/test_weather_forecast.py

# Run API tests
pytest test_case/test_api.py

# Run tests with a specific tag
pytest -m bdd

# Generate an HTML report
pytest --html=report/report.html --self - contained - html
```

### Test Reports
After test execution, you can find:
- Test logs in the `log` directory.
- Test screenshots in the `image` directory.
- HTML test reports in the `report` directory.

## Development Guide
### Adding New Test Cases
1. Create a `.feature` file in the `features` directory.
2. Create a corresponding test file in the `test_case` directory.
3. Create the required page object classes in the `page` directory.

### API Testing
1. API test cases are located in `test_case/test_api.py`.
2. The following functions are supported:
   - Capture and validate API endpoints.
   - Send requests and validate response status.
   - Extract and validate specific data (such as relative humidity).

### Coding Standards
- Use Python type hints.
- Follow the PEP 8 coding style.
- Add complete docstrings for all classes and methods.
- Use standardized logging practices.
- Maintain naming convention consistency.

## Future Enhancements
- [ ] Enhanced test report generation, such as reportportal.
- [ ] API testing support, more encapsulated interfaces and tools, such as auto - generating API scripts.
- [ ] Parallel test execution support.
- [ ] CI/CD pipeline integration.
- [ ] Performance testing module, such as locust.
- [ ] Optimization of test data management, for example, using FastApi, Pydantic, and Facker to generate test data.
- [ ] Optimization of element location.
- [ ] Support for iOS testing.
- [ ] The API test failed to capture packets, and the mobile phone failed to install the certificate. Currently, it is mocked.

## Troubleshooting
1. Q: What should I do if the device connection fails?
   A: Verify that the device serial number is correct and ensure that developer options and USB debugging are enabled on the device.

2. Q: How do I debug test cases?
   A: Set the environment variable `IS_DEBUG_ENV = 1` or add the `--debug = 1` parameter when running the test.

3. Q: Why can't I see the test report?
   A: Ensure that the `report` directory has been created and run the test using the correct command:
   ```bash
   pytest --html=report/report.html --self - contained - html
   ```

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Push to the branch.
5. Create a Pull Request.

## Best Practices
- Write clear and descriptive test scenarios.
- Maintain the page object pattern.
- Separate test data from test logic.
- Conduct regular code reviews and updates.
- Document any changes or additions.
- Maintain naming convention consistency.
- Ensure the integrity of test reports.

## License
This project is based on the MIT license. 