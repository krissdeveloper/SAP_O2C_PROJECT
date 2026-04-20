"""
SAP O2C ETL Pipeline
Extracts CSV data → Transforms → Loads into SQLite (simulating SAP BW/Datasphere layer)
Company: NovaTech Solutions Pvt. Ltd.
"""

import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH  = os.path.join(BASE_DIR, 'database', 'o2c_analytics.db')

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ─── EXTRACT ────────────────────────────────
print("📥 EXTRACT: Loading CSVs...")
customers    = pd.read_csv(f"{DATA_DIR}/customers.csv")
products     = pd.read_csv(f"{DATA_DIR}/products.csv")
sales_orders = pd.read_csv(f"{DATA_DIR}/sales_orders.csv")
order_items  = pd.read_csv(f"{DATA_DIR}/order_items.csv")
deliveries   = pd.read_csv(f"{DATA_DIR}/deliveries.csv")
invoices     = pd.read_csv(f"{DATA_DIR}/invoices.csv")

# ─── TRANSFORM ──────────────────────────────
print("🔄 TRANSFORM: Enriching data...")

# Add quarter
sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
sales_orders['order_quarter'] = sales_orders['order_date'].dt.to_period('Q').astype(str)
sales_orders['order_date'] = sales_orders['order_date'].dt.strftime('%Y-%m-%d')

# Delivery lead time
deliveries['dispatch_date']  = pd.to_datetime(deliveries['dispatch_date'])
deliveries['delivery_date']  = pd.to_datetime(deliveries['delivery_date'])
deliveries['lead_time_days'] = (deliveries['delivery_date'] - deliveries['dispatch_date']).dt.days
deliveries['dispatch_date']  = deliveries['dispatch_date'].dt.strftime('%Y-%m-%d')
deliveries['delivery_date']  = deliveries['delivery_date'].dt.strftime('%Y-%m-%d')

# DSO (Days Sales Outstanding)
invoices['invoice_date'] = pd.to_datetime(invoices['invoice_date'])
invoices['due_date']     = pd.to_datetime(invoices['due_date'])
invoices['invoice_date'] = invoices['invoice_date'].dt.strftime('%Y-%m-%d')
invoices['due_date']     = invoices['due_date'].dt.strftime('%Y-%m-%d')

# ─── LOAD ────────────────────────────────────
print("📤 LOAD: Writing to SQLite database...")
conn = sqlite3.connect(DB_PATH)

customers.to_sql('dim_customers',    conn, if_exists='replace', index=False)
products.to_sql('dim_products',      conn, if_exists='replace', index=False)
sales_orders.to_sql('fact_orders',   conn, if_exists='replace', index=False)
order_items.to_sql('fact_order_items', conn, if_exists='replace', index=False)
deliveries.to_sql('fact_deliveries', conn, if_exists='replace', index=False)
invoices.to_sql('fact_invoices',     conn, if_exists='replace', index=False)

# ─── ANALYTICS VIEWS ────────────────────────
print("📊 Creating analytics views...")

conn.execute("DROP VIEW IF EXISTS vw_revenue_by_month")
conn.execute("""
CREATE VIEW vw_revenue_by_month AS
SELECT
    order_month,
    order_year,
    COUNT(so_number)      AS total_orders,
    SUM(order_total)      AS total_revenue,
    AVG(order_total)      AS avg_order_value,
    SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM fact_orders
GROUP BY order_month, order_year
ORDER BY order_month;
""")

conn.execute("DROP VIEW IF EXISTS vw_revenue_by_region")
conn.execute("""
CREATE VIEW vw_revenue_by_region AS
SELECT
    region,
    COUNT(so_number)  AS total_orders,
    SUM(order_total)  AS total_revenue,
    AVG(order_total)  AS avg_order_value
FROM fact_orders
WHERE status != 'Cancelled'
GROUP BY region
ORDER BY total_revenue DESC;
""")

conn.execute("DROP VIEW IF EXISTS vw_top_customers")
conn.execute("""
CREATE VIEW vw_top_customers AS
SELECT
    o.customer_id,
    o.customer_name,
    o.region,
    COUNT(o.so_number)    AS total_orders,
    SUM(o.order_total)    AS total_revenue,
    AVG(o.order_total)    AS avg_order_value
FROM fact_orders o
WHERE o.status != 'Cancelled'
GROUP BY o.customer_id, o.customer_name, o.region
ORDER BY total_revenue DESC
LIMIT 10;
""")

conn.execute("DROP VIEW IF EXISTS vw_product_performance")
conn.execute("""
CREATE VIEW vw_product_performance AS
SELECT
    oi.category,
    oi.product_name,
    SUM(oi.quantity)      AS total_qty_sold,
    SUM(oi.line_total)    AS total_revenue,
    AVG(oi.discount_pct)  AS avg_discount_pct
FROM fact_order_items oi
JOIN fact_orders o ON oi.so_number = o.so_number
WHERE o.status != 'Cancelled'
GROUP BY oi.category, oi.product_name
ORDER BY total_revenue DESC;
""")

conn.execute("DROP VIEW IF EXISTS vw_order_status_summary")
conn.execute("""
CREATE VIEW vw_order_status_summary AS
SELECT
    status,
    COUNT(so_number)  AS count,
    SUM(order_total)  AS total_value
FROM fact_orders
GROUP BY status;
""")

conn.execute("DROP VIEW IF EXISTS vw_delivery_performance")
conn.execute("""
CREATE VIEW vw_delivery_performance AS
SELECT
    carrier,
    COUNT(delivery_number)     AS total_shipments,
    AVG(lead_time_days)        AS avg_lead_time,
    MIN(lead_time_days)        AS min_lead_time,
    MAX(lead_time_days)        AS max_lead_time
FROM fact_deliveries
GROUP BY carrier
ORDER BY avg_lead_time;
""")

conn.execute("DROP VIEW IF EXISTS vw_payment_performance")
conn.execute("""
CREATE VIEW vw_payment_performance AS
SELECT
    payment_status,
    COUNT(invoice_number) AS count,
    SUM(total_with_gst)   AS total_amount
FROM fact_invoices
GROUP BY payment_status;
""")

conn.commit()
conn.close()

print("✅ ETL Pipeline complete! Database ready at:", DB_PATH)

# ─── QUICK VALIDATION ───────────────────────
conn = sqlite3.connect(DB_PATH)
print("\n📋 Database Summary:")
for tbl in ['fact_orders','fact_order_items','fact_deliveries','fact_invoices',
            'dim_customers','dim_products']:
    cnt = pd.read_sql(f"SELECT COUNT(*) as c FROM {tbl}", conn).iloc[0,0]
    print(f"   {tbl:<25}: {cnt} rows")

print("\n📈 Revenue by Region:")
print(pd.read_sql("SELECT * FROM vw_revenue_by_region", conn).to_string(index=False))
conn.close()
