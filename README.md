# Online Voting System

A Django-based online voting system for managing elections, candidates, and votes.

## Features

- User registration and login
- Profile management and password change
- Ongoing and expired election pages
- Vote casting for ongoing elections
- Admin dashboard for election and candidate management
- Application uses Django ORM and built-in authentication

## Setup

1. Create a Python virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the site at `http://127.0.0.1:8000/`

## Notes

- The project uses SQLite by default. To use MySQL, update `DATABASES` in `voting_system/settings.py`.
- Admin users should be marked as staff via Django admin or the `createsuperuser` command.
