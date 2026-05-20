import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# Page configuration
# ---------------------------------------
st.set_page_config(
    page_title="Supply Chain Analysis Dashboard",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------
# Login credentials
# ---------------------------------------
USER_ID = "c"
PASSWORD = "ch01"


# ---------------------------------------
# Load dataset
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin1")
    return df


# ---------------------------------------
# Login page
# Left side: Login
# Right side: Message
# ---------------------------------------
def login():
    st.title("📦 Supply Chain Analysis Dashboard")

    with st.sidebar:
        st.subheader("🔐 Login")

        user_id = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Submit"):
            if user_id == USER_ID and password == PASSWORD:
                st.session_state["logged_in"] = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    st.subheader("Welcome to Supply Chain Analysis Web App")
    st.info("Please login from the left sidebar to access the dashboard.")


# ---------------------------------------
# Main dashboard
# Left side: User panel
# Right side: Dashboard charts and KPIs
# ---------------------------------------
def dashboard():
    st.title("📦 Supply Chain Analysis Dashboard")

    with st.sidebar:
        st.subheader("🔐 Login")
        st.success("Logged in")

        st.write("**User:**", USER_ID)

        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

    # Load data
    df = load_data()

    st.write("This web application shows supply chain KPIs and business analysis.")

    # ---------------------------------------
    # Dataset overview
    # ---------------------------------------
    st.subheader("Dataset Overview")

    col1, col2 = st.columns(2)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])

    with st.expander("View Dataset"):
        st.dataframe(df.head(100))

    # ---------------------------------------
    # Data quality checks
    # ---------------------------------------
    st.subheader("Data Quality Checks")

    duplicate_count = df.duplicated().sum()
    missing_count = df.isnull().sum().sum()

    col1, col2 = st.columns(2)
    col1.metric("Duplicate Rows", duplicate_count)
    col2.metric("Total Missing Values", missing_count)

    # ---------------------------------------
    # KPI calculations
    # ---------------------------------------
    st.subheader("Key Performance Indicators")

    total_sales = df["Sales per customer"].sum()
    average_sales = df["Sales per customer"].mean()
    total_profit = df["Benefit per order"].sum()
    average_shipping_days = df["Days for shipping (real)"].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Total Sales", f"{total_sales:,.2f}")
    kpi2.metric("Average Sales", f"{average_sales:,.2f}")
    kpi3.metric("Total Profit", f"{total_profit:,.2f}")
    kpi4.metric("Avg Shipping Days", f"{average_shipping_days:.2f}")

    # ---------------------------------------
    # Delivery status analysis
    # ---------------------------------------
    st.subheader("Delivery Status Analysis")

    delivery_status = df["Delivery Status"].value_counts().reset_index()
    delivery_status.columns = ["Delivery Status", "Count"]

    fig_delivery = px.bar(
        delivery_status,
        x="Delivery Status",
        y="Count",
        title="Delivery Status Distribution",
        text="Count"
    )

    st.plotly_chart(fig_delivery, use_container_width=True)

    # ---------------------------------------
    # Customer segment sales analysis
    # ---------------------------------------
    st.subheader("Customer Segment Sales Analysis")

    customer_segment_sales = (
        df.groupby("Customer Segment")["Sales per customer"]
        .sum()
        .reset_index()
        .sort_values(by="Sales per customer", ascending=False)
    )

    fig_segment = px.bar(
        customer_segment_sales,
        x="Customer Segment",
        y="Sales per customer",
        title="Sales by Customer Segment",
        text="Sales per customer"
    )

    st.plotly_chart(fig_segment, use_container_width=True)

    # ---------------------------------------
    # Category-wise sales analysis
    # ---------------------------------------
    st.subheader("Category-wise Sales Analysis")

    category_sales = (
        df.groupby("Category Name")["Sales per customer"]
        .sum()
        .reset_index()
        .sort_values(by="Sales per customer", ascending=False)
        .head(10)
    )

    fig_category = px.bar(
        category_sales,
        x="Category Name",
        y="Sales per customer",
        title="Top 10 Product Categories by Sales",
        text="Sales per customer"
    )

    st.plotly_chart(fig_category, use_container_width=True)

    # ---------------------------------------
    # Market-wise sales analysis
    # ---------------------------------------
    st.subheader("Market-wise Sales Analysis")

    market_sales = (
        df.groupby("Market")["Sales per customer"]
        .sum()
        .reset_index()
        .sort_values(by="Sales per customer", ascending=False)
    )

    fig_market = px.pie(
        market_sales,
        names="Market",
        values="Sales per customer",
        title="Sales Distribution by Market"
    )

    st.plotly_chart(fig_market, use_container_width=True)


# ---------------------------------------
# App execution
# ---------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    dashboard()
else:
    login()