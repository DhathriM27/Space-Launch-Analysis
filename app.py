import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Space Missions Dashboard", layout="wide")

st.title("🚀 Space Missions Analysis Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("mission_launches.csv")  # change filename if needed

# =========================
# CLEAN COLUMN NAMES (IMPORTANT FIX)
# =========================
df.columns = df.columns.str.strip()

# Show columns for debugging (you can remove later)
st.write("📌 Columns in dataset:", df.columns.tolist())

# =========================
# HANDLE DATE COLUMN SAFELY
# =========================
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print(df[['Date']].head())

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

if "Organisation" in df.columns:
    org = st.sidebar.multiselect(
        "Organisation",
        df["Organisation"].dropna().unique()
    )
else:
    org = []

if org:
    df = df[df["Organisation"].isin(org)]

# =========================
# BASIC METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Missions", len(df))

if "Mission_Status" in df.columns:
    success_rate = (df["Mission_Status"].str.lower() == "success").mean() * 100
    col2.metric("Success Rate (%)", f"{success_rate:.2f}")
else:
    col2.metric("Success Rate (%)", "N/A")

if "Price" in df.columns:
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    col3.metric("Avg Cost", f"{df['Price'].mean():.2f}")
else:
    col3.metric("Avg Cost", "N/A")

# =========================
# YEAR EXTRACTION
# =========================
df["Year"] = df["Date"].dt.year

st.subheader("📊 Missions per Year")
year_counts = df["Year"].value_counts().sort_index()
st.bar_chart(year_counts)

# =========================
# RAW DATA
# =========================
st.subheader("📄 Dataset Preview")
st.dataframe(df)