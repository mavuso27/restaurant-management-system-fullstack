# Restaurant Information System

A complete relational database system and secure backend API for managing a multi-cuisine restaurant, built with PostgreSQL 18 and FastAPI.

---

## Project Overview

This project was originally developed as part of the Database Management Systems I (ITEC343) course at **Cyprus International University**. What started as a basic 5-table academic schema was independently expanded into a comprehensive 14-table PostgreSQL database combined with a secure, production-grade RESTful FastAPI backend to simulate a real-world restaurant management system—handling multi-cuisine menus, orders, payments, table reservations, and customer ratings.

---

## Live Demo & API Documentation

The backend API is deployed and hosted live on the cloud via Render:
- **Interactive Swagger UI Documentation:** [https://restaurant-api-qfpz.onrender.com/docs](https://restaurant-api-qfpz.onrender.com/docs)

---

## Security & Production Features

- **Authentication & Authorization:** OAuth 2.0 via GitHub authentication with CSRF state verification, backed by short-lived JWT session tokens.
- **Role-Based Access Control (RBAC):** Distinct administrative privileges for managing data versus customer-level access.
- **BOLA Prevention:** Strict user-level isolation ensuring customers can only access and modify their own records.
- **Rate Limiting:** Implemented via `SlowAPI` to prevent brute force and denial-of-service attacks on all endpoints.
- **Database Security:** Parameterized queries via SQLAlchemy ORM to completely eliminate SQL injection vulnerabilities.
- **Security Headers:** Enforced via custom middleware (HSTS, Content Security Policy, X-Frame-Options, X-Content-Type-Options).

---

## Database Structure

The system contains **14 tables:**

| Table | Description |
|-------|-------------|
| category | Meal categories |
| meal | Restaurant menu items |
| ingredient | All ingredients used in meals |
| meal_ingre | Links meals to their ingredients |
| supplier | Ingredient suppliers |
| supplier_ingredient | Links suppliers to ingredients |
| tables | Restaurant tables |
| employee | Restaurant staff |
| customer | Customer details |
| orders | Customer orders |
| order_item | Meals within each order |
| payment | Order payments |
| reservation | Table reservations |
| rate | Customer meal ratings |

---

## Relational Model

```
category (category_id PK, name)

ingredient (ing_no PK, name, amount, unit)

supplier (supplier_id PK, name, phone, address, email, created_at)

supplier_ingredient (supplier_id PK FK → supplier, ing_no PK FK → ingredient)

tables (table_id PK, capacity, location, status)

employee (employee_id PK, name, role, phone, address, salary, hire_date)

customer (customer_id PK, name, phone, address, email, country, join_date)

meal (meal_id PK, name, price, time, category_id FK → category)

meal_ingre (meal_id PK FK → meal, ing_no PK FK → ingredient)

orders (order_id PK, date, time, tip, customer_id FK → customer, 
        employee_id FK → employee, table_id FK → tables)

order_item (order_item_id PK, quantity, order_id FK → orders, meal_id FK → meal)

payment (payment_id PK, payment_date, method, amount, order_id FK → orders)

reservation (reservation_id PK, date, time, status, 
             customer_id FK → customer, table_id FK → tables)

rate (rate_id PK, rating, comment, customer_id FK → customer, meal_id FK → meal)
```

---

## Cuisines Available

- Chinese
- Italian
- Mexican
- Turkish
- Zimbabwean (Ndebele dishes)

---

## Database Stats & Capabilities

- 14 tables with robust relational constraints
- 40 meals spanning 5 distinct global cuisines
- 81 unique ingredients tracked via supply-chain mapping
- 30 customers from 15+ countries
- 10 restaurant staff members
- 30 tracked orders complete with payment processing and employee tipping
- 15 analytical management queries built for operational data analysis

---

## Technologies Used

- **Backend Framework:** Python & FastAPI (RESTful API, OAuth2, JWT Security & Rate Limiting)
- **Database:** PostgreSQL 18, Supabase (Cloud DB Hosting), & pgAdmin 4
- **ORM & Validation:** SQLAlchemy & Pydantic
- **Deployment:** Render (Cloud Web Service)

---

## Repository Structure

```
restaurant-management-system-fullstack/
├── app/                # FastAPI backend source code & security routers
├── database/           # PostgreSQL SQL scripts & DDL/DML data
├── docs/               # ER diagrams & documentation assets
├── .env.example        # Environment variable template
├── .gitignore          # Git exclusion rules
├── README.md           # Project documentation
└── requirements.txt    # Python package dependencies
```

---

## How to Run Locally

1. **Clone the Repository & Environment Setup:**
   ```bash
   git clone https://github.com/mavuso27/restaurant-management-system-fullstack.git
   cd restaurant-management-system-fullstack
   ```

2. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Fill in your local PostgreSQL / Supabase credentials, GitHub OAuth App client keys, and generate a secure `SECRET_KEY`.

3. **Database Setup:**
   - Install PostgreSQL 18 from [postgresql.org](https://www.postgresql.org/download)
   - Open pgAdmin 4, create a database called `restaurant_db`, and execute `database/restaurant_db.sql` along with `database/queries.sql`.

4. **Run the Backend API:**
   - Set up your virtual environment and install dependencies: 
     ```bash
     pip install -r requirements.txt
     ```
   - Run the FastAPI application using Uvicorn: 
     ```bash
     uvicorn app.main:app --reload
     ```
   - Access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

---

## Author

**Ashley Mondela**
- 3rd Year Information Technologies Student, Cyprus International University
- ISC2 Certified in Cybersecurity (CC)
- [LinkedIn Profile](https://www.linkedin.com/in/ashley-mondela-b2a5a4218/)