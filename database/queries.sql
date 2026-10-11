-- ============================================================
-- RESTAURANT INFORMATION SYSTEM
-- 15 Management Queries for Data Analysis
-- Author: Ashley Mondela
-- Course: ITEC343 - Database Management Systems I
-- Cyprus International University
-- ============================================================


-- QUERY 1: Least and most expensive meals
SELECT name, price,
CASE WHEN price = (SELECT MIN(price) FROM meal) THEN 'Cheapest'
     WHEN price = (SELECT MAX(price) FROM meal) THEN 'Most Expensive'
END AS label
FROM meal
WHERE price = (SELECT MIN(price) FROM meal)
   OR price = (SELECT MAX(price) FROM meal);


-- QUERY 2: Number of meals in each category
SELECT c.name AS category, COUNT(m.meal_id) AS total_meals
FROM category c
JOIN meal m ON c.category_id = m.category_id
GROUP BY c.name
ORDER BY total_meals DESC;


-- QUERY 3: Most expensive meal in each category
SELECT c.name AS category, m.name AS meal, m.price
FROM meal m
JOIN category c ON m.category_id = c.category_id
WHERE m.price = (
    SELECT MAX(price) FROM meal
    WHERE category_id = m.category_id
)
ORDER BY m.price DESC;


-- QUERY 4: Number of orders on a specific date
SELECT date, COUNT(*) AS total_orders
FROM orders
WHERE date = '2024-05-01'
GROUP BY date;


-- QUERY 5: Customer who made the most expensive order
SELECT c.name AS customer, p.amount AS total_paid
FROM payment p
JOIN orders o ON p.order_id = o.order_id
JOIN customer c ON o.customer_id = c.customer_id
ORDER BY p.amount DESC
LIMIT 1;


-- QUERY 6: Highest tip received by which employee
SELECT e.name AS employee, e.role, MAX(o.tip) AS highest_tip
FROM orders o
JOIN employee e ON o.employee_id = e.employee_id
GROUP BY e.name, e.role
ORDER BY highest_tip DESC
LIMIT 1;


-- QUERY 7: Total revenue generated
SELECT SUM(amount) AS total_revenue
FROM payment;


-- QUERY 8: Top 5 most ordered meals
SELECT m.name AS meal, SUM(oi.quantity) AS times_ordered
FROM order_item oi
JOIN meal m ON oi.meal_id = m.meal_id
GROUP BY m.name
ORDER BY times_ordered DESC
LIMIT 5;


-- QUERY 9: Average rating per meal
SELECT m.name AS meal, ROUND(AVG(r.rating), 2) AS avg_rating
FROM rate r
JOIN meal m ON r.meal_id = m.meal_id
GROUP BY m.name
ORDER BY avg_rating DESC;


-- QUERY 10: Total tips earned by each employee
SELECT e.name AS employee, e.role, SUM(o.tip) AS total_tips
FROM orders o
JOIN employee e ON o.employee_id = e.employee_id
GROUP BY e.name, e.role
ORDER BY total_tips DESC;


-- QUERY 11: Most popular payment method
SELECT method, COUNT(*) AS total_transactions
FROM payment
GROUP BY method
ORDER BY total_transactions DESC;


-- QUERY 12: Customers who have made more than one order
SELECT c.name AS customer, COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customer c ON o.customer_id = c.customer_id
GROUP BY c.name
HAVING COUNT(o.order_id) > 1
ORDER BY total_orders DESC;


-- QUERY 13: Revenue per meal category
SELECT c.name AS category, SUM(p.amount) AS total_revenue
FROM payment p
JOIN orders o ON p.order_id = o.order_id
JOIN order_item oi ON o.order_id = oi.order_id
JOIN meal m ON oi.meal_id = m.meal_id
JOIN category c ON m.category_id = c.category_id
GROUP BY c.name
ORDER BY total_revenue DESC;


-- QUERY 14: Customers by country
SELECT country, COUNT(*) AS total_customers
FROM customer
GROUP BY country
ORDER BY total_customers DESC;


-- QUERY 15: Busiest month by number of orders
SELECT TO_CHAR(date, 'Month') AS month, COUNT(*) AS total_orders
FROM orders
GROUP BY TO_CHAR(date, 'Month'), EXTRACT(MONTH FROM date)
ORDER BY EXTRACT(MONTH FROM date);
