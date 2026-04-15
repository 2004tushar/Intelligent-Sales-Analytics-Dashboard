import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import re

# ─── Config
st.set_page_config(
    page_title="Intelligent Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# ─── File Setup
FILE_NAME = "user_details.csv"

if not os.path.exists(FILE_NAME):
    df_init = pd.DataFrame(columns=["First Name", "Last Name", "Email", "Phone No.", "username", "password"])
    df_init.to_csv(FILE_NAME, index=False)

# ─── Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Restore session from query params (so refresh doesn't log you out)
if "logged_in" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.username = st.query_params.get("user", "")

if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"

# LOADING DATA
@st.cache_data
def load_data():
    df = pd.read_csv("Sales_Data_Cleaned.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

# SIDEBAR FILTER
def sidebar_filter(df):
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<p style='font-family:Syne,sans-serif;font-size:0.7rem;"
        "text-transform:uppercase;letter-spacing:0.12em;"
        "color:#64748b;margin-bottom:0.5rem'>⚙ Global Filters</p>",
        unsafe_allow_html=True
    )

    years = ["All"] + sorted(df["Order Year"].unique().tolist())
    selected_year = st.sidebar.selectbox("Year", years)

    quarters = ["All"] + sorted(df["Order Quarter"].unique().tolist())
    selected_quarter = st.sidebar.selectbox("Quarter", quarters)

    region = ["All"] + sorted(df["Region"].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", region)

    categories = ["All"] + sorted(df["Category"].unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)

    # applying filter
    filtered = df.copy()
    if selected_year != "All":
        filtered = filtered[filtered["Order Year"] == selected_year]
    if selected_quarter != "All":
        filtered = filtered[filtered["Order Quarter"] == selected_quarter]
    if selected_region != "All":
        filtered = filtered[filtered["Region"] == selected_region]
    if selected_category != "All":
        filtered = filtered[filtered["Category"] == selected_category]

    st.sidebar.markdown(f"**{len(filtered)} records** match filters")
    return filtered


# Overview page
def page_overview(df, set_page):
    # ─── HERO SECTION ───
    st.markdown(f"""
        <div class="glass-card" style="margin-top: -1rem; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 2rem; flex-wrap: wrap;">
                <div style="flex: 2; min-width: 300px;">
                    <h1 style="margin-top: 0; font-size: 2.8rem !important;">Welcome back, <span style="color: var(--accent);">{st.session_state.username}</span>! 👋</h1>
                    <p style="font-size: 1.1rem; color: var(--text-soft); margin-bottom: 1.5rem;">
                        Your Intelligent Sales Command Center is ready. We've analyzed thousands of data points 
                        to bring you the most critical insights for today's strategy.
                    </p>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <span style="background: var(--accent-dim); color: var(--accent); padding: 0.5rem 1rem; border-radius: 50px; font-weight: 600; font-size: 0.8rem;">
                            🚀 Real-time Analytics
                        </span>
                        <span style="background: var(--accent-dim); color: var(--accent); padding: 0.5rem 1rem; border-radius: 50px; font-weight: 600; font-size: 0.8rem;">
                            🧠 AI-Powered Insights
                        </span>
                        <span style="background: var(--accent-dim); color: var(--accent); padding: 0.5rem 1rem; border-radius: 50px; font-weight: 600; font-size: 0.8rem;">
                            🇮🇳 Pan-India Scale
                        </span>
                    </div>
                </div>
                <div style="flex: 1; text-align: right; min-width: 200px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/3094/3094857.png" 
                         style="width: 100%; max-width: 220px; filter: drop-shadow(0 10px 15px rgba(59,130,246,0.3));">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── STRATEGIC SUMMARY ──
    col_t1, col_t2 = st.columns([1.8, 1])
    with col_t1:
        st.markdown("""
            <h2 style='margin-top: 0;'>📖 Strategic Context</h2>
            <p>This platform transforms retail complexity into clarity. By leveraging advanced data cleaning 
            and transformation scripts, we process thousands of pan-India orders to reveal the driving forces 
            behind your commercial performance.</p>
        """, unsafe_allow_html=True)

        with st.expander("📂 Technical Architecture — Dataset & Pipeline"):
            st.markdown("""
                **Dataset Dimensions:**
                - **Primary**: Sales, Profit, Discount, Quantity
                - **Temporal**: Year, Quarter, Month, Day of Week
                - **Geographic**: Region, State, City
                - **Categorical**: Category, Sub-Category, Profit Class

                **Cleaning Logic:**
                - Mean-imputation for transactional anomalies.
                - Automated feature engineering for Margin % and Revenue optimization.
                - ID standardization for relational integrity.
            """)
    with col_t2:
        st.markdown("""<div class="glass-card" style="padding: 1.5rem !important; border-left: 5px solid var(--accent);">
            <h3 style="margin-top:0">📊 Intelligence Pulse</h3>
            <div style="font-size: 0.85rem; line-height: 1.8;">
                <span style="color: var(--muted)">Volume:</span> <b>9000+ Records</b><br>
                <span style="color: var(--muted)">Scope:</span> <b>Pan-India Retail</b><br>
                <span style="color: var(--muted)">Quality:</span> <b>Cleaned & Validated</b><br>
                <span style="color: var(--muted)">Last Sink:</span> <b>Today</b>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.expander("📂 About the Dataset — Click to Read More"):
        st.markdown("""
            **Dataset: Sales Data**

            | Column | Description |
            |---|---|
            | `Order ID` | Unique identifier for each order (formatted as OD00001, OD00002, ...) |
            | `Customer Name` | Name of the customer who placed the order |
            | `Category` | Product category (e.g., Electronics, Clothing, Food) |
            | `Sub Category` | More specific product type within a category |
            | `City / State / Region` | Location where the order was placed |
            | `Order Date` | The exact date the order was placed |
            | `Sales` | Original sale amount before any discount |
            | `Discount` | Discount rate applied (0.0 to 1.0 scale) |
            | `Profit` | Actual profit earned from the order |
            | `Revenue After Discount` | Final revenue = Sales × (1 − Discount) |
            | `Profit Margin %` | (Profit ÷ Sales) × 100 — how efficient the sale was |
            | `Discount %` | Discount converted to percentage for easy reading |
            | `Profit Category` | Orders grouped as Low / Medium / High / Very High profit |
            | `Order Year / Month / Quarter / Day` | Date parts extracted for time-based analysis |
            | `Day of Week` | Which day of the week the order was placed |

            **Data Cleaning Steps Applied:**
            - Converted `Order Date` to proper datetime format and extracted year, month, quarter, day
            - Filled any missing values in Sales, Discount, Profit with column mean
            - Created derived columns: Revenue After Discount, Profit Margin %, Discount %, Profit Category
            - Reformatted Order IDs to a clean 5-digit format (OD00001)
            """)

    st.markdown("""
        **📊 What Each Module Analyses:**
        - **Sales Trends** — How revenue & profit change over time (monthly, quarterly, yearly patterns)
        - **Regional Analysis** — Which regions and cities contribute most to sales and profit
        - **Category Performance** — Which product categories drive revenue and which underperform
        - **Discount & Profit** — Does giving more discount always mean less profit? Find out here
        - **City-Wise Analysis** — A deep-dive into individual city performance metrics
        """)

    st.divider()

    # KPI Cards
    st.subheader("📌 Key Performance Indicators")
    total_revenue = df["Revenue After Discount"].sum()
    total_profit = df["Profit"].sum()
    avg_margin = df["Profit Margin %"].mean()
    avg_discount = df["Discount %"].mean()
    high_profit_share = (df["Profit Category"].isin(["High", "Very High"]).sum() / len(df)) * 100
    total_orders = len(df)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
    k2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
    k3.metric("🎯 Avg Profit Margin", f"{avg_margin:.1f}%")
    k4.metric("🏷️ Avg Discount Given", f"{avg_discount:.1f}%")
    k5.metric("⭐ High Profit Orders", f"{high_profit_share:.1f}%")
    k6.metric("🛒 Total Orders", f"{total_orders:,}")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()

    # Chart1 : Revenue by Region + profit Category split
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💹 Revenue by Region")
        region_rev = df.groupby("Region")["Revenue After Discount"].sum().reset_index()
        fig1 = px.bar(
            region_rev,
            x="Region",
            y="Revenue After Discount",
            color="Region",
            text_auto=".2s",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig1.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Profit Category Distribution")
        profit_dist = df["Profit Category"].value_counts().reset_index()
        profit_dist.columns = ["Profit Category", "Count"]
        fig2 = px.pie(
            profit_dist,
            names="Profit Category",
            values="Count",
            color_discrete_sequence=["#2ecc71", "#f39c12", "#e74c3c", "#3498db"],
            hole=0.4
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)

        # TOP 5 CITIES BY REVENUE + DAY-OF-WEEK SALES
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Top 10 Cities by Revenue")
        city_rev = df.groupby("City")["Revenue After Discount"].sum().nlargest(10).reset_index()
        fig3 = px.bar(
            city_rev,
            x="Revenue After Discount",
            y="City",
            orientation="h",
            color="Revenue After Discount",
            color_continuous_scale="Blues",
            text_auto=".2s"
        )
        fig3.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Sales by Day of Week")
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_sales = df.groupby("Day of Week")["Revenue After Discount"].sum().reindex(day_order).reset_index()
        fig4 = px.bar(
            day_sales,
            x="Day of Week",
            y="Revenue After Discount",
            color="Revenue After Discount",
            color_continuous_scale="Teal",
            text_auto=".2s"
        )
        fig4.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(fig4, use_container_width=True)

    # INTELLIGENT INSIGHTS
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.subheader("🤖 Intelligent Insights")
    i1, i2, i3, i4 = st.columns(4)

    best_region = df.groupby("Region")["Profit Margin %"].mean().idxmax()
    best_region_v = df.groupby("Region")["Profit Margin %"].mean().max()
    best_cat = df.groupby("Category")["Revenue After Discount"].sum().idxmax()
    best_cat_v = df.groupby("Category")["Revenue After Discount"].sum().max()
    best_quarter = df.groupby("Order Quarter")["Revenue After Discount"].sum().idxmax()
    worst_disc = df.groupby("Sub Category")["Discount %"].mean().idxmax()

    i1.success(f"🌍 **Top Region**\n\n{best_region} leads with {best_region_v:.1f}% avg margin.")
    i2.info(f"📦 **Best Category**\n\n{best_cat} is our primary revenue driver.")
    i3.warning(f"📅 **Peak Season**\n\n{best_quarter} shows the highest quarterly transaction volume.")
    i4.error(f"🏷️ **Most Discounted**\n\n{worst_disc} receives the highest avg discount — review pricing.")

    # 💹 REVENUE & PROFIT SECTION
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("💹 Regional Revenue & Profit Distribution")
    st.markdown("<h2 style='text-align: center; margin-top: 3rem;'>🗂️ Strategic Workspaces</h2>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: var(--text-soft); margin-bottom: 2rem;'>Dive deep into specific business dimensions using our specialized modules.</p>",
        unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)

    modules = [
        ("📈 Sales Trends", "Temporal patterns & forecasting", "nav_sales", "Sales Trends"),
        ("🌍 Regional", "Geographic performance", "nav_region", "Regional Analysis"),
        ("📦 Category", "Product line analytics", "nav_cat", "Category Performance"),
        ("🏷️ Discount", "Profitability & pricing", "nav_disc", "Discount & Profit"),
        ("🏙️ City Analysis", "Granular urban metrics", "nav_city", "City-Wise Analysis")
    ]

    cols = [m1, m2, m3, m4, m5]
    for i, (title, desc, key, page) in enumerate(modules):
        with cols[i]:
            st.markdown(f"""
                <div class="glass-card" style="padding: 1.2rem !important; height: 185px; text-align: center; display: flex; flex-direction: column; justify-content: space-between;">
                    <h3 style="margin: 0; font-size: 1.1rem;">{title}</h3>
                    <p style="font-size: 0.75rem; line-height: 1.3;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Explore →", key=key):
                set_page(page)

    st.divider()

    # DATASET EXPLORER
    st.divider()
    st.subheader("🔍 Dataset Explorer")
    st.markdown("Browse, search, and filter the raw sales data directly from here.")

    with st.expander("📋 Open Dataset Explorer", expanded=False):
        exp_col1, exp_col2, exp_col3 = st.columns(3)

        with exp_col1:
            search_city = st.text_input("🔎 Search by City", placeholder="e.g. Kanyakumari")
        with exp_col2:
            filter_category = st.selectbox("📦 Filter by Category", ["All"] + sorted(df["Category"].unique().tolist()))
        with exp_col3:
            filter_region = st.selectbox("🌍 Filter by Region", ["All"] + sorted(df["Region"].unique().tolist()))

        exp_col4, exp_col5 = st.columns(2)
        with exp_col4:
            filter_year = st.selectbox("📅 Filter by Year", ["All"] + sorted(df["Order Year"].unique().tolist()))
        with exp_col5:
            filter_profit_cat = st.selectbox("⭐ Filter by Profit Category",
                                             ["All", "Very High", "High", "Medium", "Low"])

        # Apply explorer filters
        df_explore = df.copy()
        if search_city:
            df_explore = df_explore[df_explore["City"].str.contains(search_city, case=False, na=False)]
        if filter_category != "All":
            df_explore = df_explore[df_explore["Category"] == filter_category]
        if filter_region != "All":
            df_explore = df_explore[df_explore["Region"] == filter_region]
        if filter_year != "All":
            df_explore = df_explore[df_explore["Order Year"] == filter_year]
        if filter_profit_cat != "All":
            df_explore = df_explore[df_explore["Profit Category"] == filter_profit_cat]

        st.caption(f"Showing **{len(df_explore):,}** records matching your filters")

        display_cols = ["Order ID", "Customer Name", "Category", "Sub Category", "City", "State",
                        "Region", "Order Date", "Sales", "Discount %", "Revenue After Discount",
                        "Profit", "Profit Margin %", "Profit Category"]

        st.dataframe(
            df_explore[display_cols].reset_index(drop=True).style.format({
                "Sales": "₹{:,.0f}",
                "Revenue After Discount": "₹{:,.0f}",
                "Profit": "₹{:,.0f}",
                "Profit Margin %": "{:.1f}%",
                "Discount %": "{:.1f}%"
            }).background_gradient(subset=["Profit Margin %"], cmap="RdYlGn"),
            use_container_width=True,
            height=400
        )

        dl_col1, dl_col2 = st.columns([3, 1])
        with dl_col2:
            csv_data = df_explore[display_cols].to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Filtered Data",
                data=csv_data,
                file_name="filtered_sales_data.csv",
                mime="text/csv"
            )

    # ── FOOTER ──
    st.markdown("""
        <div style="text-align: center; margin-top: 5rem; padding: 2rem; border-top: 1px solid var(--border);">
            <p style="color: var(--muted); font-size: 0.8rem;">
                <b>Intelligent Sales Analytics Platform</b> • Built for Strategic Growth<br>
                © 2026 Analytical Insights Inc. | Data Confidential
            </p>
        </div>
    """, unsafe_allow_html=True)


# SALES TRENDS
def page_sales_trends(df):
    st.title("Sales Trends")
    st.caption("Analyze How Revenue and Profit have changed over time.")
    st.divider()

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        metric = st.selectbox(
            "📊 Select Metric to Trend",
            ["Revenue After Discount", "Profit", "Sales", "Profit Margin %"]
        )
    with col_f2:
        granularity = st.selectbox(
            "⏱️ Granularity",
            ["Monthly", "Quarterly", "Yearly"]
        )
    st.divider()

    # YoY line chart

    st.subheader(f"Year-over-Year {metric} - {granularity}")

    if granularity == "Monthly":
        group_col = "Order Month"
        x_label = "Month"
        df_trend = df.groupby(["Order Year", "Order Month"])[metric].sum().reset_index()
        df_trend["x"] = df_trend["Order Month"]
        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        df_trend["x_label"] = df_trend["x"].map(month_names)

    elif granularity == "Quarterly":
        df_trend = df.groupby(["Order Year", "Order Quarter"])[metric].sum().reset_index()
        df_trend["x"] = df_trend["Order Quarter"]
        df_trend["x_label"] = df_trend["Order Quarter"]
    else:
        df_trend = df.groupby("Order Year")[metric].sum().reset_index()
        df_trend["x"] = df_trend["Order Year"]
        df_trend["x_label"] = df_trend["Order Year"].astype(str)

    if granularity == "Year":
        fig = px.bar(
            df_trend,
            x="x_label",
            y=metric,
            color_discrete_sequence=["#3498db"],
            text_auto=".2s"
        )
    else:
        fig = px.line(
            df_trend,
            x="x_label",
            y=metric,
            color="Order Year",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold,
            line_shape="spline"
        )
    fig.update_layout(xaxis_title= x_label if granularity == "Monthly" else "", yaxis_title=metric)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # MONTHLY REVENUE HEATMAP + QUARTER COMPARISON
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌡️ Monthly Revenue Heatmap (Year × Month)")
        heatmap_df = df.groupby(["Order Year", "Order Month"])["Revenue After Discount"].sum().reset_index()
        heatmap_pivot = heatmap_df.pivot(
            index="Order Year",
            columns="Order Month",
            values="Revenue After Discount"
        )
        heatmap_pivot.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        fig_h = px.imshow(
            heatmap_pivot,
            color_continuous_scale="RdYlGn",
            labels=dict(color= "Revenue (₹)"),
            aspect="auto"
        )
        fig_h.update_layout(xaxis_title="Month", yaxis_title="Year")
        st.plotly_chart(fig_h, use_container_width=True)

    with col2:
        st.subheader("📊 Quarterly Revenue Comparison")
        q_df = df.groupby(["Order Year", "Order Quarter"])["Revenue After Discount"].sum().reset_index()
        fig_q = px.bar(
            q_df,
            x="Order Quarter",
            y="Revenue After Discount",
            color="Order Year",
            barmode="group",
            text_auto=".2s",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            category_orders={"Order Quarter": ["Q1", "Q2", "Q3", "Q4"]}
        )
        fig_q.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Revenue (₹)"
        )
        st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CUMULATIVE REVENUE OVERTIME
    st.subheader("Cumulative Revenue Over Time")
    daily = df.groupby("Order Date")["Revenue After Discount"].sum().cumsum().reset_index()
    daily.columns = ["Date", "Cumulative Revenue"]
    fig_cum = px.area(
        daily,
        x="Date",
        y="Cumulative Revenue",
        color_discrete_sequence=["#2ecc71"]
    )
    fig_cum.update_layout(
        yaxis_title="Cumulative Revenue (₹)"
    )
    st.plotly_chart(fig_cum, use_container_width=True)

    # DAILY REVENUE BY ORDER DATE
    st.divider()
    st.subheader("📅 Daily Revenue by Order Date")
    st.caption("This shows revenue earned on each individual day. Spikes indicate high-sales days (festivals, promotions, etc.)")

    daily_rev = df.groupby("Order Date")["Revenue After Discount"].sum().reset_index()
    daily_rev.columns = ["Order Date", "Daily Revenue"]

    fig_daily = px.line(
        daily_rev,
        x="Order Date",
        y="Daily Revenue",
        color_discrete_sequence=["#e67e22"],
        line_shape="spline"
    )
    fig_daily.update_traces(fill="tozeroy", fillcolor="rgba(230, 126, 34, 0.15)")
    fig_daily.update_layout(
        xaxis_title="Order Date",
        yaxis_title="Revenue (₹)",
        hovermode= "x unified"
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

def page_regional(df):
    st.title("🌍 Regional Analysis")
    st.caption("Compare performance across regions and cities.")
    st.divider()

    # Filter: select region to compare
    all_regions = sorted(df['Region'].unique().tolist())
    selected_regions = st.multiselect("Select Region to Compare", all_regions, default=all_regions)
    if selected_regions:
        df = df[df['Region'].isin(selected_regions)]

    st.divider()

    # Region KPIs
    region_summary = df.groupby('Region').agg(
        Revenue=("Revenue After Discount", 'sum'),
        Profit= ('Profit', 'sum'),
        Orders=('Order ID', 'count'),
        Avg_Margin=('Profit Margin %', 'mean')
    ).reset_index()

    st.subheader("📋 Region Performance Summary")
    st.dataframe(
        region_summary.style.format({
            "Revenue": "₹{:,.0f}",
            "Profit": "{:,.0f}",
            "Orders": "{:,}",
            "Avg_Margin": "{:,.1f}%"
        }).background_gradient(subset=["Revenue", "Profit"], cmap="Greens"),
        use_container_width=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Revenue vs Profit by Region")
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Revenue", x=region_summary["Region"], y=region_summary["Revenue"],
                             marker_color="#3498db"))
        fig.add_trace(go.Bar(name="Profit", x=region_summary["Region"], y=region_summary["Profit"],marker_color="#2ecc71"))
        fig.update_layout(barmode='group', xaxis_title="", yaxis_title="Amount (₹)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Avg Profit Margin % by Region")
        fig2 = px.funnel(
            region_summary.sort_values("Avg_Margin", ascending=False), x="Avg_Margin", y="Region", color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Region x Category Heatmap
    st.subheader("🌡️ Region × Category Revenue Heatmap")
    hm = df.groupby(["Region", "Category"])["Revenue After Discount"].sum().reset_index()
    hm_pivot = hm.pivot(index="Region", columns="Category", values="Revenue After Discount").fillna(0)
    fig_hm = px.imshow(
        hm_pivot,
        color_continuous_scale="Blues",
        labels=dict(color="Revenue (₹)"),
        aspect="auto",
        text_auto=".2s"
    )
    fig_hm.update_layout(
        xaxis_title="Category",
        yaxis_title="Region"
    )
    st.plotly_chart(fig_hm, use_container_width=True)

    # City-level Breakdown
    st.subheader("🏙️ City-Level Revenue Breakdown")
    col3, col4 = st.columns([1, 2])
    with col3:
        top_n = st.slider("Show Top N Cities", 5, 24, 10)
        city_df = df.groupby("City")["Revenue After Discount"].sum().nlargest(top_n).reset_index()
        fig_c = px.bar(
            city_df,
            x="Revenue After Discount",
            y="City",
            orientation="h",
            color="Revenue After Discount",
            color_continuous_scale="Teal",
            text_auto=".2s"
        )
        fig_c.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_c, use_container_width=True)

def page_category(df):
    st.title("📦 Category Performance")
    st.caption("Deep-dive into product category and sub-category performance.")
    st.divider()

    # Filter
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        metric = st.selectbox("📊 Metric",["Revenue After Discount", "Profit", "Sales", "Profit Margin %"])

    with col_f2:
        view = st.selectbox("🔍 View By", ["Category", "Sub Category"])

    st.divider()

    # Bar + Treemap
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📊 {metric} by {view}")
        cat_df = df.groupby(view)[metric].sum().reset_index().sort_values(metric, ascending=True)
        fig = px.bar(
            cat_df,
            x=metric,
            y=view,
            orientation="h",
            color=metric,
            color_continuous_scale="Viridis",
            text_auto=".2s"
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🌳 Treemap — Category → Sub Category")
        tree_df = df.groupby(["Category", "Sub Category"])["Revenue After Discount"].sum().reset_index()
        fig2 = px.treemap(
            tree_df,
            path=["Category", "Sub Category"],
            values="Revenue After Discount",
            color="Revenue After Discount",
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Category × Quarter + Profit Category Distribution
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📅 Category Revenue by Quarter")
        cq_df = df.groupby(["Category", "Order Quarter"])["Revenue After Discount"].sum().reset_index()
        fig3 = px.bar(
            cq_df,
            x="Order Quarter",
            y="Revenue After Discount",
            color="Category",
            barmode="stack",
            category_orders={"Order Quarter": ["Q1", "Q2", "Q3", "Q4"]},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig3.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Revenue (₹)"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("⭐ Profit Category Share per Category")
        pc_df = df.groupby(["Category", "Profit Category"]).size().reset_index(name="Count")
        fig4 = px.bar(
            pc_df,
            x="Category",
            y="Count",
            color="Profit Category",
            barmode="stack",
            color_discrete_map={
                "Very High": "#27ae60",
                "High": "#2ecc71",
                "Medium": "#f39c12",
                "Low": "#e74c3c"
            }

        )
        fig4.update_layout(
            xaxis_tickangle=20,
            xaxis_title="",
            yaxis_title="Order Count"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Year-wise category trend
    st.subheader("📆 Category Revenue Trend Across Years")
    cy_df = df.groupby(["Order Year", "Category"])["Revenue After Discount"].sum().reset_index()
    fig5 = px.line(
        cy_df,
        x="Order Year",
        y="Revenue After Discount",
        color="Category",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig5.update_layout(xaxis_title="Year", yaxis_title="Revenue (₹)")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

def page_discount_profit(df):
    st.title("Discount & Profit Analysis")
    st.caption("Understand how discounting affects profitability.")
    st.divider()

    # FILTER
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        disc_range = st.slider("🔽 Filter by Discount % Range", 0, 100, (0, 100))

    with col_f2:
        profit_cats = st.multiselect(
            "⭐ Profit Category",
            ["Very high", "High", "Medium", "Low"],
            default=["Very high", "High", "Medium", "Low"]
        )

    df = df[
        (df["Discount %"] >= disc_range[0]) &
        (df["Discount %"] <= disc_range[1]) &
        (df["Profit Category"].isin(profit_cats))
    ]
    st.caption(f"📊 {len(df):,} records match selected filters")
    st.divider()

    # Scatter + Box

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Discount % vs Profit Margin % (Scatter)")
        fig = px.scatter(
            df,
            x="Discount %",
            y="Profit Margin %",
            color="Profit Category",
            size="Revenue After Discount",
            hover_data=["Category", "Sub Category"],
            color_discrete_map={
                "Very high": "#27ae60",
                "High": "#2ecc71",
                "Medium": "#f39c12",
                "Low": "#e74c3c"
            },
            opacity=0.6
        )
        fig.update_layout(xaxis_title="Discount %", yaxis_title="Profit Margin %")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Profit Margin Distribution by Category")
        fig2 = px.box(
            df,
            x="Category",
            y="Profit Margin %",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Safe,
            points="outliers"
        )
        fig2.update_layout(xaxis_tickangle=-20, showlegend=False, xaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    # Avg Discount by Category + Discount vs Revenue

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏷️ Avg Discount % by Category")
        disc_cat = df.groupby("Category")["Discount %"].mean().reset_index().sort_values("Discount %", ascending=False)
        fig3 = px.bar(
            disc_cat,
            x="Discount %",
            y="Category",
            orientation="h",
            color="Discount %",
            color_continuous_scale="Reds",
            text_auto=".1f"
        )
        fig3.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("📉 Avg Profit Margin by Discount Band")
        df["Discount Band"] = pd.cut(
            df["Discount %"],
            bins=[0, 10, 20, 30, 40, 50, 100],
            labels=["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50%+"]

        )
        band_df = df.groupby("Discount Band", observed=True)["Profit Margin %"].mean().reset_index()
        fig4 = px.bar(
            band_df,
            x="Discount Band",
            y="Profit Margin %",
            color="Profit Margin %",
            color_continuous_scale="RdYlGn",
            text_auto=".1f"
        )
        fig4.update_layout(coloraxis_showscale=False, xaxis_title="Discount Band", yaxis_title="Avg Profit Margin %")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Profit vs Revenue by Region
    st.subheader("🌍 Profit vs Revenue by Region & Category")
    bubble_df = df.groupby(["Region", "Category"]).agg(
        Revenue=("Revenue After Discount", "sum"),
        Profit=("Profit", "sum"),
        Avg_Discount=("Discount %", "mean")
    ).reset_index()
    fig5 = px.scatter(
        bubble_df,
        x="Revenue",
        y="Profit",
        size="Avg_Discount",
        color="Region",
        hover_data=["Category", "Avg_Discount"],
        color_discrete_sequence=px.colors.qualitative.Bold,
        size_max=40,
    )
    fig5.update_layout(xaxis_title="Revenue (₹)", yaxis_title="Profit (₹)")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

def page_city_analysis(df):
    st.title("🏙️ City-Wise Analysis")
    st.caption("Explore revenue, profit, and order trends across cities.")
    st.divider()

    # ── Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        all_states = sorted(df["State"].unique().tolist())
        selected_states = st.multiselect("Filter by State", all_states, default=[])
    with col_f2:
        metric = st.selectbox("📊 Metric", ["Revenue After Discount", "Profit", "Sales", "Profit Margin %"])

    if selected_states:
        df = df[df["State"].isin(selected_states)]

    st.caption(f"📊 Showing data for **{df['City'].nunique()} cities** | {len(df):,} records")
    st.divider()

    #KPI Row
    top_city_rev = df.groupby("City")["Revenue After Discount"].sum().idxmax()
    top_city_rev_val = df.groupby("City")["Revenue After Discount"].sum().max()
    top_city_profit = df.groupby("City")["Profit"].sum().idxmax()
    top_city_profit_val = df.groupby("City")["Profit"].sum().max()
    top_city_orders = df.groupby("City")["Order ID"].count().idxmax()
    top_city_orders_count = df.groupby("City")["Order ID"].count().max()
    avg_city_margin = df.groupby("City")["Profit Margin %"].mean().mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🏆 Top City (Revenue)", top_city_rev, f"₹{top_city_rev_val:,.0f}")
    k2.metric("💹 Top City (Profit)", top_city_profit, f"₹{top_city_profit_val:,.0f}")
    k3.metric("🛒 Most Orders City", top_city_orders, f"{top_city_orders_count:,.0f}")
    k4.metric("🎯 Avg City Margin", f"{avg_city_margin:.1f}%")

    st.divider()

    #Top N Cities Bar Chart
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"🏅 Top 10 Cities by {metric}")
        top_cities = df.groupby("City")[metric].sum().nlargest(10).reset_index()
        fig1 = px.bar(
            top_cities,
            x=metric,
            y="City",
            orientation="h",
            color=metric,
            color_continuous_scale="Blues",
            text_auto=".2s"
        )
        fig1.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    with col2:
        st.subheader("📉 Bottom 10 Cities by Revenue")
        bottom_cities = df.groupby("City")["Revenue After Discount"].sum().nsmallest(10).reset_index()
        fig2 = px.bar(
            bottom_cities,
            x="Revenue After Discount",
            y="City",
            orientation="h",
            color="Revenue After Discount",
            color_continuous_scale="Reds",
            text_auto=".2s"
        )
        fig2.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # City × Category Heatmap
    st.subheader("🌡️ Top 15 Cities × Category Revenue Heatmap")
    top15_cities = df.groupby("City")["Revenue After Discount"].sum().nlargest(15).index.tolist()
    hm_df = df[df["City"].isin(top15_cities)]
    hm = hm_df.groupby(["City", "Category"])["Revenue After Discount"].sum().reset_index()
    hm_pivot = hm.pivot(index="City", columns="Category", values="Revenue After Discount").fillna(0)
    fig_hm = px.imshow(
        hm_pivot,
        color_continuous_scale="YlGnBu",
        labels=dict(color="Revenue (₹)"),
        aspect="auto",
        text_auto=".2s"
    )
    fig_hm.update_layout(xaxis_title="Category", yaxis_title="City")
    st.plotly_chart(fig_hm, use_container_width=True)

    # City Profit Margin Scatter
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("📍 City Revenue vs Profit (Bubble Chart)")
        bubble = df.groupby("City").agg(
            Revenue=("Revenue After Discount", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "count")
        ).reset_index()
        fig3 = px.scatter(
            bubble,
            x="Revenue",
            y="Profit",
            size="Orders",
            hover_name="City",
            color="Profit",
            color_continuous_scale="RdYlGn",
            size_max=40
        )
        fig3.update_layout(xaxis_title="Revenue (₹)", yaxis_title="Profit (₹)")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("🎯 Avg Profit Margin % — Top 15 Cities")
        margin_city = df.groupby("City")["Profit Margin %"].mean().nlargest(15).reset_index()
        fig4 = px.bar(
            margin_city,
            x="Profit Margin %",
            y="City",
            orientation="h",
            color="Profit Margin %",
            color_continuous_scale="Greens",
            text_auto=".1f"
        )
        fig4.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    #City Summary Table
    st.subheader("📋 City-Wise Performance Summary")
    city_summary = df.groupby(["State", "City"]).agg(
        Revenue=("Revenue After Discount", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "count"),
        Avg_Margin=("Profit Margin %", "mean"),
        Avg_Discount=("Discount %", "mean")
    ).reset_index().sort_values("Revenue", ascending=False)

    st.dataframe(
        city_summary.style.format({
            "Revenue": "₹{:,.0f}",
            "Profit": "₹{:,.0f}",
            "Orders": "{:,}",
            "Avg_Margin": "{:.1f}%",
            "Avg_Discount": "{:.1f}%"
        }).background_gradient(subset=["Revenue", "Profit"], cmap="Blues"),
        use_container_width=True, hide_index=True
    )

def signup_page():
    df = pd.read_csv(FILE_NAME)

    st.title("📊 Intelligent Sales Analytics Dashboard")
    st.subheader("Create an Account")
    st.divider()

    st.info("**Quick Guide** --> Fill in all fields below. Your Email And User must be unique.")

    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="e.g. John")
        with col2:
            last_name = st.text_input("Last Name", placeholder="e.g. Cena")

        email = st.text_input("Email", placeholder="e.g. johncena@gmail.com")
        phone_no = st.text_input("Phone Number (10 digits)", placeholder="e.g. 9876543210", max_chars=10)
        username = st.text_input("Username", placeholder="e.g. john_cena or john1234")
        password = st.text_input("Password", type="password")
        re_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("✅ Register")

    if submit:
        # ── Validation

        if not first_name or not last_name or not email or not phone_no or not username or not password or not re_password:
            st.error("⚠️ Please fill in all the fields.")

        elif password != re_password:
            st.error("⚠️ Passwords do not match.")

        elif len(password) < 8:
            st.error("⚠️ Password must be at least 8 characters.")

        elif not re.search(r"[A-Z]", password):
            st.error("⚠️ Password must contain at least one uppercase letter.")

        elif not re.search(r"[!@#$%&*]", password):
            st.error("⚠️ Password must contain at least one special character (!@#$%&*).")

        elif not re.search(r"[0-9]", password):
            st.error("⚠️ Password must contain at least one number.")

        elif not re.match(r"^\d{10}$", phone_no):
            st.error("⚠️ Phone number must be exactly 10 digits.")

        elif email in df["Email"].values:
            st.warning("⚠️ This email is already registered.")

        elif username in df["username"].values:
            st.warning("⚠️ This username is already taken.")

        else:

            new_user = pd.DataFrame([{
                "First Name": first_name,
                "Last Name":  last_name,
                "Email":      email,
                "Phone No.":  phone_no,
                "username":   username,
                "password":   password,
            }])
            new_user.to_csv(FILE_NAME, mode="a", header=False, index=False)
            st.success("🎉 Account created! Please go to the Login page.")


def login_page():
    df = pd.read_csv(FILE_NAME)

    st.title("📊 Intelligent Sales Analytics Dashboard")
    st.subheader("Welcome Back")
    st.divider()

    st.info("**Tip** — Enter the username and password you used during registration. Don't have an account? Switch to the **Sign Up** tab.")

    username = st.text_input("Username", placeholder="e.g. john_cena or john1234")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    st.caption("New here? Use the **Sign Up** tab above to create a free account.")
    st.write("")

    if st.button("🔐 Login"):
        user = df[(df["username"] == username) & (df["password"] == password)]

        if not user.empty:
            st.success("✅ Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.query_params["logged_in"] = "true"
            st.query_params["user"] = username
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")


def dashboard_page():
    df_full = load_data()

    # Handle navigation from Overview buttons
    if "nav_target" not in st.session_state:
        st.session_state.nav_target = None

    all_pages = ["Overview", "Sales Trends", "Regional Analysis", "Category Performance", "Discount & Profit",
                 "City-Wise Analysis", "Logout"]

    # If a nav button was clicked, set default_index accordingly
    if st.session_state.nav_target in all_pages:
        default_idx = all_pages.index(st.session_state.nav_target)
        st.session_state.nav_target = None  # reset after use
    else:
        default_idx = 0

    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.write("---")
        selected = option_menu(
            menu_title="Navigation",
            options=all_pages,
            icons=["house-fill", "graph-up-arrow", "globe", "box-seam", "tag", "buildings", "box-arrow-right"],
            menu_icon="cast",
            default_index=default_idx
        )

        # Global filters (not shown on Logout)
        if selected != "Logout":
            df_filtered = sidebar_filter(df_full)

    def set_page(name):
        st.session_state.nav_target = name
        st.rerun()

    if selected == "Overview":
        page_overview(df_filtered, set_page)
    elif selected == "Sales Trends":
        page_sales_trends(df_filtered)
    elif selected == "Regional Analysis":
        page_regional(df_filtered)
    elif selected == "Category Performance":
        page_category(df_filtered)
    elif selected == "Discount & Profit":
        page_discount_profit(df_filtered)
    elif selected == "City-Wise Analysis":
        page_city_analysis(df_filtered)
    elif selected == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.query_params.clear()
        st.success("👋 Logged out successfully.")
        st.rerun()


if st.session_state.logged_in:
    dashboard_page()
else:
    st.title("📊 Intelligent Sales Analytics Dashboard")
    st.write("")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    with tab1:
        login_page()
    with tab2:
        signup_page()