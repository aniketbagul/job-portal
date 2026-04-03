# Django Job Portal

A straightforward, modern job board web application built using Django and Tailwind CSS. The platform connects candidates with job listings and provides employers with a custom dashboard to manage their postings and evaluate applicants.

## Features

- **Job Searching & Filtering:** Users can browse active job listings and filter by location or role.
- **User Accounts:** Full authentication system for logging in and registering.
- **Custom Admin Dashboard:** Employers/Admins can add, edit, and delete job postings without relying on the default Django admin site.
- **Application Tracking:** Candidates can apply to jobs by uploading their resumes (PDF or DOCX). Employers can view applications securely from their dashboard.
- **ATS Resume Analyzer:** Includes an automated parsing engine (powered by PyPDF2 and docx2txt) that extracts applicant resume text and compares it against the job description to calculate a skill match score.

## Tech Stack

- **Backend:** Python 3, Django
- **Frontend:** HTML, Tailwind CSS (via CDN)
- **Database:** SQLite (Default)
- **Dependencies:** `PyPDF2`, `docx2txt`

## Local Setup

1. **Clone the repository** (or download the files).
2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On macOS/Linux
   env\Scripts\activate     # On Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the Application:** Open your browser to `http://127.0.0.1:8000/`.

## Administrator Usage

To utilize the Employer Dashboard and ATS features:
1. Create a superuser account using `python manage.py createsuperuser`.
2. Login through the standard `/login/` UI.
3. Access the Admin Panel via the top navigation bar to post jobs and review resumes.
