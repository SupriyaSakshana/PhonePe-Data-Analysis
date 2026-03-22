import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 🔷 PAGE CONFIG
# ==============================
st.set_page_config(page_title="📊 PhonePe Dashboard", layout="wide")
st.title("📊 PhonePe Transaction Analysis Dashboard")

# ==============================
# 🔷 LOAD DATA
# ==============================
@st.cache_data
def load_data():
    map_tr = pd.read_csv("map_transaction.csv")
    map_in = pd.read_csv("map_insurance.csv")
    agg_us = pd.read_csv("agg_user.csv")
    return map_tr, map_in, agg_us

map_tr, map_in, agg_us = load_data()

# ==============================
# 🔷 SIDEBAR FILTERS
# ==============================
st.sidebar.header("🔎 Filters")

year = st.sidebar.selectbox("Select Year", sorted(map_tr["Year"].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(map_tr["Quarter"].unique()))
state = st.sidebar.selectbox("Select State", ["All"] + sorted(map_tr["State"].unique()))

# Apply Filters
df_tr = map_tr[(map_tr["Year"] == year) & (map_tr["Quarter"] == quarter)]
df_in = map_in[(map_in["Year"] == year) & (map_in["Quarter"] == quarter)]

if state != "All":
    df_tr = df_tr[df_tr["State"] == state]
    df_in = df_in[df_in["State"] == state]

# ==============================
# 🔷 KPI METRICS
# ==============================
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Transaction Amount", f"₹ {df_tr['Amount'].sum():,.0f}")
col2.metric("🔢 Total Transactions", f"{df_tr['Count'].sum():,}")
col3.metric("🛡️ Insurance Amount", f"₹ {df_in['Amount'].sum():,.0f}")

st.markdown("---")

# ==============================
# 🔷 TABS
# ==============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 State Analysis",
    "🏙️ District Analysis",
    "🛡️ Insurance",
    "📱 Device Insights"
])

# ==============================
# 🔷 TAB 1: STATE ANALYSIS
# ==============================
with tab1:
    st.subheader("🔝 Top States by Transaction Amount")

    state_df = df_tr.groupby("State")["Amount"].sum().reset_index()
    state_df = state_df.sort_values(by="Amount", ascending=False).head(10)

    fig = px.bar(state_df, x="State", y="Amount", color="State", title="Top States")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(state_df)

    # Pie Chart
    st.subheader("📊 Share of Top States")
    fig_pie = px.pie(state_df, names="State", values="Amount")
    st.plotly_chart(fig_pie, use_container_width=True)

# ==============================
# 🔷 TAB 2: DISTRICT ANALYSIS
# ==============================
with tab2:
    st.subheader("🏙️ Top Districts by Transactions")

    dist_df = df_tr.groupby("District")["Count"].sum().reset_index()
    dist_df = dist_df.sort_values(by="Count", ascending=False).head(10)

    fig = px.bar(dist_df, x="District", y="Count", color="District")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(dist_df)

# ==============================
# 🔷 TAB 3: INSURANCE ANALYSIS
# ==============================
with tab3:
    st.subheader("🛡️ Insurance Trends")

    ins_df = df_in.groupby("State")["Amount"].sum().reset_index()
    ins_df = ins_df.sort_values(by="Amount", ascending=False).head(10)

    fig = px.bar(ins_df, x="State", y="Amount", color="State")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(ins_df)

    # Trend over quarters
    trend = map_in.groupby(["Year", "Quarter"])["Amount"].sum().reset_index()

    fig2 = px.line(trend, x="Quarter", y="Amount", color="Year", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 🔷 TAB 4: DEVICE ANALYSIS
# ==============================
with tab4:
    st.subheader("📱 Device Brand Usage")

    brand_df = agg_us.groupby("Brand")["Count"].sum().reset_index()
    brand_df = brand_df.sort_values(by="Count", ascending=False).head(10)

    fig = px.bar(brand_df, x="Brand", y="Count", color="Brand")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(brand_df)

# ==============================
# 🔷 FOOTER
# ==============================
st.markdown("---")
st.caption("📌 Built with Streamlit | PhonePe Data Analysis Project")