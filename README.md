# COVID-19 Global Data Tracker

A comprehensive data analysis project that tracks and visualizes global COVID-19 trends through an interactive dashboard. Features real-time data exploration of cases, deaths, and vaccination progress worldwide.

## Project Overview

This project provides an interactive analysis of global COVID-19 data, offering real-time insights into pandemic trends. Using Python and Streamlit, we've created a dynamic dashboard that allows users to explore and visualize data from Our World in Data, tracking cases, deaths, recoveries, and vaccination rates across different countries and time periods.

## Objectives

- Import and clean COVID-19 global data
- Analyze time trends (cases, deaths, vaccinations)
- Compare metrics across countries/regions
- Visualize trends with charts and maps
- Generate comprehensive data insights

## Tools and Technologies

### Required Libraries
- pandas: Data manipulation and analysis
- matplotlib & seaborn: Static visualizations
- streamlit: Interactive web dashboard
- plotly: Interactive visualizations
- numpy: Numerical computations

### Optional Libraries
- geopandas: Geographical data handling
- jupyter: Notebook development

## Project Structure

```
├── data/
│   └── owid-covid-data.csv    # COVID-19 dataset from Our World in Data
├── dashboard/
│   └── app.py                 # Streamlit dashboard application
├── notebooks/
│   └── covid_analysis.py      # Analysis and visualization functions
├── reports/
│   └── covid19_analysis_report.md  # Detailed analysis report
├── visualizations/            # Generated visualization outputs
├── requirements.txt           # Project dependencies
└── README.md
```

## Getting Started

1. Clone this repository
2. Download the dataset from [Our World in Data](https://covid.ourworldindata.org/data/owid-covid-data.csv)
3. Place the dataset in the `data` directory
4. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
5. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the interactive dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
7. Open your browser and navigate to http://localhost:8501

## Features

### Interactive Dashboard
- Real-time data filtering by country and date range
- Dynamic visualizations of cases, deaths, and vaccinations
- Key metrics display with automatic updates
- Country comparison tools
- Raw data viewer

### Data Analysis
- Automated data cleaning and preprocessing
- Time series analysis of COVID-19 trends
- Vaccination progress tracking
- Cross-country comparisons
- Comprehensive insights and reporting

### Visualizations
- Interactive time series charts
- Comparative bar charts
- Key performance indicators
- Data tables with sorting and filtering

## Key Insights

1. Global Trends
   - Tracking of pandemic waves and their intensity
   - Vaccination impact on case/death rates
   - Regional variation in pandemic response

2. Vaccination Progress
   - Country-wise vaccination rates
   - Correlation with case reduction
   - Global vaccination disparities

3. Regional Comparisons
   - Different response strategies
   - Healthcare system impacts
   - Policy effectiveness

## Contributing

Feel free to fork this repository and submit pull requests with improvements or additional features.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data provided by [Our World in Data](https://ourworldindata.org/coronavirus)
- Project developed as part of the PLP Data Analysis curriculum using Python