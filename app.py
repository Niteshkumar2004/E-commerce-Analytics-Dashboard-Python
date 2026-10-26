import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="E-commerce Analytics", page_icon="🛍️", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "ecommerce_orders.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    data["month"] = data["order_date"].dt.to_period("M").astype(str)
    return data

df = load_data()

st.title("🛍️ E-commerce Analytics Dashboard")
st.caption("Explore sales, product categories, payment behavior, shipping performance, and customer satisfaction.")

with st.sidebar:
    st.header("Dashboard Filters")
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    categories = sorted(df["product_category"].unique())
    selected_categories = st.multiselect("Product categories", categories, default=categories)
    methods = sorted(df["payment_method"].unique())
    selected_methods = st.multiselect("Payment methods", methods, default=methods)
    cities = sorted(df["city"].unique())
    selected_cities = st.multiselect("Cities", cities, default=cities)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[(filtered["order_date"].dt.date >= date_range[0]) & (filtered["order_date"].dt.date <= date_range[1])]
filtered = filtered[
    filtered["product_category"].isin(selected_categories)
    & filtered["payment_method"].isin(selected_methods)
    & filtered["city"].isin(selected_cities)
]

if filtered.empty:
    st.warning("No orders match these filters. Please change your selections.")
    st.stop()

revenue = filtered["revenue"].sum()
orders = filtered["order_id"].nunique()
aov = revenue / orders if orders else 0
rating = filtered["customer_rating"].mean()
late_rate = (filtered["delivery_status"].eq("Late").mean()) * 100

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Average Order Value", f"₹{aov:,.0f}")
c4.metric("Average Rating", f"{rating:.2f} / 5")
c5.metric("Late Delivery Rate", f"{late_rate:.1f}%")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Monthly Revenue Trend")
    monthly = filtered.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    fig = px.line(monthly, x="month", y="revenue", markers=True, title="Revenue by month",
                  labels={"month": "Month", "revenue": "Revenue (₹)"})
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by Product Category")
    cat_sales = filtered.groupby("product_category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(cat_sales, x="product_category", y="revenue", color="product_category",
                 labels={"product_category": "Category", "revenue": "Revenue (₹)"})
    fig.update_layout(showlegend=False, xaxis_tickangle=-25)
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Payment Method Distribution")
    payments = filtered.groupby("payment_method", as_index=False).agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
    fig = px.pie(payments, names="payment_method", values="orders", hole=0.42, title="Orders by payment method")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Shipping Time vs Customer Rating")
    shipping = filtered.groupby("shipping_days", as_index=False).agg(
        average_rating=("customer_rating", "mean"), orders=("order_id", "count")
    )
    fig = px.scatter(shipping, x="shipping_days", y="average_rating", size="orders",
                     labels={"shipping_days": "Shipping days", "average_rating": "Average rating"},
                     title="Average rating by shipping duration")
    fig.update_yaxes(range=[1, 5])
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Top 10 Products by Revenue")
    top_products = filtered.groupby("product_name", as_index=False).agg(
        revenue=("revenue", "sum"), units_sold=("quantity", "sum")
    ).sort_values("revenue", ascending=False).head(10)
    fig = px.bar(top_products.sort_values("revenue"), x="revenue", y="product_name", orientation="h",
                 hover_data=["units_sold"], labels={"revenue": "Revenue (₹)", "product_name": "Product"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Delivery Status")
    delivery = filtered["delivery_status"].value_counts().rename_axis("delivery_status").reset_index(name="orders")
    fig = px.bar(delivery, x="delivery_status", y="orders", color="delivery_status",
                 labels={"delivery_status": "Delivery status", "orders": "Orders"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Rating Distribution")
ratings = filtered["customer_rating"].value_counts().sort_index().rename_axis("rating").reset_index(name="responses")
fig = px.bar(ratings, x="rating", y="responses", labels={"rating": "Customer rating (1–5)", "responses": "Responses"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered Order Data")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", data=csv, file_name="filtered_ecommerce_orders.csv", mime="text/csv")

st.info("Portfolio note: the included dataset is synthetic sample data created for demonstration. Replace it with a real, authorized dataset before making real-world business claims.")
