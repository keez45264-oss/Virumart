# Project Structure

```
grocery-app/
├── app/
│   ├── __init__.py          # App factory, registers routes
│   ├── models/
│   │   └── schema.sql       # Database schema (all tables)
│   ├── routes/
│   │   ├── customer.py      # Customer-facing: home, cart, checkout
│   │   └── admin.py         # Admin-facing: dashboard, products, orders
│   ├── templates/
│   │   ├── base.html        # Shared layout (navbar, Bootstrap)
│   │   ├── index.html       # Product listing page
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── products.html
│   │       └── orders.html
│   └── static/
│       ├── css/style.css
│       ├── js/               # (empty for now — add cart JS later)
│       └── images/           # product photos
├── database/
│   └── grocery.db            # SQLite file (created on first run)
├── docs/
│   └── structure.md          # This file
├── .github/workflows/
│   └── deploy.yml            # CI/CD pipeline (Phase 3)
├── Dockerfile                # Containerization (Phase 3)
├── requirements.txt
├── run.py                    # Entry point: python run.py
└── README.md
```

## Notes

- `database/` is gitignored in real setup (don't commit the .db file)
- `models/schema.sql` is run once to initialize tables — a `db_init.py`
  script will be added in the next step to do this automatically
- Templates are split customer vs admin so styling/permissions can diverge later
