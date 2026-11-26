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
4. Commit changes using clear commit messages that start with one of these prefixes:

| Prefix | Use for |
| --- | --- |
| `feat:` | a new feature |
| `fix:` | a bug fix |
| `docs:` | README or other documentation |
| `test:` | adding or updating tests |
| `refactor:` | code changes that don't change behaviour |
| `chore:` | setup, dependencies, config |

Examples:

```text
feat: add transaction model
fix: correct transaction validation
docs: update git workflow
test: add tests for login
```

5. Push the feature branch to GitHub.
6. Create a Pull Request from the feature branch into `main`. The PR description is pre-filled from the template in `.github/pull_request_template.md`; fill it in.
7. Link the Pull Request to the corresponding GitHub Issue where applicable, for example:

```text
Closes #19
```

8. At least one team member should review the Pull Request before it is merged.
9. Once approved, merge the Pull Request into `main`.
10. Switch back to `main` locally and pull the latest changes before starting the next task.

The `main` branch should always contain the latest reviewed and working version of the application. Direct development and commits on `main` should be avoided.

A simple personal spending tracker built with Flask and SQLite.

## Installation

You need Python 3.11 or newer and Git.

1. Clone the repository and go into the project folder:

```bash
git clone https://github.com/raialiakbar/SpendSmart.git
cd SpendSmart
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
```

On Windows use `python` instead of `python3`.

3. Activate it:

```bash
source .venv/bin/activate     # macOS / Linux
.venv\Scripts\activate        # Windows
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

With the virtual environment active, start the app from the project folder:

```bash
python run.py
```

Then open http://127.0.0.1:5000 in your browser. Stop the server with `Ctrl+C`.

The SQLite database is created automatically in `instance/spendsmart.db` the first time the app starts. To start with an empty database, stop the app and delete that file.

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | `dev` | Flask secret key for sessions |
| `DATABASE_URL` | `sqlite:///spendsmart.db` | Database connection string |

## Database Structure

The database has two tables, defined in `app/models.py` with Flask-SQLAlchemy. Tables are created on startup with `db.create_all()`.

### `users`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `username` | String(64) | Required, unique, indexed |
| `email` | String(120) | Required, unique, indexed |
| `password_hash` | String(256) | Required. Only the hash is stored, never the plain password |
| `display_name` | String(64) | Optional |
| `currency` | String(3) | Required, default `EUR` |
| `created_at` | DateTime | Required, set when the user registers (UTC) |
| `last_login_at` | DateTime | Optional, updated on login |

### `transactions`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `user_id` | Integer | Required, foreign key to `users.id`, indexed |
| `type` | String(10) | Required, `income` or `expense` |
| `amount` | Numeric(10, 2) | Required, must be greater than 0 |
| `category` | String(50) | Required, one of the categories in `app/categories.py` |
| `date` | Date | Required, defaults to today |
| `description` | String(255) | Optional |
| `payment_method` | String(20) | Optional: `cash`, `card` or `bank_transfer` |
| `created_at` | DateTime | Required, set when the transaction is created (UTC) |
| `updated_at` | DateTime | Required, updated whenever the transaction changes (UTC) |

Two check constraints protect the data: `type` must be `income` or `expense`, and `amount` must be positive.

### Relationship

One user has many transactions, and each transaction belongs to exactly one user (one-to-many through `transactions.user_id`).

```text
users (1) ──< transactions (many)
```

In code, `user.transactions` gives all transactions of a user and `transaction.user` gives its owner. Deleting a user also deletes their transactions (`cascade="all, delete-orphan"`).
