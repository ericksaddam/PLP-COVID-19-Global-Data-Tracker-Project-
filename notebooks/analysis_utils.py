"""
Utility functions for COVID-19 data analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

def setup_plotting_style():
    """Set up consistent plotting style"""
    plt.style.use('seaborn-v0_8')
    sns.set_theme(style="whitegrid", palette="husl")
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12

def load_and_clean_data(file_path='../data/owid-covid-data.csv'):
    """Load and clean the COVID-19 dataset"""
    # Load data
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # Select relevant columns
    cols = ['date', 'location', 'total_cases', 'new_cases', 
            'total_deaths', 'new_deaths', 'total_vaccinations', 
            'people_vaccinated', 'people_fully_vaccinated']
    df_clean = df[cols].copy()
    
    # Filter out aggregated regions
    excluded_locations = ['World', 'Europe', 'Asia', 'North America', 
                         'South America', 'Africa', 'Oceania', 
                         'European Union']
    df_clean = df_clean[~df_clean['location'].isin(excluded_locations)]
    
    # Handle negative values
    numeric_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths',
                   'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean.loc[df_clean[col] < 0, col] = np.nan
    
    # Forward fill missing values for cumulative columns
    cumulative_cols = ['total_cases', 'total_deaths', 'total_vaccinations',
                      'people_vaccinated', 'people_fully_vaccinated']
    df_clean[cumulative_cols] = df_clean.groupby('location')[cumulative_cols].ffill()
    
    return df_clean

def plot_country_trends(df, countries, metric='total_cases', start_date=None):
    """Plot trends for selected countries"""
    if start_date:
        df = df[df['date'] >= pd.to_datetime(start_date)]
    
    plt.figure(figsize=(12, 6))
    for country in countries:
        country_data = df[df['location'] == country]
        plt.plot(country_data['date'], country_data[metric], 
                label=country, linewidth=2)
    
    plt.title(f'{metric.replace("_", " ").title()} by Country')
    plt.xlabel('Date')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()

def create_interactive_plot(df, countries, metric='total_cases', start_date=None):
    """Create an interactive plot using Plotly"""
    if start_date:
        df = df[df['date'] >= pd.to_datetime(start_date)]
    
    df_filtered = df[df['location'].isin(countries)]
    
    fig = px.line(df_filtered, 
                  x='date', 
                  y=metric,
                  color='location',
                  title=f'{metric.replace("_", " ").title()} by Country',
                  labels={
                      'date': 'Date',
                      metric: metric.replace('_', ' ').title(),
                      'location': 'Country'
                  })
    
    return fig

def calculate_summary_stats(df, countries, metric='total_cases'):
    """Calculate summary statistics for selected countries"""
    latest_data = df[df['location'].isin(countries)].sort_values('date').groupby('location').last()
    summary = latest_data[[metric]].copy()
    summary['per_million'] = latest_data[f'{metric}_per_million']
    summary['rank'] = summary[metric].rank(ascending=False)
    return summary.sort_values(metric, ascending=False)

def plot_vaccination_progress(df, countries):
    """Plot vaccination progress for selected countries"""
    latest_data = df[df['location'].isin(countries)].sort_values('date').groupby('location').last()
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(latest_data.index, 
                   latest_data['people_fully_vaccinated'])
    
    plt.title('Vaccination Progress by Country')
    plt.xlabel('Country')
    plt.ylabel('People Fully Vaccinated')
    plt.xticks(rotation=45)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    return plt.gcf()
