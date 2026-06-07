import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Space Mission Dashboard", layout="wide")
st.title("🚀 Space Mission Analytics Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("space_mission_dataset.csv")
df.columns = df.columns.str.strip()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🎛 Filters")

# Company filter
companies = st.sidebar.multiselect(
    "Select Company",
    df["Company"].dropna().unique(),
    default=df["Company"].dropna().unique()
)

# Launch site filter
sites = st.sidebar.multiselect(
    "Select Launch Site",
    df["Launch_Site"].dropna().unique(),
    default=df["Launch_Site"].dropna().unique()
)

# Success filter
success_filter = st.sidebar.multiselect(
    "Mission Status",
    df["Success"].dropna().unique(),
    default=df["Success"].dropna().unique()
)

# Payload filter (slider)
min_payload = float(df["Payload_kg"].min())
max_payload = float(df["Payload_kg"].max())

payload_range = st.sidebar.slider(
    "Payload Range (kg)",
    min_value=min_payload,
    max_value=max_payload,
    value=(min_payload, max_payload)
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["Company"].isin(companies)) &
    (df["Launch_Site"].isin(sites)) &
    (df["Success"].isin(success_filter)) &
    (df["Payload_kg"].between(payload_range[0], payload_range[1]))
]

# ---------------- DATA PREVIEW ----------------
st.subheader("📊 Filtered Dataset")
st.dataframe(filtered_df)

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Missions", len(filtered_df))

success_rate = (
    filtered_df["Success"].astype(str).str.lower() == "success"
).mean() * 100 if len(filtered_df) > 0 else 0

col2.metric("Success Rate", f"{success_rate:.1f}%")

col3.metric(
    "Avg Cost (M USD)",
    round(filtered_df["Cost_Million_USD"].mean(), 2) if len(filtered_df) > 0 else 0
)

# ---------------- CHART 1: SUCCESS ----------------
st.subheader("🎯 Success Distribution")

fig1 = px.pie(filtered_df, names="Success")
st.plotly_chart(fig1, use_container_width=True)

# ---------------- CHART 2: COMPANY ----------------
st.subheader("🏢 Company Missions")

company_counts = filtered_df["Company"].value_counts().reset_index()
company_counts.columns = ["Company", "Count"]

fig2 = px.bar(company_counts, x="Company", y="Count")
st.plotly_chart(fig2, use_container_width=True)

# ---------------- CHART 3: LAUNCH SITE ----------------
st.subheader("🚀 Launch Sites")

site_counts = filtered_df["Launch_Site"].value_counts().reset_index()
site_counts.columns = ["Launch_Site", "Count"]

fig3 = px.bar(site_counts, x="Launch_Site", y="Count")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- CHART 4: COST VS PAYLOAD ----------------
st.subheader("💰 Cost vs Payload")

fig4 = px.scatter(
    filtered_df,
    x="Payload_kg",
    y="Cost_Million_USD",
    color="Success"
)

st.plotly_chart(fig4, use_container_width=True)