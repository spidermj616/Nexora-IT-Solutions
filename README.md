# Nexora IT Solutions — Business Website Starter

A real Flask website starter with a responsive front end and a working enquiry form that stores submissions in SQLite. No paid theme or API key is required.

## Run locally on Windows

1. Install Python 3.11 or newer from https://www.python.org/downloads/ (enable **Add Python to PATH**).
2. Extract this ZIP.
3. Open the extracted folder in VS Code.
4. Open Terminal → New Terminal and run:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```

   If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and then `.\.venv\Scripts\python.exe app.py`.

5. Visit http://127.0.0.1:5000 in your browser. `/health` returns a basic health check.

## Publish a public URL free (Render)

1. Create a GitHub account at https://github.com and a **public** repository called `nexora-it-website`.
2. Upload all project files and folders to the repository, preserving `templates/index.html` and `templates/enquiries.html`.
3. Create an account at https://render.com and select **New → Web Service**. Connect the repository.
4. Set:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Add environment variable `SECRET_KEY` with a long random secret value.
6. For the admin enquiry page, set `ADMIN_TOKEN` to a long random secret value. Do not share it.
7. Click deploy. Render will provide a public HTTPS URL such as `https://your-service-name.onrender.com`.

### Important persistence note
SQLite is suitable for local development and demos, but a hosting platform's local filesystem may be temporary and may be reset during redeploys/restarts. For production customer enquiries, configure a persistent disk/database (for example a managed PostgreSQL database) and backups before relying on it for business. Free hosting plans may sleep or have other limits.

## Admin enquiry view

After setting `ADMIN_TOKEN`, open:

`https://YOUR-PUBLIC-HOST/admin/enquiries?token=YOUR_ADMIN_TOKEN`

This simple token-in-query-string protection is only a starter convenience; the token may appear in browser history, server logs, and analytics. For real production use, replace it with proper login/authentication and use a persistent database. Do not share the admin URL or token.

## Before using for an actual company
- Replace the sample company name, service descriptions, example project concepts, and contact details with truthful company information.
- Add a real company email and privacy policy/contact details.
- Never present sample concepts as completed client work or claim credentials/certifications you do not have.
- Add spam protection/rate limiting and production-grade admin authentication before advertising the form widely.
- If handling personal data, follow applicable privacy and data-protection requirements.
