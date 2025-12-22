## Project Overview

This dashboard explores global weather and climate patterns using a cleaned global weather dataset. It focuses on distributions, correlations, seasonal patterns, extreme events, and regional comparisons.

## Data and Methodology

- Source: clean global weather data with country, location, coordinates, time, and multiple weather and air quality variables.
- Processing:
  - Loaded the data with pandas.
  - Computed statistical summaries for all numeric variables.
  - Calculated a correlation matrix across numeric variables.
  - Aggregated monthly trends for temperature, humidity, precipitation, and UV index.
  - Aggregated country-level averages for temperature, humidity, precipitation, UV index, and PM2.5.
  - Identified extreme events using 5th and 95th percentiles for temperature, precipitation, UV index, and PM2.5.

## Key Analyses

- Distributions
  - Basic statistics for temperature, humidity, precipitation, UV index, and air quality metrics.
- Correlations
  - Correlation matrix to see relationships between core climate and air quality variables.
- Seasonal Patterns
  - Monthly global averages for temperature, humidity, precipitation, and UV index to show seasonal cycles.
- Regional Comparisons
  - Country-level averages to highlight hottest, wettest, and most polluted regions.
- Extreme Events
  - High and low extremes detected via percentile thresholds for selected variables.

## Dashboard Design

- Overview Page
  - Global summary cards for average temperature, humidity, precipitation, and PM2.5.
  - Line chart of global average temperature by month.
  - Bar chart of global average precipitation by month.

- Regions Page
  - Metric selector for temperature, precipitation, UV, and PM2.5.
  - Bar chart of top countries by selected metric.
  - Choropleth map of the same metric by country.

- Correlations Page
  - Correlation heatmap of selected numeric variables.

## Implementation Details

- Backend: Flask
- Data handling: pandas
- Visualizations: Plotly (line, bar, choropleth, heatmap)
- Files:
  - analysis.py: generates summary CSV files for statistics, correlations, monthly trends, and regional comparisons.
  - app.py: Flask application defining dashboard routes and visualizations.
  - templates/: HTML templates for the dashboard pages.

## Testing and Validation

- Functional testing
  - Verified that each route (/, /regions, /correlations) loads successfully.
  - Confirmed that plots render correctly with the current dataset.
  - Checked that the metric selector on the regions page updates charts as expected.
- Data accuracy checks
  - Cross-checked dashboard values (e.g., global averages) against the generated CSV summaries.
  - Ensured that country and month groupings match expected aggregations.

## How to Run

1. Install dependencies:
   - pip install -r requirements.txt
2. Generate analysis outputs:
   - python analysis.py
3. Start the dashboard:
   - python app.py
4. Open the dashboard in a browser:
   - http://127.0.0.1:5000

## Future Enhancements

- Add an extreme events page with filters for variable, threshold, and region.
- Add more granular regional groupings (continents or custom regions).
- Add time controls to compare different periods if more temporal data is available.
- Enhance styling and add light/dark mode options.


