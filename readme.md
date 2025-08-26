# Django Poll App

A simple poll/voting system built with Django.

* Admins can create, manage, end or reopen polls, export results to Excel, and delete votes.
* Users can register, login, and vote (only once per poll).
* Poll results are displayed with charts using Chart.js.

---

## Setup Instructions

1. Create a virtual environment
   * Run: `python -m venv venv`
   * Activate it:

     • On Windows: `venv\Scripts\activate`

     • On macOS/Linux: `source venv/bin/activate`
2. Install dependencies
   * Run: `pip install -r requirements.txt`
3. Run migrations
   * Run: `python manage.py migrate`
4. Create a superuser (for admin access)
   * Run: `python manage.py createsuperuser`
5. Start the development server
   * Run: `python manage.py runserver`
   * Open in browser: `http://127.0.0.1:8000`

---

## Requirements

The file `requirements.txt` contains:

* Django >= 4.2, < 5.0
* openpyxl >= 3.1.2

Install with: `pip install -r requirements.txt`

---

## User Roles

* Admin → can create polls, end/reopen polls, export results, and delete votes.
* User → can register, login, and vote (one vote per poll).

---

## Tech Stack

* Backend: Django, Django ORM
* Frontend: Tailwind CSS, Chart.js
* Database: SQLite (works out of the box)
