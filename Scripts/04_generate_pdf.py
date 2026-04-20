"""
Project Documentation PDF Generator  v2
SAP O2C Analytics · NovaTech Solutions Pvt. Ltd.
A4, Helvetica, Justified, page-numbered bottom-right
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(BASE_DIR, 'documentation', 'project_documentation.pdf')
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

C_BLUE  = HexColor('#1a6ec8')
C_DARK  = HexColor('#0b1628')
C_TEAL  = HexColor('#0f7b6c')
C_LIGHT = HexColor('#e8f4fd')
C_BODY  = HexColor('#1f2937')
C_MUT   = HexColor('#6b7280')
C_BDR   = HexColor('#d1d5db')
C_ROW2  = HexColor('#f0f7ff')
W, H    = A4

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BLUE)
    canvas.rect(0, H - 20*mm, W, 8*mm, fill=1, stroke=0)
    canvas.setFillColor(white); canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(2*cm, H-14.5*mm, 'SAP O2C Analytics  |  NovaTech Solutions Pvt. Ltd.')
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(W-2*cm, H-14.5*mm, 'SAP Data Analytics Engineer — Capstone Project')
    canvas.setFillColor(C_BLUE)
    canvas.rect(0, 0, W, 11*mm, fill=1, stroke=0)
    canvas.setFillColor(white); canvas.setFont('Helvetica', 7.5)
    canvas.drawString(2*cm, 3.5*mm, 'KIIT  ·  FY 2024-25')
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawRightString(W-2*cm, 3.5*mm, f'Page {doc.page}')
    canvas.restoreState()

doc = SimpleDocTemplate(OUT_PATH, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2.8*cm, bottomMargin=2.2*cm,
    title='SAP O2C Analytics Capstone', author='SAP Data Analytics Engineer')

def mk(name, **kw):
    base = dict(fontName='Helvetica', fontSize=12, textColor=C_BODY,
                leading=19, alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(name, **base)

sH1  = mk('H1', fontName='Helvetica-Bold', fontSize=15, textColor=C_BLUE,
          spaceBefore=14, spaceAfter=5, leading=21, alignment=TA_LEFT)
sH2  = mk('H2', fontName='Helvetica-Bold', fontSize=13, textColor=C_DARK,
          spaceBefore=10, spaceAfter=4, leading=18, alignment=TA_LEFT)
sH3  = mk('H3', fontName='Helvetica-Bold', fontSize=12, textColor=C_TEAL,
          spaceBefore=8, spaceAfter=3, leading=16, alignment=TA_LEFT)
sBody= mk('Body')
sBull= mk('Bull', leftIndent=16, spaceAfter=3)
sTH  = mk('TH', fontName='Helvetica-Bold', fontSize=10, textColor=white,
          alignment=TA_CENTER, leading=14)
sTCc = mk('TCc', fontSize=10, textColor=C_BODY, alignment=TA_CENTER, leading=14)
sTCl = mk('TCl', fontSize=10, textColor=C_BODY, alignment=TA_LEFT,   leading=14)
sKPI = mk('KPI', fontName='Helvetica-Bold', fontSize=15, textColor=C_BLUE,
          alignment=TA_CENTER, leading=20)
sCov = mk('Cov', fontName='Helvetica-Bold', fontSize=22, textColor=white,
          alignment=TA_CENTER, leading=30)
sCovS= mk('CovS', fontSize=12, textColor=HexColor('#bfdbfe'),
          alignment=TA_CENTER, leading=18)

def hr(): return HRFlowable(width='100%', thickness=0.8, color=C_BDR,
                             spaceAfter=8, spaceBefore=2)
def sp(h=8): return Spacer(1, h)
def p(t, s=None): return Paragraph(t, s or sBody)

BASE_TS = [
    ('BACKGROUND',    (0,0), (-1,0),  C_BLUE),
    ('TEXTCOLOR',     (0,0), (-1,0),  white),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 10),
    ('GRID',          (0,0), (-1,-1), 0.5, C_BDR),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING',   (0,0), (-1,-1), 7),
    ('RIGHTPADDING',  (0,0), (-1,-1), 7),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, C_ROW2]),
]
LALIGN = [('ALIGN',(0,1),(-1,-1),'LEFT')]

def tbl(rows, widths, extra=None):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle(BASE_TS + (extra or [])))
    return t

def th(*x): return [p(c, sTH) for c in x]
def tc(*x): return [p(c, sTCc) for c in x]
def tl(*x): return [p(x[0], sTCc)] + [p(c, sTCl) for c in x[1:]]

# ════════════════════════════════════════
story = []

# PAGE 1 — COVER
cover_rows = [
    [p('SAP ORDER-TO-CASH (O2C)', sCov)],
    [p('SALES ANALYTICS DASHBOARD', sCov)],
    [p('&nbsp;', sCovS)],
    [p('Capstone Project Report', sCovS)],
    [p('SAP Data Analytics Engineer / SAP Business Data Cloud', sCovS)],
]
ct = Table(cover_rows, colWidths=[16.2*cm])
ct.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), C_BLUE),
    ('TOPPADDING',    (0,0),(-1,-1), 14),
    ('BOTTOMPADDING', (0,0),(-1,-1), 14),
    ('LEFTPADDING',   (0,0),(-1,-1), 18),
    ('RIGHTPADDING',  (0,0),(-1,-1), 18),
]))
story.append(ct); story.append(sp(18))

meta = [
    [p('<b>Company</b>',   sH3), p('NovaTech Solutions Pvt. Ltd.')],
    [p('<b>Industry</b>',  sH3), p('IT Products and Electronics Distribution — B2B')],
    [p('<b>Programme</b>', sH3), p('SAP Data Analytics Engineer / SAP Business Data Cloud')],
    [p('<b>Topic</b>',     sH3), p('Order-to-Cash (O2C) — Complete Sales Cycle Analytics')],
    [p('<b>Period</b>',    sH3), p('Financial Year 2024-25  (January 2024 to March 2025)')],
    [p('<b>Institute</b>', sH3), p('KIIT')],
]
mt = Table(meta, colWidths=[4.5*cm, 11.7*cm])
mt.setStyle(TableStyle([
    ('ROWBACKGROUNDS',(0,0),(-1,-1),[C_LIGHT, white]),
    ('GRID',         (0,0),(-1,-1), 0.5, C_BDR),
    ('TOPPADDING',   (0,0),(-1,-1), 8),
    ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ('LEFTPADDING',  (0,0),(-1,-1), 10),
    ('RIGHTPADDING', (0,0),(-1,-1), 10),
    ('VALIGN',       (0,0),(-1,-1), 'MIDDLE'),
]))
story.append(mt); story.append(sp(18))

story.append(p('<b>Executive KPI Summary — FY 2024-25</b>', sH2))
kpis = [
    th('Metric', 'Value', 'Metric', 'Value'),
    [p('Total Sales Orders', sTCl), p('<b>520</b>', sKPI),
     p('Gross Revenue',      sTCl), p('<b>Rs.54.17 Cr</b>', sKPI)],
    [p('Fulfillment Rate',   sTCl), p('<b>88.3%</b>', sKPI),
     p('Avg Order Value',    sTCl), p('<b>Rs.10.4 L</b>', sKPI)],
    [p('Invoices Raised',    sTCl), p('<b>459</b>', sKPI),
     p('Payment Compliance', sTCl), p('<b>68.6%</b>', sKPI)],
    [p('Top Region',         sTCl), p('<b>South India</b>', sKPI),
     p('Top Category',       sTCl), p('<b>Laptops</b>', sKPI)],
]
story.append(tbl(kpis, [4.5*cm, 3.5*cm, 4.5*cm, 3.7*cm]))
story.append(PageBreak())

# PAGE 2 — Problem Statement & O2C Process
story.append(p('1.  Problem Statement', sH1)); story.append(hr())
story.append(p(
    'The Order-to-Cash (O2C) cycle is the revenue backbone of any product-selling enterprise. '
    'It spans every customer-facing activity from sales order creation through to cash collection. '
    'Despite operating on SAP S/4HANA, many organisations lack consolidated real-time visibility '
    'into this process — leading to elevated Days Sales Outstanding (DSO), poor delivery tracking, '
    'and blind spots in customer and product performance reporting.'))
story.append(p(
    'NovaTech Solutions Pvt. Ltd., a growing IT products distributor operating across four Indian '
    'regions, faces these exact challenges. Sales, logistics, and finance data are distributed '
    'across SAP SD, MM, and FI modules with no unified analytics layer. Business leaders cannot '
    'quickly answer: Which customers generate the most revenue? Which products are underperforming? '
    'What is our current DSO? How are our logistics partners performing? This project addresses '
    'all of these gaps with a complete end-to-end analytics solution.'))

story.append(sp(6))
story.append(p('2.  Project Objective', sH1)); story.append(hr())
story.append(p('This capstone project designs and implements a complete end-to-end SAP '
               'Order-to-Cash Analytics solution with the following objectives:'))
for obj in [
    'Simulate SAP S/4HANA O2C master and transactional data with realistic Indian B2B enterprise records across 20 customers and 20 products',
    'Build a structured ETL pipeline replicating SAP BW / SAP Datasphere data flow from ERP source tables into an analytical layer with Star Schema design',
    'Implement 10 business KPIs using SQL analytics queries including window functions, RANK, cumulative sums, and regional share calculations',
    'Deliver an interactive browser-based Analytics Dashboard with 15+ Chart.js visualisations across 6 analytical tabs — equivalent to SAP Analytics Cloud stories',
    'Document the complete O2C process with SAP T-codes, table mappings, enterprise configuration, and a future improvement roadmap',
]:
    story.append(p(f'  * {obj}', sBull))

story.append(sp(8))
story.append(p('3.  SAP Order-to-Cash Business Process', sH1)); story.append(hr())
story.append(p(
    'The O2C cycle in SAP S/4HANA represents the complete lifecycle of a customer transaction. '
    'Each step generates documents that update specific SAP database tables, creating a fully '
    'traceable audit trail from pre-sales inquiry through payment clearance.'))
story.append(sp(4))

proc = [
    th('Step', 'Process Stage', 'SAP T-Code', 'Key SAP Tables', 'FY25 Volume'),
    tc('1', 'Customer Inquiry / Quotation', 'VA11 / VA21', 'VBAK, VBAP', 'Pre-Sales'),
    tc('2', 'Sales Order Creation',          'VA01',        'VBAK, VBAP, VBKD', '520 Orders'),
    tc('3', 'Outbound Delivery Creation',    'VL01N',       'LIKP, LIPS',  '496 Deliveries'),
    tc('4', 'Post Goods Issue',              'VL02N',       'MKPF, MSEG',  '459 GI Posted'),
    tc('5', 'Billing / Invoice Creation',    'VF01',        'VBRK, VBRP',  '459 Invoices'),
    tc('6', 'Payment Receipt / Clearing',    'F-28',        'BKPF, BSEG',  '315 Cleared'),
]
story.append(tbl(proc, [1.2*cm, 4.2*cm, 2.6*cm, 4.1*cm, 4.1*cm]))
story.append(PageBreak())

# PAGE 3 — Solution, Architecture, Data Model
story.append(p('4.  Solution and Features', sH1)); story.append(hr())
story.append(p('4.1  Three-Layer Analytics Architecture', sH2))
story.append(p(
    'The solution mirrors the standard SAP data analytics stack: a Source Layer feeds an '
    'Integration / ETL Layer, which populates an Analytical Storage Layer consumed by the '
    'Reporting and Presentation Layer.'))
story.append(sp(4))
arch = [
    th('Layer', 'Component Built', 'SAP Equivalent', 'Technology Used'),
    tl('Source Layer',       'Synthetic SAP master and transactional data (CSV)',    'SAP S/4HANA ERP',           'Python + Faker + Pandas'),
    tl('ETL Layer',          'Extract, Transform, Load pipeline script',             'SAP Data Services / BTP',   'Python ETL (02_etl_pipeline.py)'),
    tl('Analytical Storage', 'Star Schema: 2 Dimension + 4 Fact tables + 7 Views',  'SAP Datasphere / BW4HANA',  'SQLite Analytical Database'),
    tl('Analytics Layer',    '10 SQL KPI queries with window functions',             'SAP Analytics Cloud Queries','SQL (analysis_queries.sql)'),
    tl('Presentation Layer', 'Interactive dashboard with 6 tabs and 15+ charts',    'SAP Analytics Cloud Stories','HTML5 + Chart.js'),
]
story.append(tbl(arch, [3*cm, 5.2*cm, 4*cm, 4*cm], extra=LALIGN))
story.append(sp(10))

story.append(p('4.2  Data Model — Star Schema Design', sH2))
story.append(p(
    'The analytical database uses a Star Schema aligned with SAP BW4HANA and Datasphere modelling '
    'conventions. Two dimension tables surround four fact tables covering the full O2C document flow, '
    'joined by business keys (customer_id, product_id, so_number).'))
story.append(sp(4))
dm = [
    th('Table Name', 'Type', 'SAP Source Table', 'Rows', 'Key Fields'),
    tl('dim_customers',    'Dimension', 'KNA1',        '20',   'customer_id, region, credit_limit'),
    tl('dim_products',     'Dimension', 'MARA / MAKT', '20',   'product_id, category, unit_price, hsn_code'),
    tl('fact_orders',      'Fact',      'VBAK / VBAP', '520',  'so_number, customer_id, order_total, status'),
    tl('fact_order_items', 'Fact',      'VBAP',        '1600', 'so_number, product_id, quantity, line_total'),
    tl('fact_deliveries',  'Fact',      'LIKP / LIPS', '496',  'delivery_number, carrier, lead_time_days'),
    tl('fact_invoices',    'Fact',      'VBRK / VBRP', '459',  'invoice_number, total_with_gst, payment_status'),
]
story.append(tbl(dm, [3.8*cm, 2*cm, 2.8*cm, 1.5*cm, 6.1*cm], extra=LALIGN))
story.append(sp(10))

story.append(p('4.3  Analytics KPIs Implemented', sH2))
story.append(sp(4))
kpi_list = [
    th('#', 'KPI Name', 'SQL Method', 'Business Value'),
    tl('1',  'Total Orders and Revenue',   'COUNT, SUM aggregation',           'Overall business health'),
    tl('2',  'Monthly Revenue Trend',      '15-month GROUP BY time series',     'Seasonal pattern identification'),
    tl('3',  'Revenue by Region',          'GROUP BY + window function share',  'Regional sales strategy'),
    tl('4',  'Top 10 Customers',           'RANK() window function',            'Key account management'),
    tl('5',  'Product Category Revenue',   'JOIN + GROUP BY category',          'Inventory and pricing decisions'),
    tl('6',  'Order Status Distribution',  'CASE WHEN classification',          'O2C pipeline health check'),
    tl('7',  'Delivery Lead Time',         'AVG, MIN, MAX per carrier',         'Logistics partner evaluation'),
    tl('8',  'Payment / DSO Analysis',     'Overdue vs Paid On Time split',     'Cash flow risk management'),
    tl('9',  'Quarterly Comparison',       'GROUP BY quarter with Q-o-Q',       'Executive performance review'),
    tl('10', 'Top Products by Revenue',    'JOIN items and orders + RANK',      'Product portfolio optimisation'),
]
story.append(tbl(kpi_list, [0.8*cm, 4*cm, 4.3*cm, 7.1*cm], extra=LALIGN))
story.append(PageBreak())

# PAGE 4 — Results & SAP Config
story.append(p('5.  Results and Key Findings', sH1)); story.append(hr())
story.append(p(
    'The analytics solution processed 520 sales orders for FY 2024-25 and surfaced the following '
    'actionable insights across revenue, customer, product, logistics, and finance dimensions:'))
story.append(sp(4))
res = [
    th('Dimension', 'KPI Measured', 'Result', 'Business Insight'),
    tl('Revenue',     'Gross Revenue FY25',       'Rs.54.17 Crore',         'Strong annual performance across all regions'),
    tl('Revenue',     'Best Month',               'May 2024 — Rs.4.15 Cr', 'Seasonal demand spike identified in Q2'),
    tl('Revenue',     'Weakest Month',            'Jun 2024 — Rs.2.38 Cr', 'Possible mid-year procurement slowdown'),
    tl('Fulfillment', 'Order Fulfillment Rate',   '88.3%',                  '459 of 520 orders successfully completed'),
    tl('Fulfillment', 'Cancellation Rate',        '4.6% (24 orders)',       'Within acceptable industry range'),
    tl('Geography',   'Top Revenue Region',       'South — Rs.16.6 Cr',   '30.7% of total revenue'),
    tl('Geography',   'Highest Avg Order Value',  'East — Rs.11.4 L avg',  'Fewer but higher-value enterprise deals'),
    tl('Customers',   'Top Customer',             'Delta Software Pvt. Ltd.','Rs.4.03 Cr — 36 orders placed'),
    tl('Products',    'Top Product',              'Apple MacBook Air M2',   'Rs.8.13 Cr — 757 units sold'),
    tl('Products',    'Top Category',             'Laptops',                'Rs.25.36 Cr — 46.8% of total revenue'),
    tl('Logistics',   'Best Carrier (Lead Time)', 'Delhivery — 6.4 days',  'Fastest average delivery lead time'),
    tl('Finance',     'Payment Compliance',       '68.6% paid on time',     '315 of 459 invoices cleared in time'),
    tl('Finance',     'DSO Risk',                 '144 Overdue Invoices',   'Rs.16.9 Cr outstanding — immediate action needed'),
]
story.append(tbl(res, [2.5*cm, 3.8*cm, 3.9*cm, 6*cm], extra=LALIGN))

story.append(sp(10))
story.append(p('6.  SAP Enterprise Configuration', sH1)); story.append(hr())
story.append(p(
    'NovaTech Solutions has been set up as a fully configured SAP enterprise. The organisational '
    'structure covers all SD, FI, and MM configuration objects required for an end-to-end O2C '
    'process, reflecting a real Indian IT products company SAP implementation.'))
story.append(sp(4))
cfg = [
    th('SAP Object', 'Code / Value', 'Description'),
    tl('Company Code',         '1000',              'NovaTech Solutions Pvt. Ltd. — India Entity'),
    tl('Fiscal Year Variant',  'V3',                'April to March (Indian Financial Year)'),
    tl('Chart of Accounts',    'CAIN',              'India Standard Chart of Accounts'),
    tl('Sales Organization',   '1000',              'India National Sales Organisation'),
    tl('Distribution Channel', '10',                'Direct Sales to Enterprise B2B Customers'),
    tl('Division',             '00',                'Cross-Division — All Product Lines'),
    tl('Plant',                'PL01',              'Bengaluru Central Warehouse and Distribution Hub'),
    tl('Storage Location',     'SL01',              'Main IT Products Storage Bay'),
    tl('Shipping Points',      'SP01, SP02, SP03',  'Bengaluru, Mumbai, and Delhi Dispatch Centres'),
    tl('Sales Document Type',  'OR',                'Standard Sales Order — Commercial B2B'),
    tl('Delivery Type',        'LF',                'Standard Outbound Delivery Document'),
    tl('Billing Type',         'F2',                'Commercial Invoice with 18% GST (CGST + SGST)'),
    tl('Pricing Procedure',    'RVAA01',            'Standard pricing with discount and GST conditions'),
    tl('Payment Terms',        'ZN15 / ZN30 / ZN45','Net 15, 30, or 45 days customer credit periods'),
]
story.append(tbl(cfg, [4.2*cm, 3.3*cm, 8.7*cm], extra=LALIGN))
story.append(PageBreak())

# PAGE 5 — Unique Points, Future, Conclusion
story.append(p('7.  Unique Points of This Project', sH1)); story.append(hr())
unique = [
    ('End-to-End Functional Pipeline',
     'Three Python scripts (data generation, ETL, analytics export) replicate the full SAP data '
     'engineering workflow: extract from ERP, load to BW, query in SAC. Most capstone projects '
     'stop at documentation — this one runs and produces real analytical output.'),
    ('Authentic SAP Naming Conventions',
     'Every table, field, and SAP object uses real SAP naming — VBAK, VBAP, LIKP, VBRK, KNA1, '
     'MARA, Company Code 1000, Sales Org 1000, Billing Type F2 — making this directly relatable '
     'to real SAP SD/FI consulting and implementation experience.'),
    ('Star Schema Data Warehouse Design',
     'Two dimension tables and four fact tables plus seven pre-built SQL analytical views are '
     'structured exactly like SAP BW InfoProviders or Datasphere Analytic Models, with proper '
     'foreign key relationships and a well-defined fact grain.'),
    ('Advanced SQL Analytics — 10 KPI Queries',
     'KPI queries use SQL window functions (RANK OVER, SUM OVER for cumulative revenue), '
     'multi-table JOINs, CASE WHEN classification, and percentage share calculations — the same '
     'SQL patterns used in SAP Datasphere SQL Views connected to SAP Analytics Cloud.'),
    ('Interactive Multi-Tab Dashboard — Zero Dependencies',
     'Six analytical tabs with 15+ Chart.js charts including dual-axis time series, doughnut, '
     'polar area, horizontal bar, and a dynamic ranked customer table. Opens directly in any '
     'browser with no server, no installation, and no internet connection required.'),
    ('GST-Compliant Indian Finance Model',
     'Invoices include 18% GST on all line items (displayed as total_with_gst), reflecting the '
     'Indian indirect tax framework that SAP SD/FI handles through pricing condition types JIVP '
     'and JIVC in the standard pricing procedure.'),
]
for title, desc in unique:
    story.append(KeepTogether([
        p(f'<b>  *  {title}</b>', sH3),
        p(desc, sBody),
        sp(5),
    ]))

story.append(sp(6))
story.append(p('8.  Dashboard Structure Overview', sH1)); story.append(hr())
story.append(p(
    'The interactive dashboard (dashboard/index.html) is structured into six analytical tabs. '
    'Open the file in any modern web browser — Google Chrome, Firefox, or Edge. '
    'No server or internet connection is required.'))
story.append(sp(4))
tabs = [
    th('Tab', 'Name', 'Charts / Components Included', 'Primary Business Question'),
    tl('1', 'Overview',    'Monthly trend bar, Status donut, Region bar, Quarterly bar',   'Full O2C health at a glance'),
    tl('2', 'Revenue',     'Dual-axis monthly, Region doughnut, Quarterly combo chart',    'Revenue trends and regional mix'),
    tl('3', 'Customers',   'Top-10 ranked table with bars, Horizontal bar chart',          'Which customers drive revenue?'),
    tl('4', 'Products',    'Category bar, Units polar area, Top-8 products bar chart',     'Product portfolio performance'),
    tl('5', 'Operations',  'Payment donut, Carrier lead-time bar, Shipments pie',          'DSO risk and logistics quality'),
    tl('6', 'O2C Process', 'Stage flow diagram, Stage stats table, SAP config table',      'SAP process traceability'),
]
story.append(tbl(tabs, [0.8*cm, 2.5*cm, 6*cm, 6.9*cm], extra=LALIGN))

story.append(sp(10))
story.append(p('9.  Future Improvements', sH1)); story.append(hr())
future = [
    th('Enhancement', 'Description', 'SAP Platform'),
    tl('Live SAP OData Connection',  'Replace CSV with real-time SAP S/4HANA OData APIs',     'SAP BTP / OData v4'),
    tl('SAP Datasphere Migration',   'Host star schema in Datasphere with managed data spaces','SAP Datasphere'),
    tl('SAC Story Migration',        'Rebuild as native SAP Analytics Cloud Story/Application','SAP Analytics Cloud'),
    tl('ML Demand Forecasting',      'Python time-series model for sales order forecasting',   'SAP AI Core / HANA ML'),
    tl('Custom ABAP ALV Report',     'O2C pipeline status report via SALV framework / SE38',  'SAP ABAP'),
    tl('Power BI Integration',       'Connect SQLite via ODBC for enterprise BI reporting',   'Power BI Desktop'),
    tl('Automated ETL Scheduling',   'Schedule pipeline with Apache Airflow or SAP DS',       'SAP Data Services'),
    tl('RFM Customer Segmentation',  'Recency, Frequency, Monetary model for customer tiers', 'Python / SAP C4HANA'),
]
story.append(tbl(future, [4*cm, 6.8*cm, 5.4*cm], extra=LALIGN))

story.append(sp(10))
story.append(p('10.  Conclusion', sH1)); story.append(hr())
story.append(p(
    'This capstone project successfully delivers a complete, functional SAP Order-to-Cash '
    'Analytics solution for NovaTech Solutions Pvt. Ltd. All six O2C process stages are covered '
    'with authentic SAP enterprise configuration, a Star Schema data warehouse, ten SQL-driven '
    'KPIs, and an interactive multi-tab analytics dashboard. The solution bridges SAP functional '
    'module knowledge (SD, FI, MM) with modern data engineering skills — Python ETL, relational '
    'SQL analytics, and interactive Chart.js visualisation — precisely the competency profile '
    'expected of an SAP Data Analytics Engineer.'))
story.append(p(
    'The architecture is production-ready and directly extensible to a live SAP environment '
    'using SAP Datasphere for the analytical storage layer and SAP Analytics Cloud for '
    'the reporting layer, making this project not just a submission artifact but a genuine '
    'blueprint for enterprise O2C analytics implementation.'))

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
size_kb = os.path.getsize(OUT_PATH) / 1024
print(f'PDF built -> {OUT_PATH}  ({size_kb:.1f} KB)')
