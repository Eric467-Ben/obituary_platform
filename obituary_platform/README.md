# Obituary Platform

This is a Flask web application for submitting, storing, displaying, and sharing obituaries. It uses SQLite for the `obituary_platform` database and includes SEO and social media optimization features.

## Features

- Chosen framework: Flask
- Chosen database: SQLite
- Obituary submission form at `/obituary_form.html`
- POST submission handler at `/submit_obituary`
- Paginated obituary listing at `/view_obituaries`
- Individual obituary detail pages with unique slugs
- SQLite database table named `obituaries`
- Client-side and server-side validation
- Dynamic title, description, keywords, canonical tags, Open Graph tags, and Twitter card tags
- Schema.org JSON-LD structured data
- Social sharing buttons for Facebook, X/Twitter, LinkedIn, and WhatsApp
- XML sitemap at `/sitemap.xml`

## Project Structure

```text
obituary_platform/
├── app.py
├── obituary_platform.db
├── requirements.txt
├── schema.sql
├── static/
│   ├── css/styles.css
│   └── js/validation.js
└── templates/
    ├── base.html
    ├── obituary_detail.html
    ├── obituary_form.html
    └── view_obituaries.html
```

## Environment Setup

Create and activate a virtual environment:

```bash
cd /home/stein/obituary_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Initialize the database:

```bash
.venv/bin/python -m flask --app app init-db
```

Run the local development server:

```bash
.venv/bin/python -m flask --app app run --debug
```

Open the application in a browser:

```text
http://127.0.0.1:5000/obituary_form.html
```

## Database

The application creates `obituary_platform.db` and the `obituaries` table automatically. The table contains:

- `id`
- `name`
- `date_of_birth`
- `date_of_death`
- `content`
- `author`
- `submission_date`
- `slug`

The SQL structure is documented in `schema.sql`.

SQLite is file-based, so it does not require a separate database service like MySQL or PostgreSQL. Running the `init-db` command creates the database file and table locally.

## Assignment Requirement Checklist

| Requirement | Where it is implemented |
| --- | --- |
| Development environment | `.venv`, `requirements.txt`, and setup commands above |
| Framework installed | Flask in `requirements.txt` |
| Database named `obituary_platform` | Local SQLite database file `obituary_platform.db` |
| `obituaries` table | `app.py` `init_db()` and `schema.sql` |
| Form file named `obituary_form.html` | `templates/obituary_form.html` |
| Fields for name, birth date, death date, content, author | `templates/obituary_form.html` |
| POST action to `submit_obituary` | Form posts to `/submit_obituary` |
| CSS styling | `static/css/styles.css` |
| JavaScript validation | `static/js/validation.js` |
| Backend data submission | `submit_obituary()` route in `app.py` |
| Backend data retrieval | `view_obituaries()` route in `app.py` |
| HTML table display | `templates/view_obituaries.html` |
| Pagination | `view_obituaries()` route and pagination links |
| Dynamic SEO tags | `templates/base.html` and `templates/obituary_detail.html` |
| Structured data | JSON-LD in `templates/obituary_detail.html` |
| Open Graph social tags | `templates/obituary_detail.html` |
| Social sharing buttons | `templates/obituary_detail.html` |
| Canonical tags | `templates/base.html` and `templates/obituary_detail.html` |
| XML sitemap | `/sitemap.xml` route in `app.py` |
| Error handling | Validation and database exception handling in `app.py` |

## Testing and Validation

1. Open `/obituary_form.html`.
2. Submit an obituary with valid names, dates, content, and author details.
3. Confirm that the app redirects to the new obituary detail page.
4. Open `/view_obituaries` and confirm the submitted record appears in the table.
5. Try invalid inputs such as empty fields, short content, or a death date earlier than birth date.
6. Open `/sitemap.xml` to confirm the obituary page URLs are listed.
7. Inspect the obituary detail page source to confirm dynamic SEO, Open Graph, canonical, and JSON-LD tags.

## GitHub Submission

Create a repository on GitHub, then run:

```bash
cd /home/stein/obituary_platform
git init
git add .
git commit -m "Build obituary platform assignment"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Share the GitHub repository URL with the lecturer.
