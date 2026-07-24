# Hostel Management SaaS — Foundation Build

This is a **working foundation** for a multi-tenant Hostel Management SaaS ERP, built with
Django + Django REST Framework + PostgreSQL + JWT auth + Docker.

## What's actually implemented in this milestone (real, runnable code)

**Core platform**
- Multi-tenant data model: every business table carries `organization`, `created_at`, `updated_at`
  via a shared `TenantModel` base class, with a `TenantManager` that scopes querysets to an
  organization so one hostel can never see another hostel's data.
- Custom `User` model with roles: `SUPER_ADMIN`, `HOSTEL_OWNER`, `HOSTEL_MANAGER`,
  `RECEPTIONIST`, `ACCOUNTANT`, `TENANT`.
- JWT auth (login with account lockout, refresh, logout), password reset (request/confirm),
  and profile management (`GET/PATCH /api/auth/me/`, role/org locked to prevent self-escalation).
- Owner self-signup (`/api/auth/owner-signup/`) creating a `PENDING` Organization, with a
  Super Admin approval workflow (`/api/tenants/organizations/{id}/approve|reject|suspend|reactivate/`).
  Business endpoints stay locked (`403`) until approval.
- Role-based permission classes (`permissions/roles.py`), including role-scoped variants:
  front-desk staff (Owner/Manager/Receptionist) vs accounting staff (Owner/Manager/Accountant).

**Business modules (each with real models, migrations, DRF viewsets, and tenant isolation)**
- **Hostels, Rooms, Beds** — full CRUD, room types, capacities, bed status tracking.
- **Tenant profiles (KYC)** — photo, emergency contact, ID document, university/course fields;
  tenants manage their own via `/api/tenant-profiles/me/`.
- **Bookings / Reservations** — pending → waitlisted/confirmed/cancelled workflow.
- **Rent & Payments** — invoices (rent + deposit + utilities + late fee) with an
  auto-computed outstanding balance; payments (Cash/Bank/Card/Stripe/PayPal) that
  automatically recalculate invoice status.
- **Attendance** — daily present/absent/leave/late per tenant.
- **Visitor management** — entry/exit logging per tenant.
- **Complaints** — tenants file & see only their own; Owner/Manager triage and resolve.
- **Staff (HR)** — Manager/Receptionist/Accountant/Cleaner/Security/Cook records.
- **Inventory** — beds, mattresses, furniture, appliances, with condition tracking.
- **Expenses & Income** — categorized expenses including a required-note **Miscellaneous**
  category, plus a `/summary/` endpoint for dashboard charts.

**Frontend** — a responsive React + Tailwind app (see `frontend/README.md`) covering
login, owner signup, Super Admin approvals, the owner/manager dashboard (occupancy +
expense chart), Hostels, Rooms & Beds, Expenses, and a Tenant dashboard.

- Automatic tenant isolation middleware attaches `request.organization` from the authenticated user.
- Dockerfile + docker-compose (Django + Postgres + Redis + Celery worker stub + Nginx).
- Pytest suite (12 files) covering auth, tenant isolation, owner signup/approval, expenses
  including the Miscellaneous-note requirement, payments/invoice status calculation, complaint
  visibility, and role-based access for the new modules.
- `.env.example`, no hardcoded secrets anywhere.

## What's intentionally NOT built yet (next milestones)

- **Reports** (PDF/Excel/CSV export of income, occupancy, tenant lists, etc.) — no export
  library wired up yet (ReportLab/ WeasyPrint/openpyxl).
- **Notifications** (email/SMS/WhatsApp reminders) — no Celery task/email backend wired up;
  password reset currently logs its token instead of emailing it.
- **Dashboard** metrics are partially built (occupancy, expenses); full metric set (recent
  check-ins, recent complaints, pending payments feed) still to come.
- Frontend pages for the 8 new backend modules (tenant profiles, bookings, payments,
  attendance, visitors, complaints, staff, inventory) — backend is ready, UI isn't yet.
- Stripe/PayPal are modeled as payment *methods* but not actually integrated as payment
  gateways (no webhook handling, no client-side checkout).

Tell me which one to build next.

## Quickstart

```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build
```

Then, in another terminal:

```bash
docker compose -f docker/docker-compose.yml exec backend python manage.py migrate
docker compose -f docker/docker-compose.yml exec backend python manage.py createsuperuser
```

API is available at `http://localhost:8000/api/`.

### Local (non-Docker) setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Run tests

```bash
cd backend
pytest --cov=apps
```

## Project structure

```
hostel_saas/
├── backend/
│   ├── config/            # Django settings, urls, wsgi, celery app
│   ├── apps/
│   │   ├── accounts/        # Custom User model, JWT auth, password reset
│   │   ├── tenants/         # Organization model + approval workflow
│   │   ├── hostels/         # Hostel model + API
│   │   ├── rooms/           # Room model + API
│   │   ├── beds/            # Bed + BedAllocation + tenant "my room" view
│   │   ├── tenant_profiles/ # Tenant KYC profiles
│   │   ├── bookings/        # Reservations / waiting list
│   │   ├── payments/        # Rent invoices + payments
│   │   ├── attendance/      # Daily attendance
│   │   ├── visitors/        # Visitor log
│   │   ├── complaints/      # Tenant complaints
│   │   ├── staff/           # Staff HR records
│   │   ├── inventory/       # Asset tracking
│   │   └── expenses/        # Expenses (incl. Miscellaneous) + Income
│   ├── api/                # Root API router/urls
│   ├── permissions/         # Role-based DRF permission classes
│   ├── middleware/          # Tenant-context middleware
│   ├── utils/                # Shared base models/mixins
│   └── tests/               # Pytest suite (12 files)
├── frontend/                # React + Tailwind SPA — see frontend/README.md
├── docker/                  # Dockerfile, docker-compose.yml
├── nginx/                   # nginx.conf
├── docs/                    # API reference
├── .env.example
└── README.md
```

## Security notes

- All secrets are read from environment variables (`config/settings.py` uses `os.environ`/`django-environ`).
- Passwords hashed via Django's default PBKDF2 (upgradeable to Argon2 by adding `argon2-cffi`).
- `SECRET_KEY`, DB credentials, and JWT signing key are never committed — see `.env.example`.

# hostel-management-saas
Multi-tenant Hostel Management SaaS ERP built with Django REST Framework, React, PostgreSQL, and Docker.
