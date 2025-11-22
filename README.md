Global Weather Data Cleaning and Preprocessing
This repository contains the Jupyter Notebook used for comprehensive data cleaning and preprocessing of the 'Global Weather Repository' dataset. The goal is to transform raw weather data into a clean, consistent, and analysis-ready format.

Project Overview
The project focuses on preparing a global weather dataset for further analysis. This involves identifying and handling missing values and anomalies, standardizing units, converting data types, normalizing numerical features, and aggregating data for easier trend analysis. The final cleaned dataset is saved as 'cleaned_global_weather_data.csv'.

Dataset
The primary dataset used is master_dataset.csv (originally 'Global Weather Repository.csv' from Kaggle).

Setup and Environment
To run this notebook, you will need a Python environment with the following libraries:

pandas (for data manipulation)
numpy (for numerical operations, especially with NaN values)
scikit-learn (specifically MinMaxScaler for normalization)
You can install these using pip:

pip install pandas numpy scikit-learn
Data Cleaning and Preprocessing Steps
The following steps were performed to clean and preprocess the data:

Data Loading and Initial Inspection: The dataset was loaded, and its structure, data types, and basic statistics were inspected using df.info(), df.head(), and df.describe().
Missing Value and Anomaly Handling: Erroneous sentinel values (e.g., -9999, -1848.15) in air quality columns and extreme outliers in wind and pressure data were identified and replaced with np.nan. All np.nan values were then imputed using the median of their respective columns.
Data Type Conversions:
last_updated, sunrise, sunset, moonrise, and moonset columns were converted to datetime objects.
The moon_phase column was converted to a categorical data type.
Unit Standardization: Imperial unit columns (temperature_fahrenheit, wind_mph, pressure_in, precip_in, visibility_miles, gust_mph) were dropped to standardize the dataset to metric units.
Value Normalization: Key numerical features (e.g., temperature_celsius, wind_kph, pressure_mb, air_quality_Carbon_Monoxide, etc.) were normalized using MinMaxScaler to a range between 0 and 1.
Data Aggregation: A new 'month' column was extracted from last_updated. Monthly average temperatures (temperature_celsius) were calculated by grouping data by 'country' and 'month'.
Output
The cleaned and preprocessed dataset is saved as cleaned_global_weather_data.csv in the root directory of the project.

How to Use
Clone this repository.
Place your master_dataset.csv file in the same directory as the notebook.
Open and run the Jupyter Notebook (your_notebook_name.ipynb).
The cleaned_global_weather_data.csv file will be generated upon successful execution.
Conclusion
This project provides a robust framework for cleaning and preparing global weather data, ensuring its quality and readiness for subsequent analysis, such as trend identification, predictive modeling, or geographical studies.
