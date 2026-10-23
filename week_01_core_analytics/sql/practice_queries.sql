-- ============================================================================
-- BLUESTOCK FINTECH — WEEK 1 SQL PRACTICE SUITE
-- Author: Mayank Soni (Data Analyst Intern)
-- Topic: SQL Foundations to Advanced Analytical Windows & CTEs
-- Compatible with: SQLite 3, PostgreSQL, MySQL 8.0+
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SECTION 1: SCHEMA DEFINITIONS & SEED DATA (Self-Contained & Runnable)
-- ----------------------------------------------------------------------------

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment TEXT NOT NULL, -- 'Retail', 'Corporate', 'HNI'
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL, -- 'Terminal', 'API', 'Advisory', 'Analytics'
    unit_price NUMERIC(10, 2) NOT NULL,
    cost_price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    status TEXT NOT NULL, -- 'Completed', 'Pending', 'Cancelled'
    payment_method TEXT NOT NULL
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    discount_pct NUMERIC(5, 2) DEFAULT 0.00
);

-- Seed Customers
INSERT INTO customers (customer_id, customer_name, segment, city, state, signup_date) VALUES
(101, 'Aarav Mehta', 'Corporate', 'Mumbai', 'Maharashtra', '2024-01-15'),
(102, 'Priya Iyer', 'Retail', 'Bengaluru', 'Karnataka', '2024-02-10'),
(103, 'Vikram Malhotra', 'HNI', 'Delhi', 'Delhi', '2024-02-20'),
(104, 'Sneha Patel', 'Corporate', 'Ahmedabad', 'Gujarat', '2024-03-05'),
(105, 'Rohan Deshmukh', 'Retail', 'Pune', 'Maharashtra', '2024-03-18'),
(106, 'Ananya Roy', 'HNI', 'Kolkata', 'West Bengal', '2024-04-01'),
(107, 'Karan Singhal', 'Retail', 'Jaipur', 'Rajasthan', '2024-04-22'),
(108, 'Neha Joshi', 'Corporate', 'Hyderabad', 'Telangana', '2024-05-11');

-- Seed Products
INSERT INTO products (product_id, product_name, category, unit_price, cost_price) VALUES
(1, 'Bluestock Pro Terminal', 'Terminal', 45000.00, 28000.00),
(2, 'Market Data Streaming API', 'API', 25000.00, 12000.00),
(3, 'Portfolio Risk Optimizer', 'Analytics', 20000.00, 11000.00),
(4, 'Algo Strategy Builder', 'Analytics', 35000.00, 18000.00),
(5, 'Tax & Capital Gains Engine', 'Advisory', 15000.00, 7500.00),
(6, 'Retail Screener Pass', 'Terminal', 5000.00, 2000.00);

-- Seed Orders
INSERT INTO orders (order_id, customer_id, order_date, status, payment_method) VALUES
(1001, 101, '2024-06-01', 'Completed', 'Bank Transfer'),
(1002, 102, '2024-06-05', 'Completed', 'UPI'),
(1003, 103, '2024-06-12', 'Completed', 'Credit Card'),
(1004, 104, '2024-06-18', 'Completed', 'Bank Transfer'),
(1005, 101, '2024-07-02', 'Completed', 'Bank Transfer'),
(1006, 105, '2024-07-09', 'Cancelled', 'UPI'),
(1007, 106, '2024-07-15', 'Completed', 'Credit Card'),
(1008, 107, '2024-07-22', 'Completed', 'Debit Card'),
(1009, 108, '2024-08-01', 'Completed', 'Net Banking'),
(1010, 102, '2024-08-10', 'Completed', 'UPI'),
(1011, 103, '2024-08-15', 'Completed', 'Credit Card'),
(1012, 104, '2024-08-25', 'Pending', 'Bank Transfer');

-- Seed Order Items
INSERT INTO order_items (item_id, order_id, product_id, quantity, discount_pct) VALUES
(1, 1001, 1, 2, 0.05),
(2, 1001, 2, 1, 0.00),
(3, 1002, 6, 1, 0.00),
(4, 1003, 3, 1, 0.10),
(5, 1003, 4, 1, 0.05),
(6, 1004, 1, 3, 0.10),
(7, 1005, 2, 2, 0.00),
(8, 1006, 6, 2, 0.00),
(9, 1007, 4, 1, 0.00),
(10, 1008, 5, 1, 0.05),
(11, 1009, 1, 1, 0.00),
(12, 1009, 3, 1, 0.00),
(13, 1010, 6, 2, 0.10),
(14, 1011, 2, 1, 0.00),
(15, 1011, 4, 1, 0.05),
(16, 1012, 1, 1, 0.00);


-- ----------------------------------------------------------------------------
-- SECTION 2: ANALYTICAL SQL PRACTICE QUERIES
-- ----------------------------------------------------------------------------

-- QUERY 1: SELECT, WHERE, ORDER BY
-- Objective: Retrieve all completed orders from Corporate and HNI clients sorted by date descending.
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    c.segment,
    c.city,
    o.payment_method
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed' 
  AND c.segment IN ('Corporate', 'HNI')
ORDER BY o.order_date DESC;

-- QUERY 2: AGGREGATE FUNCTIONS & GROUP BY
-- Objective: Calculate total order count, total gross revenue, and average transaction size by customer segment.
SELECT 
    c.segment,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS total_net_revenue,
    ROUND(AVG(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS avg_item_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY c.segment
ORDER BY total_net_revenue DESC;

-- QUERY 3: HAVING CLAUSE
-- Objective: Identify high-performing product categories that generated over ₹50,000 in revenue.
SELECT 
    p.category,
    COUNT(DISTINCT oi.order_id) AS orders_count,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS net_category_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
HAVING SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)) > 50000
ORDER BY net_category_revenue DESC;

-- QUERY 4: MULTI-TABLE JOIN & PROFIT MARGIN ANALYSIS
-- Objective: Measure gross margin and net profit contribution per product.
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS net_revenue,
    ROUND(SUM(oi.quantity * p.cost_price), 2) AS total_cogs,
    ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)) - SUM(oi.quantity * p.cost_price), 2) AS net_profit,
    ROUND(
        (SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)) - SUM(oi.quantity * p.cost_price)) / 
        SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)) * 100, 
        2
    ) AS profit_margin_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY net_profit DESC;

-- QUERY 5: SUBQUERY (Scalar & Correlated)
-- Objective: Find all customers whose lifetime spending exceeds the company-wide average customer spend.
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    c.city,
    ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS customer_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id, c.customer_name, c.segment, c.city
HAVING customer_spend > (
    -- Subquery: Overall average customer spend
    SELECT AVG(cust_rev) 
    FROM (
        SELECT 
            c2.customer_id, 
            SUM(oi2.quantity * p2.unit_price * (1 - oi2.discount_pct)) AS cust_rev
        FROM customers c2
        JOIN orders o2 ON c2.customer_id = o2.customer_id
        JOIN order_items oi2 ON o2.order_id = oi2.order_id
        JOIN products p2 ON oi2.product_id = p2.product_id
        WHERE o2.status = 'Completed'
        GROUP BY c2.customer_id
    )
)
ORDER BY customer_spend DESC;

-- QUERY 6: WINDOW FUNCTION — ROW_NUMBER(), DENSE_RANK()
-- Objective: Rank customers within their respective segment by total spend.
WITH customer_spending AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT 
    customer_id,
    customer_name,
    segment,
    total_spend,
    ROW_NUMBER() OVER (PARTITION BY segment ORDER BY total_spend DESC) AS row_num,
    DENSE_RANK() OVER (PARTITION BY segment ORDER BY total_spend DESC) AS segment_rank
FROM customer_spending
ORDER BY segment, segment_rank;

-- QUERY 7: WINDOW FUNCTION — RUNNING TOTAL OVER TIME
-- Objective: Calculate daily order revenue along with cumulative running total revenue for 2024.
WITH daily_sales AS (
    SELECT 
        o.order_date,
        COUNT(DISTINCT o.order_id) AS orders_count,
        ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
    GROUP BY o.order_date
)
SELECT 
    order_date,
    orders_count,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM daily_sales
ORDER BY order_date;

-- QUERY 8: WINDOW FUNCTION — LAG() / LEAD() FOR MONTH-OVER-MONTH GROWTH
-- Objective: Measure month-over-month percentage growth in net revenue.
WITH monthly_revenue AS (
    SELECT 
        SUBSTR(o.order_date, 1, 7) AS sales_month,
        ROUND(SUM(oi.quantity * p.unit_price * (1 - oi.discount_pct)), 2) AS net_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'Completed'
    GROUP BY SUBSTR(o.order_date, 1, 7)
)
SELECT 
    sales_month,
    net_revenue,
    LAG(net_revenue, 1) OVER (ORDER BY sales_month) AS prev_month_revenue,
    ROUND(
        (net_revenue - LAG(net_revenue, 1) OVER (ORDER BY sales_month)) / 
        LAG(net_revenue, 1) OVER (ORDER BY sales_month) * 100, 
        2
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY sales_month;
