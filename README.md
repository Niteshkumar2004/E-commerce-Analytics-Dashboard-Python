# E-commerce Analytics Dashboard

An interactive data analytics portfolio project for exploring retail order data, sales performance, payment preferences, product categories, shipping times, and customer satisfaction.

## Features

- KPI cards: revenue, orders, average order value, average customer rating, and late-delivery rate
- Date, category, payment method, and city filters
- Monthly revenue trend
- Category-wise revenue
- Payment method distribution
- Shipping duration versus customer ratings
- Top 10 products by revenue
- Delivery status and rating distribution
- Filtered order table and CSV download

## Tech stack

- Python
- Pandas
- Streamlit
- Plotly
- CSV dataset

## Project structure

```text
ecommerce-analytics-project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── ecommerce_orders.csv
```

## Run locally

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment (recommended).

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, you can skip activation and run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Dataset fields

| Field | Meaning |
|---|---|
| `order_id` | Unique order identifier |
| `order_date` | Date the order was placed |
| `customer_id` | Sample customer identifier |
| `city` | Customer city |
| `product_category` | Retail product category |
| `product_name` | Product purchased |
| `quantity` | Units purchased |
| `unit_price` | Price per unit in INR |
| `discount_pct` | Discount percentage |
| `revenue` | Revenue after discount |
| `payment_method` | Payment type used |
| `shipping_days` | Number of days for shipping |
| `customer_rating` | Sample customer rating from 1 to 5 |
| `delivery_status` | On Time or Late, based on the sample shipping rule |

## Business questions

1. Which months generate the highest revenue?
2. Which categories and products generate the most revenue?
3. Which payment methods are most frequently used?
4. Is longer shipping associated with lower customer ratings?
5. What percentage of orders are marked late?
6. How do sales differ by city?

## Important data note

The included 1,200-row dataset is **synthetic sample data** generated for this portfolio project. It is not real customer or retailer data. Treat dashboard results as demonstrations, not factual claims about a real business. Replace it with a properly licensed or authorized dataset for a real analysis.

## Suggested GitHub description

`Interactive E-commerce Analytics dashboard built with Python, Pandas, Streamlit and Plotly. Analyzes retail revenue, product categories, payment methods, shipping performance and customer ratings.`

## Future improvements

- Connect to a SQL database
- Add sales forecasting
- Add customer segmentation (RFM analysis)
- Add automated data validation
- Deploy the dashboard with Streamlit Community Cloud
