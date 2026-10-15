# Restaurant Information System

A complete relational database system and secure backend API for managing a multi-cuisine restaurant, built with PostgreSQL 18 and FastAPI.

---

## Project Overview

This project was developed as part of the Database Management Systems I (ITEC343) course at **Cyprus International University**. It combines a 14-table PostgreSQL database with a secure RESTful FastAPI backend to simulate a real-world restaurant management system-handling menu items, orders, payments, reservations, and customer ratings.

---

## Live Demo & API Documentation

The backend API is deployed and hosted live on the cloud via Render:
- **Interactive Swagger UI Documentation:** [https://restaurant-api-qfpz.onrender.com/docs](https://restaurant-api-qfpz.onrender.com/docs)

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

## Database Stats

- 14 tables
- 40 meals across 5 cuisines
- 81 ingredients
- 30 customers from 15+ countries
- 10 employees
- 30 orders with payments and tips
- 15 management queries for data analysis

---

## Technologies Used

- Python & FastAPI (RESTful API, OAuth2, JWT Security & Rate Limiting)
- PostgreSQL 18 & pgAdmin 4
- SQLAlchemy & Pydantic
- Render (Cloud Web Service Deployment)

---

## Repository Structure

```
restaurant-management-system-fullstack/
├── app/                # FastAPI backend source code & security
├── database/           # PostgreSQL SQL scripts & DDL/DML
├── docs/               # ER diagrams & documentation assets
├── .env                # Environment configuration (Local)
├── .gitignore          # Git exclusion rules
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

---

## How to Run Locally

1. **Database Setup:**
   - Install PostgreSQL 18 from [postgresql.org](https://www.postgresql.org/download)
   - Open pgAdmin 4, create a database called `restaurant_db`, and run `database/restaurant_db.sql` along with `database/queries.sql`.

2. **Backend API Setup:**
   - Set up your virtual environment and install dependencies: `pip install -r requirements.txt`
   - Configure your local `.env` file with your database URL, secret keys, and settings.
   - Run the FastAPI application using Uvicorn: `uvicorn app.main:app --reload`
   - Access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

   ## Environment Configuration

1. Clone the repository.
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   
   - Fill in your Supabase PostgreSQL credentials, GitHub OAuth App client keys, and generate a secure SECRET_KEY.



---

## Author

**Ashley Mondela**
- 3rd Year Information Technologies Student
- Cyprus International University
- ISC2 Certified in Cybersecurity (CC)
- [LinkedIn](https://www.linkedin.com/in/ashley-mondela-b2a5a4218/)
