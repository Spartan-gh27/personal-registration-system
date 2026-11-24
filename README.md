
# Personal Registration System

A command-line CRUD application developed with Python and SQLite for managing personal records.

## Technologies Used

- Python
- SQLite
- SQL

## Features

- Register new people.
- List all registered records.
- Update existing records.
- Delete records.
- Search for people by name.
- Validate user input.
- Handle database exceptions.

## Database Structure

The application uses an SQLite database with a `pessoas` table containing the following fields:

| Field | Type | Description |
|---|---|---|
| cod | INTEGER | Primary key with auto-increment |
| nome | TEXT | Person's name |
| altura | REAL | Person's height |

The database and its table are automatically created when the application starts.

## How to Run

1. Make sure Python 3.10 or newer is installed.
2. Clone this repository.
3. Open the project directory in your terminal.
4. Run the application using:

```bash
python -m exercicios.ex019
```

## Author

Gustavo Henry Silva Campos
