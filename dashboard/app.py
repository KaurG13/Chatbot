import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Adidas Sales Dashboard",
    page_icon="👟",
    layout="wide"
)

st.title("👟 Adidas Sales Dashboard")
st.markdown("Interactive analysis of Adidas retail sales data")

# ------------------ LOAD DATA ------------------
df = pd.read_excel("Adidas.xlsx")

# Fix column types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

product = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

sales_method = st.sidebar.multiselect(
    "Sales Method",
    options=df["SalesMethod"].unique(),
    default=df["SalesMethod"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Product"].isin(product)) &
    (df["SalesMethod"].isin(sales_method))
]

# ------------------ KPI METRICS ------------------
total_sales = filtered_df["TotalSales"].sum()
total_units = filtered_df["UnitsSold"].sum()
avg_price = filtered_df["PriceperUnit"].mean()
total_profit = filtered_df["OperatingProfit"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📦 Units Sold", f"{total_units:,}")
col3.metric("🏷️ Avg Price/Unit", f"${avg_price:.2f}")
col4.metric("📈 Operating Profit", f"${total_profit:,.0f}")

st.divider()

# ------------------ SALES BY REGION ------------------
sales_by_region = (
    filtered_df.groupby("Region")["TotalSales"]
    .sum()
    .sort_values()
)

fig1, ax1 = plt.subplots()
ax1.barh(sales_by_region.index, sales_by_region.values)
ax1.set_title("Total Sales by Region")
ax1.set_xlabel("Sales ($)")

st.pyplot(fig1)

# ------------------ TOP PRODUCTS ------------------
top_products = (
    filtered_df.groupby("Product")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
ax2.bar(top_products.index, top_products.values)
ax2.set_title("Top 10 Products by Sales")
ax2.set_ylabel("Sales ($)")
ax2.tick_params(axis='x', rotation=45)

st.pyplot(fig2)

# ------------------ PRICE vs UNITS SOLD ------------------
fig3, ax3 = plt.subplots()
ax3.scatter(
    filtered_df["PriceperUnit"],
    filtered_df["UnitsSold"]
)
ax3.set_xlabel("Price per Unit ($)")
ax3.set_ylabel("Units Sold")
ax3.set_title("Price vs Units Sold")

st.pyplot(fig3)

# ------------------ SALES TREND OVER TIME ------------------
sales_over_time = (
    filtered_df.groupby(filtered_df["InvoiceDate"].dt.to_period("M"))["TotalSales"]
    .sum()
)

fig4, ax4 = plt.subplots()
ax4.plot(sales_over_time.index.astype(str), sales_over_time.values)
ax4.set_title("Monthly Sales Trend")
ax4.set_xlabel("Month")
ax4.set_ylabel("Sales ($)")
ax4.tick_params(axis='x', rotation=45)

st.pyplot(fig4)

# ------------------ BUSINESS INSIGHTS ------------------
st.markdown("""
### 📌 Key Business Insights
- Certain regions dominate Adidas revenue contribution
- Few top products generate majority of total sales
- Higher price per unit usually leads to lower units sold
- Sales show seasonal trends over time
- Sales method impacts overall profitability
""")

# ------------------ RAW DATA ------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)
