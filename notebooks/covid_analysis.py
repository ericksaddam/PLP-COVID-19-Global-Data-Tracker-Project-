"""
COVID-19 Global Data Analysis
This script contains the analysis code that will be used in our Jupyter notebook.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Load and prepare the dataset
def load_data():
    df = pd.read_csv('data/owid-covid-data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

# Data cleaning and preprocessing
def clean_data(df):
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
    df_clean[cumulative_cols] = df_clean.groupby('location')[cumulative_cols].fillna(method='ffill')
    
    return df_clean

# Analysis functions
def analyze_global_trends(df):
    # Group by date and calculate global totals
    global_daily = df.groupby('date').agg({
        'new_cases': 'sum',
        'new_deaths': 'sum',
        'total_cases': 'max',
        'total_deaths': 'max'
    }).reset_index()
    
    # Calculate 7-day moving averages
    global_daily['cases_7day_avg'] = global_daily['new_cases'].rolling(window=7).mean()
    global_daily['deaths_7day_avg'] = global_daily['new_deaths'].rolling(window=7).mean()
    
    # Calculate growth rates
    global_daily['case_growth_rate'] = global_daily['new_cases'].pct_change()
    global_daily['death_growth_rate'] = global_daily['new_deaths'].pct_change()
    
    return global_daily

def analyze_top_countries(df, metric='total_cases', n=10):
    # Get latest date for each country
    latest_data = df.sort_values('date').groupby('location').last().reset_index()
    
    # Remove rows where the metric is NaN
    latest_data = latest_data[latest_data[metric].notna()]
    
    # Get top countries
    top_countries = latest_data.nlargest(n, metric)[['location', metric]]
    
    # Sort in descending order
    top_countries = top_countries.sort_values(metric, ascending=False)
    
    return top_countries

def analyze_vaccination_progress(df):
    # Get latest vaccination data per country
    latest_vax = df.sort_values('date').groupby('location').last()
    latest_vax = latest_vax[['people_fully_vaccinated', 'people_vaccinated']]
    
    return latest_vax.sort_values('people_fully_vaccinated', ascending=False)

# Visualization functions
def plot_global_trends(global_daily):
    # Create figure with secondary y-axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Plot daily cases and 7-day average
    ax1.fill_between(global_daily['date'], global_daily['new_cases'], 
                    alpha=0.3, color='skyblue', label='Daily Cases')
    ax1.plot(global_daily['date'], global_daily['cases_7day_avg'], 
             color='blue', linewidth=2, label='7-day Average')
    ax1.set_title('Global Daily COVID-19 Cases', pad=20)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Number of Cases')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Format y-axis with comma separator
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Plot daily deaths and 7-day average
    ax2.fill_between(global_daily['date'], global_daily['new_deaths'], 
                    alpha=0.3, color='salmon', label='Daily Deaths')
    ax2.plot(global_daily['date'], global_daily['deaths_7day_avg'], 
             color='red', linewidth=2, label='7-day Average')
    ax2.set_title('Global Daily COVID-19 Deaths', pad=20)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Number of Deaths')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # Format y-axis with comma separator
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    plt.savefig('visualizations/global_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    return fig

def plot_top_countries(top_countries, metric='total_cases'):
    plt.figure(figsize=(12, 8))
    
    # Create bar plot
    bars = sns.barplot(data=top_countries, x=metric, y='location', 
                      palette='viridis')
    
    # Add value labels on the bars
    for i, v in enumerate(top_countries[metric]):
        bars.text(v, i, f' {format(int(v), ",")}', va='center')
    
    plt.title(f'Top Countries by {metric.replace("_", " ").title()}', pad=20)
    plt.xlabel(metric.replace('_', ' ').title())
    plt.ylabel('Country')
    
    # Format x-axis with comma separator
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'visualizations/top_countries_{metric}.png', dpi=300, bbox_inches='tight')
    plt.close()
    return plt.gcf()

def plot_vaccination_progress(vax_data, n=10):
    # Select top N countries and calculate vaccination rates
    plot_data = vax_data.head(n).copy()
    
    plt.figure(figsize=(14, 8))
    
    # Create colored bars with a gradient
    bars = plt.bar(range(len(plot_data.index)), 
                   plot_data['people_fully_vaccinated'],
                   color=plt.cm.viridis(np.linspace(0, 1, n)))
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{format(int(height), ",")}',
                 ha='center', va='bottom', rotation=0)
    
    plt.title('COVID-19 Vaccination Progress by Country', pad=20)
    plt.xlabel('Country')
    plt.ylabel('Number of People Fully Vaccinated')
    
    # Set x-axis labels
    plt.xticks(range(len(plot_data.index)), plot_data.index, rotation=45, ha='right')
    
    # Format y-axis with comma separator
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/vaccination_progress.png', dpi=300, bbox_inches='tight')
    plt.close()
    return plt.gcf()

# Main analysis workflow
def main():
    # Load data
    df = load_data()
    print("Data loaded successfully!")
    
    # Clean data
    df_clean = clean_data(df)
    print("Data cleaned successfully!")
    
    # Perform analyses
    global_trends = analyze_global_trends(df_clean)
    top_countries = analyze_top_countries(df_clean)
    vax_progress = analyze_vaccination_progress(df_clean)
    
    # Generate visualizations
    plot_global_trends(global_trends)
    plot_top_countries(top_countries)
    plot_vaccination_progress(vax_progress)
    
    return {
        'df': df_clean,
        'global_trends': global_trends,
        'top_countries': top_countries,
        'vax_progress': vax_progress
    }

if __name__ == "__main__":
    main()
