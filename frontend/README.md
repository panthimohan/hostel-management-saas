# Nestled — Frontend

A responsive React + Tailwind frontend for the Hostel SaaS backend. Works on
phone, tablet, and desktop browsers — no native mobile app, by design.

## Pages included in this milestone

- **Login** — JWT login, split hero panel on desktop, stacks on mobile
- **Owner signup** — public self-service registration for a new hostel business
- **Super Admin dashboard** — review & approve/reject/suspend organizations
- **Owner/Manager dashboard** — occupancy stats + live expense-category chart
- **Hostels** — list + add hostel locations
- **Rooms & Beds** — tabbed management with status key-tags
- **Expenses** — log expenses by category (including Miscellaneous, which
  requires a short note), filter by category, see totals
- **Tenant dashboard** — a tenant's own room/bed/rate + stay history

## Design system

- Palette: fog background, deep-teal primary, brass accent, moss (available/paid),
  clay (alerts/overdue) — see `tailwind.config.js`.
- Type: Fraunces (headings), IBM Plex Sans (UI/body), IBM Plex Mono (numbers, IDs).
- Signature element: the **key-tag** badge (`src/components/KeyTag.jsx`) — a pill
  shape with a punched hole at one edge, like a physical room-key fob. Used for
  every status indicator across the app.
- Layout: sidebar nav on tablet/desktop (`≥768px`), bottom tab bar on mobile.

## Running it

```bash
cd frontend
cp .env.example .env      # point at your backend, default is localhost:8000
npm install
npm run dev
```

Opens at `http://localhost:5173`. Make sure the Django backend (see
`../backend/README.md` or the root `README.md`) is running and `CORS_ALLOWED_ORIGINS`
in the backend's `.env` includes `http://localhost:5173`.

```bash
npm run build     # production build to dist/
npm run preview   # preview the production build locally
```

## What's not built yet

Payments/rent collection UI, tenant KYC/document upload, complaints,
notifications, and attendance don't have pages yet — they can follow the same
pattern (a page + the matching backend viewset) once those backend modules exist.
