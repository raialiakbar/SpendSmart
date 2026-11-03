# SpendSmart

## Git Workflow

To keep development organized and avoid conflicts, all new features and fixes must be developed on separate branches instead of directly on `main`.

1. Before starting a new task, switch to the `main` branch and pull the latest changes.
2. Create a new branch for the user story or feature being implemented.

Example branch names:

```text
feature/us-19-transaction-model
feature/us-20-add-income
fix/login-validation
```

3. Make and test the required changes on the feature branch.
4. Commit changes using clear commit messages, for example:

```text
feat: add transaction model
fix: correct transaction validation
docs: update git workflow
```

5. Push the feature branch to GitHub.
6. Create a Pull Request from the feature branch into `main`.
7. Link the Pull Request to the corresponding GitHub Issue where applicable, for example:

```text
Closes #19
```

8. At least one team member should review the Pull Request before it is merged.
9. Once approved, merge the Pull Request into `main`.
10. Switch back to `main` locally and pull the latest changes before starting the next task.

The `main` branch should always contain the latest reviewed and working version of the application. Direct development and commits on `main` should be avoided.

A simple personal spending tracker built with Flask and SQLite.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Then open http://127.0.0.1:5000. The SQLite database is created automatically in `instance/spendsmart.db`.
