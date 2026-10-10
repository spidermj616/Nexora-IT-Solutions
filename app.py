import os
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, url_for, flash, render_template, g, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-before-deploying")
DATABASE = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "nexora.db"))

SERVICES = [
    ("Web Development", "Responsive business websites, landing pages, and web applications.", "⌘"),
    ("Custom Software", "Internal tools, dashboards, and workflow automation built around your process.", "⚙"),
    ("Cloud & DevOps", "Deployment planning, cloud setup, monitoring, and maintainable release workflows.", "☁"),
    ("Cybersecurity", "Practical security reviews and implementation guidance to reduce common risks.", "⬡"),
    ("UI/UX Design", "User-friendly page layouts, prototypes, and consistent design systems.", "▦"),
    ("AI & Data", "Useful reporting dashboards and carefully scoped AI-powered workflows.", "✦"),
]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            service TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

@app.route("/")
def home():
    return render_template("index.html", services=SERVICES, current_year=datetime.now().year)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    service = request.form.get("service", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not service or not message:
        flash("Please complete every field before submitting.", "error")
        return redirect(url_for("home") + "#contact")
    if len(name) > 100 or len(email) > 254 or len(service) > 100 or len(message) > 5000:
        flash("One of your fields is too long. Please shorten it and try again.", "error")
        return redirect(url_for("home") + "#contact")
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("home") + "#contact")

    db = get_db()
    db.execute(
        "INSERT INTO enquiries (name, email, service, message, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, email, service, message, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
    )
    db.commit()
    flash("Thanks! Your enquiry has been received. We'll follow up using the email you provided.", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/admin/enquiries")
def enquiries():
    # Set ADMIN_TOKEN in your hosting environment before enabling this route.
    token = os.environ.get("ADMIN_TOKEN")
    if not token:
        abort(404)
    if request.args.get("token", "") != token:
        abort(403)
    rows = get_db().execute("SELECT * FROM enquiries ORDER BY id DESC LIMIT 200").fetchall()
    return render_template("enquiries.html", enquiries=rows)

@app.route("/health")
def health():
    return {"status": "ok"}

init_db()

if __name__ == "__main__":
    app.run(debug=False, port=int(os.environ.get("PORT", "5000")), host="0.0.0.0")
