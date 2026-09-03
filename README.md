# Grocery Store Management System

A full-stack inventory, sales, and online ordering system built for a real
grocery store — designed as a portfolio project covering Python, SQL,
Docker, AWS, and CI/CD.

## Roadmap

- **Phase 1** — Core app: product/stock management + customer ordering (Flask + SQLite)
- **Phase 2** — Insights dashboard: sales trends, top products (pandas + Streamlit)
- **Phase 3** — Cloud deployment: Docker, AWS RDS, EC2, GitHub Actions CI/CD, S3 backups
- **Phase 4** — (Optional) Notifications, payment integration

## Tech Stack

- Backend: Python, Flask
- Database: SQLite (dev) → PostgreSQL on AWS RDS (production)
- Frontend: Jinja2 templates + Bootstrap
- Analytics: pandas, Streamlit
- DevOps: Docker, GitHub Actions, AWS (EC2, RDS, S3)

## Local Setup

```bash
pip install -r requirements.txt
python run.py
```

Visit `http://localhost:5000`

## Project Structure

See `docs/structure.md`
