# SAP Order-to-Cash (O2C) Sales Analytics Dashboard
### NovaTech Solutions Pvt. Ltd. | SAP Data Analytics Engineer — Capstone Project

---

## 🏢 Company Overview
**NovaTech Solutions Pvt. Ltd.** is a fictitious IT products and electronics distribution company based in India, operating across four regions (North, South, East, West) with 20 B2B enterprise customers and a catalog of 20 products.

## 📌 Project Overview
This capstone project implements a complete **SAP Order-to-Cash (O2C)** process analytics solution, simulating the data flow from SAP S/4HANA through an ETL pipeline into an analytics layer — aligned with the **SAP Data Analytics Engineer / SAP Business Data Cloud** curriculum.

---

## 🔄 SAP O2C Process Covered

| Step | SAP T-Code | Description |
|------|-----------|-------------|
| Inquiry / Quotation | VA11 / VA21 | Pre-sales customer inquiry |
| Sales Order | VA01 | Standard sales order (Type: OR) |
| Delivery | VL01N | Outbound delivery creation |
| Goods Issue | VL02N | Stock reduction / dispatch |
| Billing / Invoice | VF01 | Commercial invoice (Type: F2) |
| Payment Receipt | F-28 | Accounts receivable clearing |

---

## 🗂️ Project Structure

```
SAP_O2C_Analytics_Project/
├── data/                          # Raw SAP-like source data (CSV)
│   ├── customers.csv              # Customer Master (SAP: KNA1)
│   ├── products.csv               # Material Master (SAP: MARA)
│   ├── sales_orders.csv           # Sales Orders (SAP: VBAK/VBAP)
│   ├── order_items.csv            # Line items per order
│   ├── deliveries.csv             # Delivery documents (SAP: LIKP)
│   └── invoices.csv               # Billing documents (SAP: VBRK)
│
├── scripts/
│   ├── 01_generate_data.py        # Synthetic SAP data generation
│   ├── 02_etl_pipeline.py         # ETL: CSV → SQLite (like SAP BW)
│   └── 03_analytics_export.py     # Analytics KPI extraction
│
├── database/
│   └── o2c_analytics.db           # SQLite analytical database
│
├── sql/
│   └── analysis_queries.sql       # All 10 KPI SQL queries
│
├── dashboard/
│   ├── index.html                 # Interactive analytics dashboard
│   └── analytics_data.json       # Pre-computed KPI data
│
└── documentation/
    └── project_documentation.pdf  # Capstone project report
```

---

## 📊 Analytics KPIs Implemented

1. **Total Orders & Revenue** — FY 2024–25 summary
2. **Monthly Revenue Trend** — 15-month time series
3. **Revenue by Region** — 4 geographic regions
4. **Top 10 Customers** — Ranked by net revenue
5. **Product Category Performance** — 9 categories
6. **Order Status Distribution** — O2C pipeline health
7. **Delivery Performance** — Lead time by carrier
8. **Payment / DSO Analysis** — Overdue vs paid on time
9. **Quarterly Revenue Comparison** — Q-o-Q analysis
10. **Top Products by Revenue** — Best-selling materials

---

## 🚀 How to Run

### Step 1: Install dependencies
```bash
pip install pandas faker matplotlib seaborn reportlab
```

### Step 2: Generate Data
```bash
python scripts/01_generate_data.py
```

### Step 3: Run ETL Pipeline
```bash
python scripts/02_etl_pipeline.py
```

### Step 4: Export Analytics
```bash
python scripts/03_analytics_export.py
```

### Step 5: Open Dashboard
Open `dashboard/index.html` in any web browser — no server needed!

---

## 🛠️ Tech Stack

| Layer | Technology | SAP Equivalent |
|-------|-----------|----------------|
| Source Data | Python (Faker, Pandas) | SAP S/4HANA Tables |
| ETL | Python ETL Script | SAP Data Services / BTP |
| Storage | SQLite (Analytical DB) | SAP Datasphere / BW |
| Analytics | SQL (10 KPI Queries) | SAP Analytics Cloud |
| Visualization | HTML + Chart.js | SAP Analytics Cloud Stories |
| Documentation | Python ReportLab | — |

---

## 📈 Key Results

- **520 Sales Orders** processed across FY 2024–25
- **₹54.2 Crore** gross revenue generated
- **88.3% Order Fulfillment Rate**
- **South Region** leads with ₹16.6 Cr (30.7% share)
- **Apple MacBook Air M2** is the top product (₹8.1 Cr)
- **68.6%** invoices paid on time; 31.4% overdue (DSO risk)

---

## 👤 Author
**Krishnamachari Rout :- Capstone Project — SAP Data Analytics Engineer / SAP Business Data Cloud**  
KIIT · Batch: 2023–27
