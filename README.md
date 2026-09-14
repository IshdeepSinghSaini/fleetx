# FleetX — Vehicle Rental & Fleet Analytics Platform

A full-stack vehicle rental platform where customers can browse, book, and review vehicles, admins can manage the fleet and users, and the underlying data is analyzed with SQL and Python.

Built as an intermediate-level project covering full-stack development (SDE), backend security, and data analytics.

## Features

**Customer**
- Register / login (JWT authentication, hashed passwords)
- Browse, search, and filter vehicles by type
- Check availability and book a vehicle for a date range
- View booking history and cancel a booking
- Simulated payment for a booking
- Leave a rating and review after a booking

**Admin**
- Add, update, and delete vehicles
- View and manage all bookings
- Manage users (view, change role, delete)
- Log and complete vehicle maintenance (auto-updates vehicle availability)
- Dashboard with revenue, active bookings, and fleet stats

**Security**
- JWT-based authentication
- Passwords hashed with BCrypt
- Role-based endpoint authorization (admin-only vs. any-logged-in-user routes enforced server-side)

**Analytics**
- SQL queries for revenue, popular vehicles, cancellation rate, vehicle utilization, and customer spend (`analytics/sql`)
- Python/Pandas script that pulls the same data and generates charts (`analytics/python`)

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, React Router, Axios |
| Backend | Java, Spring Boot, Spring Security |
| Database | PostgreSQL |
| Auth | JWT (jjwt), BCrypt |
| Analytics | SQL, Python, Pandas, Matplotlib |
| Tools | Git, Postman |

## Project Structure

```
FleetX/
├── backend/          Spring Boot backend
├── frontend/         React frontend
├── analytics/
│   ├── sql/          Analytics SQL queries
│   └── python/        Pandas analysis + chart generation
└── package.json      Root script to run backend + frontend together
```

## Running Locally

**Prerequisites:** Java 21+, Node.js, PostgreSQL running locally.

1. Create a PostgreSQL database named `fleetx`.
2. Copy `backend/src/main/resources/application.properties.example` to `application.properties` and fill in your database credentials.
3. From the project root, install dependencies once:
   ```bash
   npm install
   cd frontend && npm install
   ```
4. Start both the backend (`localhost:8080`) and frontend (`localhost:5173`) together:
   ```bash
   npm run dev
   ```

## Database Schema

Six related tables: `users`, `vehicles`, `bookings`, `payments`, `maintenance_logs`, `reviews` — tables are created automatically by Hibernate from the JPA entities on first run.

## API Overview

| Endpoint | Access |
|---|---|
| `POST /api/users/register`, `/login` | Public |
| `GET /api/vehicles`, `/api/reviews/**` | Public |
| `POST/PUT/DELETE /api/vehicles/**` | Admin only |
| `/api/maintenance/**` | Admin only |
| `GET/DELETE /api/users/**` | Admin only |
| `/api/bookings/**`, `/api/payments/**` | Any authenticated user |
