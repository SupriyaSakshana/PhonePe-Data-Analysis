import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 🔷 PAGE CONFIG
# ==============================
st.set_page_config(page_title="📊 PhonePe Dashboard", layout="wide")
st.title("📊 PhonePe Transaction Insights Dashboard")

# ==============================
# 🔷 LOAD ALL DATA (9 CSVs)
# ==============================
@st.cache_data
def load_data():
    agg_tr = pd.read_csv("agg_transaction.csv")
    agg_us = pd.read_csv("agg_user.csv")
    agg_in = pd.read_csv("agg_insurance.csv")

    map_tr = pd.read_csv("map_transaction.csv")
    map_us = pd.read_csv("map_user.csv")
    map_in = pd.read_csv("map_insurance.csv")

    top_tr = pd.read_csv("top_transaction.csv")
    top_us = pd.read_csv("top_user.csv")
    top_in = pd.read_csv("top_insurance.csv")

    return agg_tr, agg_us, agg_in, map_tr, map_us, map_in, top_tr, top_us, top_in

agg_tr, agg_us, agg_in, map_tr, map_us, map_in, top_tr, top_us, top_in = load_data()

# ==============================
# 🔷 SIDEBAR FILTERS
# ==============================
st.sidebar.header("🔎 Filters")

year = st.sidebar.selectbox("Select Year", sorted(map_tr["Year"].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(map_tr["Quarter"].unique()))
state = st.sidebar.selectbox("Select State", ["All"] + sorted(map_tr["State"].unique()))

# Filter Data
df_tr = map_tr[(map_tr["Year"] == year) & (map_tr["Quarter"] == quarter)]
df_in = map_in[(map_in["Year"] == year) & (map_in["Quarter"] == quarter)]

if state != "All":
    df_tr = df_tr[df_tr["State"] == state]
    df_in = df_in[df_in["State"] == state]

# ==============================
# 🔷 KPI SECTION
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Amount", f"₹ {df_tr['Amount'].sum():,.0f}")
col2.metric("🔢 Total Transactions", f"{df_tr['Count'].sum():,}")
col3.metric("🛡️ Insurance Amount", f"₹ {df_in['Amount'].sum():,.0f}")
col4.metric("📱 Total Users", f"{map_us['RegisteredUsers'].sum():,}")

st.markdown("---")

# ==============================
# 🔷 TABS
# ==============================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 State Analysis",
    "🏙️ District Analysis",
    "🛡️ Insurance",
    "📱 Device Insights",
    "🏆 Top Performers"
])

# ==============================
# 🔷 TAB 1: STATE ANALYSIS
# ==============================
with tab1:
    st.subheader("Top States by Transaction Amount")

    state_df = df_tr.groupby("State")["Amount"].sum().reset_index()
    state_df = state_df.sort_values(by="Amount", ascending=False).head(10)

    fig = px.bar(state_df, x="State", y="Amount", color="State")
    st.plotly_chart(fig, use_container_width=True)

    # Trend
    st.subheader("📈 Yearly Trend")
    trend = agg_tr.groupby(["Year"])["Amount"].sum().reset_index()
    fig2 = px.line(trend, x="Year", y="Amount", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 🔷 TAB 2: DISTRICT ANALYSIS
# ==============================
with tab2:
    st.subheader("Top Districts")

    dist_df = df_tr.groupby("District")["Count"].sum().reset_index()
    dist_df = dist_df.sort_values(by="Count", ascending=False).head(10)

    fig = px.bar(dist_df, x="District", y="Count", color="District")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# 🔷 TAB 3: INSURANCE
# ==============================
with tab3:
    st.subheader("Insurance by State")

    ins_df = df_in.groupby("State")["Amount"].sum().reset_index()
    ins_df = ins_df.sort_values(by="Amount", ascending=False)

    fig = px.bar(ins_df, x="State", y="Amount", color="State")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Insurance Trend")
    trend = agg_in.groupby(["Year"])["Amount"].sum().reset_index()
    fig2 = px.line(trend, x="Year", y="Amount", markers=True)
    st.plotly_chart(fig2)

# ==============================
# 🔷 TAB 4: DEVICE ANALYSIS
# ==============================
with tab4:
    st.subheader("Top Device Brands")

    brand_df = agg_us.groupby("Brand")["Count"].sum().reset_index()
    brand_df = brand_df.sort_values(by="Count", ascending=False).head(10)

    fig = px.bar(brand_df, x="Brand", y="Count", color="Brand")
    st.plotly_chart(fig, use_container_width=True)

# ==============================
# 🔷 TAB 5: TOP PERFORMERS
# ==============================
with tab5:
    st.subheader("Top States (Transaction)")

    top_state = top_tr.groupby("State")["Amount"].sum().reset_index()
    top_state = top_state.sort_values(by="Amount", ascending=False).head(10)

    fig = px.bar(top_state, x="State", y="Amount", color="State")
    st.plotly_chart(fig)

    st.subheader("Top Districts")

    top_dist = top_tr.groupby("District")["Amount"].sum().reset_index()
    top_dist = top_dist.sort_values(by="Amount", ascending=False).head(10)

    fig2 = px.bar(top_dist, x="District", y="Amount", color="District")
    st.plotly_chart(fig2)

# ==============================
# 🔷 FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Advanced PhonePe Dashboard | Built with Streamlit")