# EventManagement

A Django-based event management system with modules for accounts, students, teachers, events, and rooms.

## Project Structure

- `eventmanagement/` - main Django project and apps
- `main.py` - default PyCharm sample script
- `manage.py` - Django management entry point at the repository root

## Features

- Account login flow
- Student management
- Teacher management
- Event management
- Room management

## Requirements

- Python 3
- Django
- MySQL

## Database Configuration

The current Django settings use MySQL with these defaults:

- Database: `event_system`
- User: `root`
- Password: `root`
- Host: `localhost`
- Port: `3306`

Update `eventmanagement/eventmanagement/settings.py` if your local database settings differ.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django mysqlclient
```

Create the MySQL database:

```sql
CREATE DATABASE event_system;
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Notes

- `.venv`, local database files, logs, and IDE files are excluded from Git.
- This repository currently does not include a dependency lockfile such as `requirements.txt`.
