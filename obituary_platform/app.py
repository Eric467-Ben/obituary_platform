import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus
from xml.sax.saxutils import escape

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "obituary_platform.db"
PER_PAGE = 5

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["DATABASE"] = DATABASE


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS obituaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            date_of_birth DATE NOT NULL,
            date_of_death DATE NOT NULL,
            content TEXT NOT NULL,
            author VARCHAR(100) NOT NULL,
            submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            slug VARCHAR(255) UNIQUE NOT NULL
        )
        """
    )
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Initialized obituary_platform database.")


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "obituary"


def unique_slug(name):
    db = get_db()
    base = slugify(name)
    slug = base
    counter = 2
    while db.execute("SELECT id FROM obituaries WHERE slug = ?", (slug,)).fetchone():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


def validate_obituary(form):
    errors = []
    name = form.get("name", "").strip()
    date_of_birth = form.get("date_of_birth", "").strip()
    date_of_death = form.get("date_of_death", "").strip()
    content = form.get("content", "").strip()
    author = form.get("author", "").strip()

    if not name or len(name) > 100:
        errors.append("Name is required and must be 100 characters or fewer.")
    if not author or len(author) > 100:
        errors.append("Author is required and must be 100 characters or fewer.")
    if not content or len(content) < 20:
        errors.append("Content is required and must be at least 20 characters.")

    try:
        birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        death = datetime.strptime(date_of_death, "%Y-%m-%d").date()
        if death < birth:
            errors.append("Date of death cannot be earlier than date of birth.")
    except ValueError:
        errors.append("Please enter valid birth and death dates.")

    return errors, {
        "name": name,
        "date_of_birth": date_of_birth,
        "date_of_death": date_of_death,
        "content": content,
        "author": author,
    }


def excerpt(text, length=155):
    clean = " ".join(text.split())
    if len(clean) <= length:
        return clean
    return clean[: length - 3].rsplit(" ", 1)[0] + "..."


def obituary_schema(obituary):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"Obituary of {obituary['name']}",
        "description": excerpt(obituary["content"]),
        "author": {"@type": "Person", "name": obituary["author"]},
        "datePublished": obituary["submission_date"],
        "mainEntityOfPage": url_for("obituary_detail", slug=obituary["slug"], _external=True),
    }
    return json.dumps(data)


@app.route("/")
def home():
    return redirect(url_for("obituary_form"))


@app.route("/obituary_form.html")
def obituary_form():
    return render_template("obituary_form.html", form={})


@app.route("/submit_obituary", methods=["POST"])
def submit_obituary():
    init_db()
    errors, data = validate_obituary(request.form)
    if errors:
        for error in errors:
            flash(error, "error")
        return render_template("obituary_form.html", form=data), 400

    data["slug"] = unique_slug(data["name"])
    try:
        db = get_db()
        db.execute(
            """
            INSERT INTO obituaries
                (name, date_of_birth, date_of_death, content, author, slug)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["date_of_birth"],
                data["date_of_death"],
                data["content"],
                data["author"],
                data["slug"],
            ),
        )
        db.commit()
    except sqlite3.DatabaseError:
        app.logger.exception("Failed to save obituary")
        flash("The obituary could not be saved. Please try again.", "error")
        return render_template("obituary_form.html", form=data), 500

    flash("Obituary submitted successfully.", "success")
    return redirect(url_for("obituary_detail", slug=data["slug"]))


@app.route("/view_obituaries")
def view_obituaries():
    init_db()
    page = max(request.args.get("page", 1, type=int), 1)
    offset = (page - 1) * PER_PAGE
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM obituaries").fetchone()[0]
    obituaries = db.execute(
        """
        SELECT * FROM obituaries
        ORDER BY submission_date DESC, id DESC
        LIMIT ? OFFSET ?
        """,
        (PER_PAGE, offset),
    ).fetchall()
    total_pages = max((total + PER_PAGE - 1) // PER_PAGE, 1)
    return render_template(
        "view_obituaries.html",
        obituaries=obituaries,
        page=page,
        total_pages=total_pages,
    )


@app.route("/obituaries/<slug>")
def obituary_detail(slug):
    init_db()
    obituary = get_db().execute(
        "SELECT * FROM obituaries WHERE slug = ?",
        (slug,),
    ).fetchone()
    if obituary is None:
        abort(404)

    canonical_url = url_for("obituary_detail", slug=slug, _external=True)
    title = f"Obituary of {obituary['name']}"
    description = excerpt(obituary["content"])
    share_text = quote_plus(f"{title} - {canonical_url}")
    return render_template(
        "obituary_detail.html",
        obituary=obituary,
        title=title,
        description=description,
        canonical_url=canonical_url,
        share_text=share_text,
        schema_json=obituary_schema(obituary),
    )


@app.route("/sitemap.xml")
def sitemap():
    init_db()
    pages = [
        url_for("obituary_form", _external=True),
        url_for("view_obituaries", _external=True),
    ]
    rows = get_db().execute("SELECT slug FROM obituaries ORDER BY id DESC").fetchall()
    pages.extend(url_for("obituary_detail", slug=row["slug"], _external=True) for row in rows)
    xml_urls = "\n".join(f"  <url><loc>{escape(page)}</loc></url>" for page in pages)
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{xml_urls}\n"
        f"</urlset>\n",
        200,
        {"Content-Type": "application/xml; charset=utf-8"},
    )


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
