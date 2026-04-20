-- ================================================================
-- SAP Order-to-Cash (O2C) Analytics SQL Queries
-- Company  : NovaTech Solutions Pvt. Ltd.
-- Database : SQLite (simulating SAP BW / Datasphere analytical layer)
-- Author   : SAP Data Analytics Engineer - Capstone Project
-- ================================================================

-- ────────────────────────────────────────────
-- KPI 1: Total Revenue & Orders (Overall)
-- ────────────────────────────────────────────
SELECT
    COUNT(so_number)                    AS total_orders,
    SUM(order_total)                    AS gross_revenue,
    AVG(order_total)                    AS avg_order_value,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(so_number), 2
    )                                   AS cancellation_rate_pct
FROM fact_orders;

-- ────────────────────────────────────────────
-- KPI 2: Monthly Revenue Trend
-- ────────────────────────────────────────────
SELECT
    order_month,
    COUNT(so_number)       AS orders_placed,
    SUM(order_total)       AS monthly_revenue,
    AVG(order_total)       AS avg_order_value,
    SUM(SUM(order_total)) OVER (ORDER BY order_month) AS cumulative_revenue
FROM fact_orders
WHERE status != 'Cancelled'
GROUP BY order_month
ORDER BY order_month;

-- ────────────────────────────────────────────
-- KPI 3: Revenue by Region
-- ────────────────────────────────────────────
SELECT
    region,
    COUNT(so_number)   AS total_orders,
    SUM(order_total)   AS total_revenue,
    ROUND(
        100.0 * SUM(order_total) /
        SUM(SUM(order_total)) OVER (), 2
    )                  AS revenue_share_pct
FROM fact_orders
WHERE status != 'Cancelled'
GROUP BY region
ORDER BY total_revenue DESC;

-- ────────────────────────────────────────────
-- KPI 4: Top 10 Customers by Revenue
-- ────────────────────────────────────────────
SELECT
    customer_id,
    customer_name,
    region,
    COUNT(so_number)   AS total_orders,
    SUM(order_total)   AS total_revenue,
    AVG(order_total)   AS avg_order_value,
    RANK() OVER (ORDER BY SUM(order_total) DESC) AS revenue_rank
FROM fact_orders
WHERE status != 'Cancelled'
GROUP BY customer_id, customer_name, region
ORDER BY total_revenue DESC
LIMIT 10;

-- ────────────────────────────────────────────
-- KPI 5: Product Category Performance
-- ────────────────────────────────────────────
SELECT
    oi.category,
    SUM(oi.quantity)        AS total_units_sold,
    SUM(oi.line_total)      AS category_revenue,
    ROUND(AVG(oi.discount_pct), 2) AS avg_discount_pct,
    ROUND(
        100.0 * SUM(oi.line_total) /
        SUM(SUM(oi.line_total)) OVER (), 2
    )                       AS revenue_share_pct
FROM fact_order_items oi
JOIN fact_orders o ON oi.so_number = o.so_number
WHERE o.status != 'Cancelled'
GROUP BY oi.category
ORDER BY category_revenue DESC;

-- ────────────────────────────────────────────
-- KPI 6: Order Status Distribution (O2C Health)
-- ────────────────────────────────────────────
SELECT
    status,
    COUNT(so_number)    AS order_count,
    SUM(order_total)    AS total_value,
    ROUND(
        100.0 * COUNT(so_number) / SUM(COUNT(so_number)) OVER (), 2
    )                   AS percentage
FROM fact_orders
GROUP BY status
ORDER BY order_count DESC;

-- ────────────────────────────────────────────
-- KPI 7: Delivery Performance by Carrier
-- ────────────────────────────────────────────
SELECT
    carrier,
    COUNT(delivery_number)      AS total_shipments,
    ROUND(AVG(lead_time_days), 1) AS avg_lead_time_days,
    MIN(lead_time_days)         AS min_days,
    MAX(lead_time_days)         AS max_days,
    SUM(CASE WHEN delivery_status = 'Goods Issued' THEN 1 ELSE 0 END) AS delivered_count
FROM fact_deliveries
GROUP BY carrier
ORDER BY avg_lead_time_days;

-- ────────────────────────────────────────────
-- KPI 8: Payment / DSO Analysis
-- ────────────────────────────────────────────
SELECT
    payment_status,
    COUNT(invoice_number)   AS invoice_count,
    SUM(total_with_gst)     AS total_amount_incl_gst,
    ROUND(AVG(days_to_pay), 1) AS avg_days_to_pay
FROM fact_invoices
GROUP BY payment_status;

-- ────────────────────────────────────────────
-- KPI 9: Quarterly Revenue Comparison
-- ────────────────────────────────────────────
SELECT
    order_quarter,
    order_year,
    COUNT(so_number)    AS total_orders,
    SUM(order_total)    AS quarterly_revenue,
    AVG(order_total)    AS avg_order_value
FROM fact_orders
WHERE status != 'Cancelled'
GROUP BY order_quarter, order_year
ORDER BY order_quarter;

-- ────────────────────────────────────────────
-- KPI 10: Top 5 Products by Revenue
-- ────────────────────────────────────────────
SELECT
    oi.product_id,
    oi.product_name,
    oi.category,
    SUM(oi.quantity)      AS total_units,
    SUM(oi.line_total)    AS total_revenue
FROM fact_order_items oi
JOIN fact_orders o ON oi.so_number = o.so_number
WHERE o.status != 'Cancelled'
GROUP BY oi.product_id, oi.product_name, oi.category
ORDER BY total_revenue DESC
LIMIT 5;
