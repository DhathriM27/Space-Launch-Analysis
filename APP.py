import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Space Launch Analysis Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv("space_launches.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# -----------------------------------
# Basic Preprocessing
# -----------------------------------

# Missing value handling
df.fillna("Unknown", inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Convert date column
df['Launch Date'] = pd.to_datetime(
    df['Launch Date'],
    errors='coerce'
)

# Create Year column
df['Year'] = df['Launch Date'].dt.year

# -----------------------------------
# Title
# -----------------------------------

st.title("🚀 Global Space Launch Analysis Dashboard")

st.markdown(
    """
    This dashboard performs Exploratory Data Analysis (EDA)
    on Space Launch data including:
    
    - Data preprocessing
    - Missing value handling
    - Time-series analysis
    - Country analysis
    - Mission outcome analysis
    - Pivot table analysis
    """
)

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] +
    sorted(df['Customer Country'].astype(str).unique())
)

mission = st.sidebar.selectbox(
    "Mission Outcome",
    ["All"] +
    sorted(df['Mission Outcome'].astype(str).unique())
)

# Apply filters

filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df['Customer Country'] == country
    ]

if mission != "All":
    filtered_df = filtered_df[
        filtered_df['Mission Outcome'] == mission
    ]

# -----------------------------------
# KPI Cards
# -----------------------------------

st.subheader("📊 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Launches",
    len(filtered_df)
)

col2.metric(
    "Countries",
    filtered_df['Customer Country'].nunique()
)

col3.metric(
    "Vehicle Types",
    filtered_df['Vehicle Type'].nunique()
)

col4.metric(
    "Customers",
    filtered_df['Customer Name'].nunique()
)

# -----------------------------------
# Dataset Preview
# -----------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df.head(20))

# -----------------------------------
# Launches Per Year
# -----------------------------------

st.subheader("📈 Launches Per Year")

launches_per_year = (
    filtered_df.groupby('Year')
    .size()
    .reset_index(name='Launches')
)

fig1 = px.line(
    launches_per_year,
    x='Year',
    y='Launches',
    markers=True,
    title="Launches Per Year"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -----------------------------------
# Mission Outcome Analysis
# -----------------------------------

st.subheader("✅ Mission Outcome Analysis")

mission_count = (
    filtered_df['Mission Outcome']
    .value_counts()
    .reset_index()
)

mission_count.columns = [
    'Mission Outcome',
    'Count'
]

fig2 = px.bar(
    mission_count,
    x='Mission Outcome',
    y='Count',
    title="Mission Outcome Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# Country Analysis
# -----------------------------------

st.subheader("🌍 Top Customer Countries")

country_count = (
    filtered_df['Customer Country']
    .value_counts()
    .head(10)
    .reset_index()
)

country_count.columns = [
    'Country',
    'Launches'
]

fig3 = px.bar(
    country_count,
    x='Country',
    y='Launches',
    title="Top 10 Countries"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# Vehicle Type Analysis
# -----------------------------------

st.subheader("🚀 Vehicle Type Distribution")

vehicle_count = (
    filtered_df['Vehicle Type']
    .value_counts()
    .head(10)
    .reset_index()
)

vehicle_count.columns = [
    'Vehicle Type',
    'Count'
]

fig4 = px.pie(
    vehicle_count,
    values='Count',
    names='Vehicle Type',
    title="Vehicle Type Distribution"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -----------------------------------
# Pivot Table
# -----------------------------------

st.subheader("📑 Pivot Table Analysis")

pivot_table = pd.pivot_table(
    filtered_df,
    values='Flight Number',
    index='Customer Country',
    columns='Mission Outcome',
    aggfunc='count',
    fill_value=0
)

st.dataframe(pivot_table)

# -----------------------------------
# Download Filtered Data
# -----------------------------------

st.subheader("⬇ Download Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_space_launches.csv",
    mime="text/csv"
)

# -----------------------------------
# Observations
# -----------------------------------

st.subheader("🔍 Key Observations")

st.write("""
1. Launch activity trends can be observed from the yearly launch graph.
2. Mission outcomes help evaluate launch success and failure rates.
3. Some countries contribute significantly more launches than others.
4. Vehicle type distribution highlights the most frequently used launch vehicles.
5. Pivot table analysis helps compare mission outcomes across countries.
6. Interactive filters allow detailed exploration of launch data.
""")