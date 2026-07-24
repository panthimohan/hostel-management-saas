# API Quick Reference

Base URL: `/api/`

## Auth
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/api/auth/owner-signup/` | Self-service signup for a **new hostel business** — creates a PENDING Organization + its first Hostel Owner user | Public |
| POST | `/api/auth/register/` | Register a user directly (used for adding staff/tenants to an *existing* org) | Public — see note below |
| POST | `/api/auth/login/` | Obtain JWT access + refresh token | Public |
| POST | `/api/auth/refresh/` | Refresh an access token | Public (valid refresh token) |
| POST | `/api/auth/logout/` | Blacklist a refresh token | Authenticated |
| GET/PATCH | `/api/auth/me/` | Get or update current user profile (role/org are read-only) | Authenticated |
| POST | `/api/auth/password-reset/` | Request a reset token (always returns a generic success message) | Public |
| POST | `/api/auth/password-reset/confirm/` | Confirm reset with `uid`, `token`, `new_password` | Public |

> **Known gap:** `/api/auth/register/` currently accepts any `role`/`organization` from an unauthenticated caller. It's fine for quick local testing, but before production use it should be locked down so only an authenticated Hostel Owner can invite Managers/Tenants into *their own* organization. Flagging this so it doesn't get missed.

## Organizations (Super Admin only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tenants/organizations/` | List all hostel businesses on the platform. Filter with `?status=PENDING` |
| GET | `/api/tenants/organizations/{id}/` | View one organization |
| POST | `/api/tenants/organizations/{id}/approve/` | Approve a pending signup → sets status `ACTIVE`, unlocking hostel/room/bed management for that owner |
| POST | `/api/tenants/organizations/{id}/reject/` | Reject a pending signup → sets status `CANCELLED` |
| POST | `/api/tenants/organizations/{id}/suspend/` | Suspend an active organization |
| POST | `/api/tenants/organizations/{id}/reactivate/` | Reactivate a suspended organization |

### The owner signup → approval flow
```
1. POST /api/auth/owner-signup/   (public) → Organization created with status=PENDING
2. Super Admin: GET /api/tenants/organizations/?status=PENDING
3. Super Admin: POST /api/tenants/organizations/{id}/approve/
4. Owner: POST /api/auth/login/  → hostel/room/bed endpoints now unlocked
```
Until step 3, the owner can log in and call `/api/auth/me/`, but any request to
`/api/hostels/`, `/api/rooms/`, or `/api/beds/` returns `403` with a message
explaining the organization isn't active yet (enforced by the `OrganizationIsActive`
permission class).

## Hostels
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET/POST | `/api/hostels/` | List / create hostels (scoped to your org) | Owner, Manager, Super Admin |
| GET/PUT/PATCH/DELETE | `/api/hostels/{id}/` | Retrieve / update / delete a hostel | Owner, Manager, Super Admin |

## Rooms
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/rooms/` | List / create rooms. Filter with `?hostel=`, `?status=`, `?room_type=` |
| GET/PUT/PATCH/DELETE | `/api/rooms/{id}/` | Manage a single room |

## Beds
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/beds/` | List / create beds. Filter with `?room=`, `?status=` |
| GET/PUT/PATCH/DELETE | `/api/beds/{id}/` | Manage a single bed |
| GET/POST | `/api/beds/allocations/` | List / create tenant-to-bed allocations |
| GET/PUT/PATCH/DELETE | `/api/beds/allocations/{id}/` | Manage a single allocation |

All endpoints (except register/login/refresh/password-reset) require:
`Authorization: Bearer <access_token>`

## Tenant profiles (KYC)
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET/POST | `/api/tenant-profiles/` | List/create tenant KYC profiles | Owner, Manager |
| GET/PATCH | `/api/tenant-profiles/me/` | A Tenant's own profile (auto-created on first access) | Tenant |

## Reservations / Booking
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET/POST | `/api/reservations/` | List/create bookings. Filter `?status=`, `?hostel=`, `?room=` | Owner, Manager, Receptionist |
| POST | `/api/reservations/{id}/confirm/` \| `/waitlist/` \| `/cancel/` | Status transitions | Owner, Manager, Receptionist |

## Rent & Payments
| Method | Endpoint | Description | Role |
|---|---|---|---|
| GET/POST | `/api/payments/invoices/` | Rent invoices per bed allocation (rent + deposit + utilities + late fee) | Owner, Manager, Accountant |
| GET | `/api/payments/invoices/outstanding_summary/` | Count + total outstanding for the filtered set | Owner, Manager, Accountant |
| GET/POST | `/api/payments/` | Record a payment (Cash/Bank/Card/Stripe/PayPal) — auto-recalculates invoice status | Owner, Manager, Accountant |

## Attendance
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/attendance/` | Daily attendance per tenant (Present/Absent/Leave/Late). One record per tenant per day. |

## Visitors
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/visitors/` | Log a visitor entry |
| POST | `/api/visitors/{id}/check_out/` | Stamp exit time |

## Complaints
| Method | Endpoint | Description | Role |
|---|---|---|---|
| POST | `/api/complaints/` | File a complaint (category: Water/Electricity/Internet/Cleaning/Maintenance/Other) | Tenant only |
| GET | `/api/complaints/` | List — Tenants see only their own; Owner/Manager see all in their org | Any authenticated |
| POST | `/api/complaints/{id}/start_progress/` \| `/resolve/` | Status transitions | Owner, Manager |

## Staff
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/staff/` | HR records (Manager/Receptionist/Accountant/Cleaner/Security/Cook). `user` link is optional. |

## Inventory
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/inventory/` | Assets per hostel (beds, mattresses, chairs, fans, etc.) with condition tracking |

Swagger/OpenAPI generation (e.g. via `drf-spectacular`) is a good next addition — not yet wired up in this milestone.
