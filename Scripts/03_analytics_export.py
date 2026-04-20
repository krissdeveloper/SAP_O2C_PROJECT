"""
Analytics Script - Extracts all KPIs from SQLite for dashboard embedding
"""
import sqlite3
import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'database', 'o2c_analytics.db')

conn = sqlite3.connect(DB_PATH)

# ── KPI 1: Overall summary ──────────────────────────────────────
kpi_summary = pd.read_sql("""
SELECT
    COUNT(so_number)                    AS total_orders,
    ROUND(SUM(order_total))             AS gross_revenue,
    ROUND(AVG(order_total))             AS avg_order_value,
    SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END)     AS cancelled_orders,
    SUM(CASE WHEN status IN ('Completed','Delivered') THEN 1 ELSE 0 END) AS completed_orders
FROM fact_orders
""", conn).iloc[0]

# ── KPI 2: Monthly Revenue ──────────────────────────────────────
monthly = pd.read_sql("""
SELECT order_month, ROUND(SUM(order_total)) AS monthly_revenue, COUNT(so_number) AS order_count
FROM fact_orders WHERE status != 'Cancelled'
GROUP BY order_month ORDER BY order_month
""", conn)

# ── KPI 3: Revenue by Region ────────────────────────────────────
region = pd.read_sql("""
SELECT region, ROUND(SUM(order_total)) AS total_revenue, COUNT(*) AS total_orders
FROM fact_orders WHERE status!='Cancelled'
GROUP BY region ORDER BY total_revenue DESC
""", conn)

# ── KPI 4: Top 10 Customers ─────────────────────────────────────
top_customers = pd.read_sql("""
SELECT customer_name, ROUND(SUM(order_total)) AS total_revenue, COUNT(*) AS total_orders
FROM fact_orders WHERE status!='Cancelled'
GROUP BY customer_id, customer_name ORDER BY total_revenue DESC LIMIT 10
""", conn)

# ── KPI 5: Category Revenue ─────────────────────────────────────
category_rev = pd.read_sql("""
SELECT oi.category, ROUND(SUM(oi.line_total)) AS category_revenue, SUM(oi.quantity) AS units_sold
FROM fact_order_items oi JOIN fact_orders o ON oi.so_number=o.so_number
WHERE o.status!='Cancelled'
GROUP BY oi.category ORDER BY category_revenue DESC
""", conn)

# ── KPI 6: Order Status ─────────────────────────────────────────
status_dist = pd.read_sql("""
SELECT status, COUNT(*) AS count FROM fact_orders GROUP BY status ORDER BY count DESC
""", conn)

# ── KPI 7: Delivery Carrier Performance ─────────────────────────
delivery_perf = pd.read_sql("""
SELECT carrier, ROUND(AVG(lead_time_days),1) AS avg_days, COUNT(*) AS shipments
FROM fact_deliveries GROUP BY carrier ORDER BY avg_days
""", conn)

# ── KPI 8: Payment Performance ──────────────────────────────────
payment = pd.read_sql("""
SELECT payment_status, COUNT(*) AS count, ROUND(SUM(total_with_gst)) AS total
FROM fact_invoices GROUP BY payment_status
""", conn)

# ── KPI 9: Top 5 Products ────────────────────────────────────────
top_products = pd.read_sql("""
SELECT oi.product_name, ROUND(SUM(oi.line_total)) AS revenue, SUM(oi.quantity) AS units
FROM fact_order_items oi JOIN fact_orders o ON oi.so_number=o.so_number
WHERE o.status!='Cancelled'
GROUP BY oi.product_id, oi.product_name ORDER BY revenue DESC LIMIT 8
""", conn)

# ── KPI 10: Quarterly ───────────────────────────────────────────
quarterly = pd.read_sql("""
SELECT order_quarter, ROUND(SUM(order_total)) AS revenue, COUNT(*) AS orders
FROM fact_orders WHERE status!='Cancelled'
GROUP BY order_quarter ORDER BY order_quarter
""", conn)

conn.close()

# Package everything for dashboard
dashboard_data = {
    "summary": {
        "total_orders": int(kpi_summary['total_orders']),
        "gross_revenue": float(kpi_summary['gross_revenue']),
        "avg_order_value": float(kpi_summary['avg_order_value']),
        "cancelled_orders": int(kpi_summary['cancelled_orders']),
        "completed_orders": int(kpi_summary['completed_orders']),
        "fulfillment_rate": round(float(kpi_summary['completed_orders'])/float(kpi_summary['total_orders'])*100, 1)
    },
    "monthly": {
        "labels": monthly['order_month'].tolist(),
        "revenue": monthly['monthly_revenue'].tolist(),
        "orders": monthly['order_count'].tolist()
    },
    "region": {
        "labels": region['region'].tolist(),
        "revenue": region['total_revenue'].tolist(),
        "orders": region['total_orders'].tolist()
    },
    "top_customers": {
        "labels": top_customers['customer_name'].tolist(),
        "revenue": top_customers['total_revenue'].tolist(),
        "orders": top_customers['total_orders'].tolist()
    },
    "categories": {
        "labels": category_rev['category'].tolist(),
        "revenue": category_rev['category_revenue'].tolist(),
        "units": category_rev['units_sold'].tolist()
    },
    "status": {
        "labels": status_dist['status'].tolist(),
        "counts": status_dist['count'].tolist()
    },
    "delivery": {
        "labels": delivery_perf['carrier'].tolist(),
        "avg_days": delivery_perf['avg_days'].tolist(),
        "shipments": delivery_perf['shipments'].tolist()
    },
    "payment": {
        "labels": payment['payment_status'].tolist(),
        "counts": payment['count'].tolist(),
        "totals": payment['total'].tolist()
    },
    "top_products": {
        "labels": [p[:30]+'...' if len(p)>30 else p for p in top_products['product_name'].tolist()],
        "revenue": top_products['revenue'].tolist(),
        "units": top_products['units'].tolist()
    },
    "quarterly": {
        "labels": quarterly['order_quarter'].tolist(),
        "revenue": quarterly['revenue'].tolist(),
        "orders": quarterly['orders'].tolist()
    }
}

out_path = os.path.join(BASE_DIR, 'dashboard', 'analytics_data.json')
with open(out_path, 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print("✅ Analytics extraction complete!")
print(f"   Total Orders   : {dashboard_data['summary']['total_orders']}")
print(f"   Gross Revenue  : ₹{dashboard_data['summary']['gross_revenue']:,.0f}")
print(f"   Avg Order Val  : ₹{dashboard_data['summary']['avg_order_value']:,.0f}")
print(f"   Fulfillment    : {dashboard_data['summary']['fulfillment_rate']}%")
print(f"\n   Data saved to  : {out_path}")
