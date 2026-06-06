import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Space Mission Launch Analysis Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# Load Dataset
# -----------------------------------
df = pd.read_csv("mission_launches.csv")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# -----------------------------------
# Basic Preprocessing
# -----------------------------------
df = df.drop_duplicates()
df = df.fillna("")

# Convert Date column safely
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Create Year column
df['Year'] = df['Date'].dt.year

# Remove rows where Year is NaN
df = df.dropna(subset=['Year'])

df['Year'] = df['Year'].astype(int)

# -----------------------------------
# Title
# -----------------------------------
st.title("🚀 Global Space Mission Launch Analysis Dashboard")

st.markdown("""
This dashboard provides EDA on Space Launch Data:
- Trends over time
- Mission outcomes
- Organisation analysis
- Pivot table insights
""")

# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("Filters")

organisation = st.sidebar.selectbox(
    "Select Organisation",
    ["All"] + sorted(df['Organisation'].astype(str).unique())
)

mission_status = st.sidebar.selectbox(
    "Mission Status",
    ["All"] + sorted(df['Mission_Status'].astype(str).unique())
)

# Apply filters
filtered_df = df.copy()

if organisation != "All":
    filtered_df = filtered_df[filtered_df['Organisation'] == organisation]

if mission_status != "All":
    filtered_df = filtered_df[filtered_df['Mission_Status'] == mission_status]

# -----------------------------------
# KPI Cards
# -----------------------------------
st.subheader("📊 Dashboard Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Launches", len(filtered_df))
col2.metric("Organisations", filtered_df['Organisation'].nunique())
col3.metric("Mission Types", filtered_df['Mission_Status'].nunique())

# -----------------------------------
# Dataset Preview
# -----------------------------------
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)

# -----------------------------------
# Launches Per Year
# -----------------------------------
st.subheader("📈 Launches Per Year")

launches_per_year = filtered_df.groupby('Year').size().reset_index(name='Launches')

fig1 = px.line(
    launches_per_year,
    x='Year',
    y='Launches',
    markers=True,
    title="Launches Per Year"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------
# Mission Outcome Analysis
# -----------------------------------
st.subheader("✅ Mission Outcome Analysis")

mission_count = (
    filtered_df['Mission_Status']
    .value_counts()
    .reset_index()
)

mission_count.columns = ['Mission_Status', 'Count']

fig2 = px.bar(
    mission_count,
    x='Mission_Status',
    y='Count',
    title="Mission Outcome Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# Organisation Analysis
# -----------------------------------
st.subheader("🌍 Top Organisations")

org_count = (
    filtered_df['Organisation']
    .value_counts()
    .head(10)
    .reset_index()
)

org_count.columns = ['Organisation', 'Count']

fig3 = px.bar(
    org_count,
    x='Organisation',
    y='Count',
    title="Top 10 Organisations"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------
# Pivot Table
# -----------------------------------
st.subheader("📑 Pivot Table Analysis")

pivot_table = pd.pivot_table(
    filtered_df,
    index='Organisation',
    columns='Mission_Status',
    aggfunc='size',
    fill_value=0
)

st.dataframe(pivot_table, use_container_width=True)

# -----------------------------------
# Download Data
# -----------------------------------
st.subheader("⬇ Download Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_mission_launches.csv",
    mime="text/csv"
)

# -----------------------------------
# Observations
# -----------------------------------
st.subheader("🔍 Key Observations")

st.write("""
1. Launch trends show yearly progress of space missions.
2. Mission outcomes highlight success/failure distribution.
3. Organisations vary significantly in launch frequency.
4. Pivot table helps compare mission outcomes by organisation.
5. Filters allow interactive exploration of dataset.
""")