import pandas as pd
import numpy as np


def load_data(path="clean global weather data.xlsx"):
    return pd.read_excel(path)


def basic_statistics(df):
    numeric_cols = df.select_dtypes(include=["number"])
    summary = numeric_cols.describe(percentiles=[0.25, 0.5, 0.75]).T
    return summary


def correlations(df):
    numeric_cols = df.select_dtypes(include=["number"])
    corr = numeric_cols.corr()
    return corr


def monthly_trends(df):
    if "month" not in df.columns:
        return None
    grouped = df.groupby("month").agg(
        avg_temperature=("temperature_celsius", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_precip=("precip_mm", "mean"),
        avg_uv=("uv_index", "mean"),
    ).reset_index()
    return grouped


def regional_comparison(df):
    grouped = df.groupby("country").agg(
        avg_temperature=("temperature_celsius", "mean"),
        avg_humidity=("humidity", "mean"),
        avg_precip=("precip_mm", "mean"),
        avg_uv=("uv_index", "mean"),
        avg_pm25=("air_quality_PM2.5", "mean"),
    ).reset_index()
    return grouped


def extreme_events(df):
    numeric_cols = ["temperature_celsius", "precip_mm", "uv_index", "air_quality_PM2.5"]
    extremes = {}
    for col in numeric_cols:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if series.empty:
            continue
        high_threshold = series.quantile(0.95)
        low_threshold = series.quantile(0.05)
        extremes[col] = {
            "high_threshold": float(high_threshold),
            "low_threshold": float(low_threshold),
            "high_events": df[df[col] >= high_threshold][
                ["country", "location_name", "month", col]
            ],
            "low_events": df[df[col] <= low_threshold][
                ["country", "location_name", "month", col]
            ],
        }
    return extremes


def save_summary_outputs(df):
    stats = basic_statistics(df)
    corr = correlations(df)
    monthly = monthly_trends(df)
    regional = regional_comparison(df)
    stats.to_csv("output_basic_statistics.csv")
    corr.to_csv("output_correlations.csv")
    if monthly is not None:
        monthly.to_csv("output_monthly_trends.csv", index=False)
    if regional is not None:
        regional.to_csv("output_regional_comparison.csv", index=False)


def main():
    df = load_data()
    save_summary_outputs(df)


if __name__ == "__main__":
    main()


