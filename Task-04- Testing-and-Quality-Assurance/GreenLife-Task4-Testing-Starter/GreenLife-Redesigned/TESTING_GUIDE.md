# GreenLife – Task 4: Testing and Quality Assurance

## 1. Setup

Open a terminal in the `GreenLife-Redesigned` project folder and run:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install pytest
```

If PowerShell blocks activation, run the commands below instead (activation is optional):

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip install pytest
.\venv\Scripts\python.exe -m pytest -v
```

## 2. Run automated tests

```bash
python -m pytest -v
```

The test suite uses a temporary SQLite database. It does not write test records into the supplied `greenlife.db` file.

## 3. Test coverage

The current automated tests check:

- Home page HTTP response and page content.
- Electricity and car emission calculations.
- Six-month date range generation.
- Successful activity insertion and stored emission value.
- Empty, text, zero, negative, NaN and infinite amounts.
- Unsupported activity category.
- Future activity date.
- Notes exceeding 200 characters.
- Deleting an existing activity and handling a missing activity.

## 4. Evidence to capture

After running the tests, capture a screenshot showing the terminal command `python -m pytest -v` and its final passed/failed summary. If any test fails, keep the failure output, investigate the cause, fix the code or test as appropriate, and run the complete suite again.

## 5. Important reporting rule

Only report the results actually produced on your computer. Do not claim that all tests passed until the command completes successfully. Record the Python and Flask versions used, the date of testing, the number of passed/failed tests, and any bugs found and corrected.
