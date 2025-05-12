"""
COVID-19 Data Dashboard
Built with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Page config
st.set_page_config(
    page_title="COVID-19 Global Data Tracker",
    page_icon="🦠",
    layout="wide"
)

# Title and description
st.title("🦠 COVID-19 Global Data Tracker")
st.markdown("""
This dashboard provides interactive visualizations of COVID-19 data worldwide.
Data source: Our World in Data
""")

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    df = pd.read_csv('data/owid-covid-data.csv')
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Replace negative values with NaN
    numeric_columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
                      'people_vaccinated', 'people_fully_vaccinated']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: np.nan if pd.isna(x) or x < 0 else x)
    
    # Filter out aggregated regions (like 'World', 'Europe', etc.)
    df = df[~df['location'].isin(['World', 'Europe', 'Asia', 'North America', 
                                 'South America', 'Africa', 'Oceania', 
                                 'European Union'])]
    
    # Forward fill missing values for cumulative columns
    cumulative_cols = ['total_cases', 'total_deaths', 'people_vaccinated', 
                       'people_fully_vaccinated']
    df[cumulative_cols] = df.groupby('location')[cumulative_cols].fillna(method='ffill')
    
    return df

# Load data
try:
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range selector
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(max_date - timedelta(days=30), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Country selector
    available_countries = sorted(df['location'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        available_countries,
        default=['United States', 'United Kingdom', 'India', 'Brazil', 'South Africa']
    )
    
    # Filter data based on selection
    mask = (
        (df['date'].dt.date >= date_range[0]) & 
        (df['date'].dt.date <= date_range[1]) & 
        (df['location'].isin(selected_countries))
    )
    filtered_df = df.loc[mask]
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Cases")
        fig_cases = px.line(
            filtered_df,
            x='date',
            y='new_cases',
            color='location',
            title='Daily New Cases by Country'
        )
        fig_cases.update_layout(height=400)
        st.plotly_chart(fig_cases, use_container_width=True)
    
    with col2:
        st.subheader("💉 Vaccination Progress")
        latest_vax = filtered_df.sort_values('date').groupby('location').last()
        fig_vax = px.bar(
            latest_vax,
            x=latest_vax.index,
            y='people_fully_vaccinated',
            title='Total People Fully Vaccinated',
            labels={'people_fully_vaccinated': 'People Fully Vaccinated'}
        )
        fig_vax.update_layout(height=400)
        st.plotly_chart(fig_vax, use_container_width=True)
    
    # Additional metrics
    st.subheader("📊 Key Metrics")
    metrics_cols = st.columns(4)
    
    latest_data = filtered_df[filtered_df['date'] == filtered_df['date'].max()]
    
    # Calculate metrics with proper error handling
    def format_metric(value):
        if pd.isna(value) or value == 0:
            return "N/A"
        return f"{value:,.0f}"
    
    def calculate_death_rate(deaths, cases):
        if pd.isna(deaths) or pd.isna(cases) or cases == 0:
            return "N/A"
        rate = (deaths / cases) * 100
        return f"{rate:.2f}%"
    
    with metrics_cols[0]:
        total_cases = latest_data['total_cases'].sum()
        st.metric("Total Cases", format_metric(total_cases))
    
    with metrics_cols[1]:
        total_deaths = latest_data['total_deaths'].sum()
        st.metric("Total Deaths", format_metric(total_deaths))
    
    with metrics_cols[2]:
        total_vaccinated = latest_data['people_fully_vaccinated'].sum()
        st.metric("Total Vaccinated", format_metric(total_vaccinated))
    
    with metrics_cols[3]:
        death_rate = calculate_death_rate(total_deaths, total_cases)
        st.metric("Average Death Rate", death_rate)
    
    # Detailed country comparison
    st.subheader("🌍 Country Comparison")
    comparison_metrics = ['total_cases', 'total_deaths', 'people_fully_vaccinated']
    selected_metric = st.selectbox("Select Metric", comparison_metrics)
    
    fig_comparison = px.bar(
        latest_data,
        x='location',
        y=selected_metric,
        title=f'{selected_metric.replace("_", " ").title()} by Country',
        color='location'
    )
    fig_comparison.update_layout(height=500)
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please make sure the data file is available in the data directory.")
