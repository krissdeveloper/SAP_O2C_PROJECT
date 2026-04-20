"""
SAP Order-to-Cash (O2C) Data Generator
Company: NovaTech Solutions Pvt. Ltd.
Author: Capstone Project - SAP Data Analytics Engineer
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# 1. CUSTOMERS (SAP Master Data: Customer Master)
# ─────────────────────────────────────────────
customers = [
    {"customer_id": "C001", "customer_name": "Infosys Limited",           "region": "South", "city": "Bengaluru", "credit_limit": 2000000, "payment_terms": "Net 30"},
    {"customer_id": "C002", "customer_name": "Wipro Technologies",         "region": "South", "city": "Bengaluru", "credit_limit": 1800000, "payment_terms": "Net 30"},
    {"customer_id": "C003", "customer_name": "TCS Enterprises",            "region": "West",  "city": "Mumbai",    "credit_limit": 2500000, "payment_terms": "Net 45"},
    {"customer_id": "C004", "customer_name": "HCL Systems Pvt Ltd",        "region": "North", "city": "Noida",     "credit_limit": 1500000, "payment_terms": "Net 30"},
    {"customer_id": "C005", "customer_name": "Tech Mahindra",              "region": "West",  "city": "Pune",      "credit_limit": 1600000, "payment_terms": "Net 30"},
    {"customer_id": "C006", "customer_name": "Mphasis Solutions",          "region": "South", "city": "Chennai",   "credit_limit": 900000,  "payment_terms": "Net 15"},
    {"customer_id": "C007", "customer_name": "L&T Infotech",               "region": "West",  "city": "Mumbai",    "credit_limit": 1200000, "payment_terms": "Net 45"},
    {"customer_id": "C008", "customer_name": "Mindtree Technologies",      "region": "South", "city": "Bengaluru", "credit_limit": 800000,  "payment_terms": "Net 30"},
    {"customer_id": "C009", "customer_name": "Hexaware Technologies",      "region": "West",  "city": "Navi Mumbai","credit_limit": 700000, "payment_terms": "Net 30"},
    {"customer_id": "C010", "customer_name": "Zensar Technologies",        "region": "West",  "city": "Pune",      "credit_limit": 600000,  "payment_terms": "Net 15"},
    {"customer_id": "C011", "customer_name": "NIIT Technologies",          "region": "North", "city": "Gurugram",  "credit_limit": 500000,  "payment_terms": "Net 30"},
    {"customer_id": "C012", "customer_name": "Persistent Systems",         "region": "West",  "city": "Pune",      "credit_limit": 750000,  "payment_terms": "Net 30"},
    {"customer_id": "C013", "customer_name": "Cyient Limited",             "region": "South", "city": "Hyderabad", "credit_limit": 650000,  "payment_terms": "Net 30"},
    {"customer_id": "C014", "customer_name": "Mastech Digital",            "region": "East",  "city": "Kolkata",   "credit_limit": 400000,  "payment_terms": "Net 15"},
    {"customer_id": "C015", "customer_name": "KPIT Technologies",          "region": "West",  "city": "Pune",      "credit_limit": 850000,  "payment_terms": "Net 30"},
    {"customer_id": "C016", "customer_name": "Ratan IT Solutions",         "region": "North", "city": "Delhi",     "credit_limit": 1100000, "payment_terms": "Net 45"},
    {"customer_id": "C017", "customer_name": "Sigma Infotech",             "region": "East",  "city": "Bhubaneswar","credit_limit": 350000, "payment_terms": "Net 15"},
    {"customer_id": "C018", "customer_name": "BlueStar Systems",           "region": "South", "city": "Coimbatore","credit_limit": 480000,  "payment_terms": "Net 30"},
    {"customer_id": "C019", "customer_name": "Apex Digital Corp",          "region": "North", "city": "Chandigarh","credit_limit": 560000,  "payment_terms": "Net 30"},
    {"customer_id": "C020", "customer_name": "Delta Software Pvt Ltd",     "region": "East",  "city": "Guwahati",  "credit_limit": 300000,  "payment_terms": "Net 15"},
]

# ─────────────────────────────────────────────
# 2. PRODUCTS (SAP Material Master)
# ─────────────────────────────────────────────
products = [
    {"product_id": "MAT001", "product_name": "Dell Latitude 5540 Laptop",       "category": "Laptops",        "unit_price": 72000,  "unit": "EA", "hsn_code": "84713010"},
    {"product_id": "MAT002", "product_name": "HP EliteBook 840 G10",            "category": "Laptops",        "unit_price": 85000,  "unit": "EA", "hsn_code": "84713010"},
    {"product_id": "MAT003", "product_name": "Lenovo ThinkPad E14",             "category": "Laptops",        "unit_price": 68000,  "unit": "EA", "hsn_code": "84713010"},
    {"product_id": "MAT004", "product_name": "Apple MacBook Air M2",            "category": "Laptops",        "unit_price": 114000, "unit": "EA", "hsn_code": "84713010"},
    {"product_id": "MAT005", "product_name": "Samsung 27\" 4K Monitor",         "category": "Monitors",       "unit_price": 28000,  "unit": "EA", "hsn_code": "85285200"},
    {"product_id": "MAT006", "product_name": "LG 24\" Full HD Monitor",         "category": "Monitors",       "unit_price": 14000,  "unit": "EA", "hsn_code": "85285200"},
    {"product_id": "MAT007", "product_name": "Cisco Catalyst 2960 Switch",      "category": "Networking",     "unit_price": 45000,  "unit": "EA", "hsn_code": "85176200"},
    {"product_id": "MAT008", "product_name": "TP-Link WiFi 6 Router",           "category": "Networking",     "unit_price": 12000,  "unit": "EA", "hsn_code": "85176200"},
    {"product_id": "MAT009", "product_name": "HP LaserJet Pro M404dn",          "category": "Printers",       "unit_price": 22000,  "unit": "EA", "hsn_code": "84433200"},
    {"product_id": "MAT010", "product_name": "Canon ImageRunner 2625i",         "category": "Printers",       "unit_price": 55000,  "unit": "EA", "hsn_code": "84433200"},
    {"product_id": "MAT011", "product_name": "Seagate 4TB External HDD",        "category": "Storage",        "unit_price": 7500,   "unit": "EA", "hsn_code": "84717050"},
    {"product_id": "MAT012", "product_name": "Samsung 1TB NVMe SSD",            "category": "Storage",        "unit_price": 9500,   "unit": "EA", "hsn_code": "84717050"},
    {"product_id": "MAT013", "product_name": "APC 1500VA UPS",                  "category": "Power",          "unit_price": 18000,  "unit": "EA", "hsn_code": "85044010"},
    {"product_id": "MAT014", "product_name": "Logitech MX Master 3 Mouse",      "category": "Peripherals",    "unit_price": 4200,   "unit": "EA", "hsn_code": "84716060"},
    {"product_id": "MAT015", "product_name": "Corsair Mechanical Keyboard",     "category": "Peripherals",    "unit_price": 6500,   "unit": "EA", "hsn_code": "84716060"},
    {"product_id": "MAT016", "product_name": "Lenovo ThinkCentre Desktop",      "category": "Desktops",       "unit_price": 52000,  "unit": "EA", "hsn_code": "84714900"},
    {"product_id": "MAT017", "product_name": "Dell OptiPlex 5000 Desktop",      "category": "Desktops",       "unit_price": 48000,  "unit": "EA", "hsn_code": "84714900"},
    {"product_id": "MAT018", "product_name": "Jabra Evolve2 Headset",           "category": "Peripherals",    "unit_price": 8500,   "unit": "EA", "hsn_code": "85183000"},
    {"product_id": "MAT019", "product_name": "D-Link 24-Port Patch Panel",      "category": "Networking",     "unit_price": 5500,   "unit": "EA", "hsn_code": "85176200"},
    {"product_id": "MAT020", "product_name": "Microsoft Office 365 (1 Year)",   "category": "Software",       "unit_price": 4200,   "unit": "LIC","hsn_code": "99831100"},
]

# ─────────────────────────────────────────────
# 3. SALES ORDERS + ORDER ITEMS
# ─────────────────────────────────────────────
sales_orders = []
order_items = []

start_date = datetime(2024, 1, 1)
end_date   = datetime(2025, 3, 31)

order_statuses = ['Completed', 'Completed', 'Completed', 'Delivered', 'In Transit', 'Cancelled']
status_weights = [0.60, 0.10, 0.05, 0.12, 0.08, 0.05]

so_number = 4500000  # SAP SO numbering convention

for i in range(520):
    cust = random.choice(customers)
    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    status = random.choices(order_statuses, weights=status_weights)[0]
    so_no = f"SO-{so_number + i}"
    doc_no = f"500{so_number + i}"
    num_items = random.randint(1, 5)
    selected_products = random.sample(products, num_items)

    order_total = 0
    for j, prod in enumerate(selected_products):
        qty = random.randint(1, 20)
        discount_pct = random.choice([0, 2, 5, 8, 10])
        unit_price = prod['unit_price']
        line_total = round(qty * unit_price * (1 - discount_pct / 100), 2)
        order_total += line_total
        order_items.append({
            "order_item_id": f"{so_no}-{j+1:02d}",
            "so_number": so_no,
            "item_number": f"{(j+1)*10:04d}",
            "product_id": prod['product_id'],
            "product_name": prod['product_name'],
            "category": prod['category'],
            "quantity": qty,
            "unit": prod['unit'],
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "line_total": line_total,
        })

    sales_orders.append({
        "so_number": so_no,
        "sap_doc_number": doc_no,
        "customer_id": cust['customer_id'],
        "customer_name": cust['customer_name'],
        "region": cust['region'],
        "order_date": order_date.strftime('%Y-%m-%d'),
        "order_month": order_date.strftime('%Y-%m'),
        "order_year": order_date.year,
        "status": status,
        "order_total": round(order_total, 2),
        "payment_terms": cust['payment_terms'],
        "sales_org": "1000",
        "distribution_channel": "10",
        "division": "00",
    })

# ─────────────────────────────────────────────
# 4. DELIVERIES (SAP VL01N / VL02N)
# ─────────────────────────────────────────────
deliveries = []
del_number = 800000
for so in sales_orders:
    if so['status'] in ['Completed', 'Delivered', 'In Transit']:
        order_dt = datetime.strptime(so['order_date'], '%Y-%m-%d')
        dispatch_days = random.randint(1, 5)
        delivery_days = random.randint(3, 10)
        dispatch_date = order_dt + timedelta(days=dispatch_days)
        delivery_date = dispatch_date + timedelta(days=delivery_days)
        deliveries.append({
            "delivery_number": f"DEL-{del_number}",
            "so_number": so['so_number'],
            "customer_id": so['customer_id'],
            "dispatch_date": dispatch_date.strftime('%Y-%m-%d'),
            "delivery_date": delivery_date.strftime('%Y-%m-%d'),
            "delivery_status": "Goods Issued" if so['status'] in ['Completed', 'Delivered'] else "In Transit",
            "shipping_point": random.choice(["SP01", "SP02", "SP03"]),
            "carrier": random.choice(["BlueDart", "DTDC", "Delhivery", "FedEx India"]),
        })
        del_number += 1

# ─────────────────────────────────────────────
# 5. INVOICES / BILLING (SAP VF01)
# ─────────────────────────────────────────────
invoices = []
inv_number = 9000000
for so in sales_orders:
    if so['status'] in ['Completed', 'Delivered']:
        order_dt = datetime.strptime(so['order_date'], '%Y-%m-%d')
        inv_date = order_dt + timedelta(days=random.randint(7, 14))
        payment_terms_days = int(so['payment_terms'].split()[1])
        due_date = inv_date + timedelta(days=payment_terms_days)
        days_to_pay = random.randint(-5, payment_terms_days + 15)
        paid_date = inv_date + timedelta(days=max(1, days_to_pay))
        paid = days_to_pay <= payment_terms_days
        invoices.append({
            "invoice_number": f"INV-{inv_number}",
            "so_number": so['so_number'],
            "customer_id": so['customer_id'],
            "invoice_date": inv_date.strftime('%Y-%m-%d'),
            "due_date": due_date.strftime('%Y-%m-%d'),
            "invoice_amount": so['order_total'],
            "gst_18pct": round(so['order_total'] * 0.18, 2),
            "total_with_gst": round(so['order_total'] * 1.18, 2),
            "payment_status": "Paid On Time" if paid else "Overdue",
            "paid_date": paid_date.strftime('%Y-%m-%d') if paid else None,
            "days_to_pay": days_to_pay if paid else None,
            "accounting_doc": f"ACC{inv_number}",
        })
        inv_number += 1

# ─────────────────────────────────────────────
# SAVE TO CSV
# ─────────────────────────────────────────────
pd.DataFrame(customers).to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
pd.DataFrame(products).to_csv(f"{OUTPUT_DIR}/products.csv", index=False)
pd.DataFrame(sales_orders).to_csv(f"{OUTPUT_DIR}/sales_orders.csv", index=False)
pd.DataFrame(order_items).to_csv(f"{OUTPUT_DIR}/order_items.csv", index=False)
pd.DataFrame(deliveries).to_csv(f"{OUTPUT_DIR}/deliveries.csv", index=False)
pd.DataFrame(invoices).to_csv(f"{OUTPUT_DIR}/invoices.csv", index=False)

print("✅ Data generation complete!")
print(f"   Customers   : {len(customers)}")
print(f"   Products    : {len(products)}")
print(f"   Sales Orders: {len(sales_orders)}")
print(f"   Order Items : {len(order_items)}")
print(f"   Deliveries  : {len(deliveries)}")
print(f"   Invoices    : {len(invoices)}")
