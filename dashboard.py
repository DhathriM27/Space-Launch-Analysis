import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Space Mission Dashboard", layout="wide")
st.title("🚀 Space Mission Analytics Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("space_mission_dataset.csv")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

# ---------------- SAFETY CHECK ----------------
required_cols = ["Success", "Cost_Million_USD", "Company", "Launch_Site", "Payload_kg"]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"❌ Missing columns in dataset: {missing}")
    st.stop()

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Missions", len(df))

# Success rate fix (robust handling)
success_rate = (df["Success"].astype(str).str.lower() == "success").mean() * 100
col2.metric("Success Rate", f"{success_rate:.1f}%")

col3.metric("Avg Cost (M USD)", round(df["Cost_Million_USD"].mean(), 2))

# ---------------- CHART 1: SUCCESS ----------------
st.subheader("🎯 Success Distribution")

fig1 = px.pie(
    df,
    names="Success"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CHART 2: COMPANY ----------------
st.subheader("🏢 Company Missions")

company_counts = df["Company"].value_counts().reset_index()
company_counts.columns = ["Company", "Count"]

fig2 = px.bar(
    company_counts,
    x="Company",
    y="Count"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- CHART 3: LAUNCH SITE ----------------
st.subheader("🚀 Launch Sites")

site_counts = df["Launch_Site"].value_counts().reset_index()
site_counts.columns = ["Launch_Site", "Count"]

fig3 = px.bar(
    site_counts,
    x="Launch_Site",
    y="Count"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- CHART 4: COST VS PAYLOAD ----------------
st.subheader("💰 Cost vs Payload")

df["Success"] = df["Success"].astype(str)  # safety fix

fig4 = px.scatter(
    df,
    x="Payload_kg",
    y="Cost_Million_USD",
    color="Success"
)

st.plotly_chart(fig4, use_container_width=True)