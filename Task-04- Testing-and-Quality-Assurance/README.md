# 🌿 GreenLife – Testing and Quality Assurance

### Yuvaintern Python Developer Internship | Task 4

##  Project Overview

GreenLife is a Flask-based Sustainability Tracker that helps users monitor their environmental impact by recording daily activities such as electricity consumption and travel.

This task focuses on testing and quality assurance of the GreenLife application. The objective was to verify application functionality, identify potential issues, validate user inputs, test database operations, and measure application performance.

##  Testing Objectives

- Verify individual application functions.
- Test integration between Flask routes, database operations, and dashboard components.
- Validate input fields and handle invalid data.
- Test edge cases and application error handling.
- Measure response times for important operations.
- Perform manual User Acceptance Testing (UAT).

## Technologies Used

- Python 3.14.6
- Flask
- SQLite
- Pytest
- HTML
- CSS
- JavaScript
- Chart.js

##  Project Structure

```text
GreenLife-Redesigned/
│
├── app.py
├── greenlife.db
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── tests/
    ├── conftest.py
    ├── test_app.py
    ├── test_integration.py
    ├── test_system.py
    ├── test_edge_cases.py
    ├── test_error_handling.py
    └── test_performance.py
```

##  Testing Methodology

The application was tested using pytest and Flask's test client.

### 1. Unit / Application Testing
- Dashboard loading.
- Carbon emission calculations.
- Valid activity submission.
- Input validation.
- Activity deletion.

### 2. Integration Testing
- Database storage and retrieval.
- Activity updates on the dashboard.
- Multiple activity calculations.
- History updates after adding or deleting records.

### 3. System Testing
- Complete application workflow.
- Dashboard availability.
- Multiple activity submissions.
- Invalid input handling.
- Application response to invalid URLs.

### 4. Edge Case Testing
- Missing activity amount.
- Missing activity date.
- Invalid and boundary input values.

### 5. Error Handling Testing
- Invalid routes.
- Appropriate validation messages.
- Prevention of invalid database entries.

### 6. Performance Testing
Performance tests measured dashboard response time, activity insertion time, and dashboard performance with multiple records.

##  Automated Testing Results

**Final Result: 34 Tests Passed Successfully!**

| Testing Category | Test Cases | Result |
|---|---:|---|
| Application / Unit Testing | 16 | Passed |
| Integration Testing | 4 | Passed |
| System Testing | 6 | Passed |
| Edge Case Testing | 2 | Passed |
| Error Handling Testing | 3 | Passed |
| Performance Testing | 3 | Passed |
| **Total** | **34** | **34 Passed** |

### Test Execution

Command used:

```bash
py -m pytest -v
```

Final output:

```text
collected 34 items

34 passed in 1.29s
```

**Failed Tests:** 0

##  Performance Testing Results

Performance testing was conducted using Python's `time.perf_counter()` and Flask's local test client.

| Performance Test | Observed Result |
|---|---:|
| Dashboard average response time (30 requests) | 3.29 ms |
| Dashboard median response time | 2.30 ms |
| Activity insertion average (10 requests) | 6.65 ms |
| Dashboard with 50 records | 9.55 ms |

*Note: These measurements represent local test-client execution and are not production or real-browser benchmarks.*

##  User Acceptance Testing (UAT)

Manual testing was performed through the browser using the locally running application.

The following scenarios were verified:

1. Adding a new activity with valid information.
2. Checking updated dashboard values and charts.
3. Viewing recently added activities.
4. Deleting an activity and verifying updated records.

**UAT Result:** All four manual test scenarios passed.

##  Debugging and Improvements

During testing, a few environment-related issues were encountered:

- Installed pytest in the Python environment.
- Resolved a test import-path issue by running commands from the correct project directory.
- Organized test cases into separate modules for easier maintenance.
- Used an isolated temporary database for automated testing.

These steps helped make the testing process more reliable and repeatable.

##  Key Learnings

Through this task, I gained practical experience in:

- Writing automated test cases using pytest.
- Understanding unit, integration, and system testing.
- Testing Flask applications using a test client.
- Validating user input and handling errors.
- Testing SQLite database operations.
- Identifying edge cases.
- Measuring application performance.
- Performing manual User Acceptance Testing.
- Understanding the importance of software quality assurance.

##  Conclusion

The GreenLife application successfully completed all 34 automated test cases with zero failures. Manual testing also confirmed that the main activity management workflow worked as expected.

This task improved my understanding of software testing, debugging, validation, performance measurement, and quality assurance in Python-based web applications.

---

### Internship Details

**Internship:** Yuvaintern Python Developer Internship  
**Task:** Task 4 – Testing and Quality Assurance  
**Project:** GreenLife – Sustainability Tracker  
**Testing Framework:** Pytest

*Developed and tested as part of my Python Developer Internship learning journey.*
