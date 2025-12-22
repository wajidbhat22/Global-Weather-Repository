from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

df = pd.read_excel("clean global weather data.xlsx")
monthly = pd.read_csv("output_monthly_trends.csv")
regional = pd.read_csv("output_regional_comparison.csv")
corr = pd.read_csv("output_correlations.csv", index_col=0)


def fig_to_html(fig):
    return pio.to_html(fig, full_html=False)


@app.route("/")
def index():
    global_avg_temp = df["temperature_celsius"].mean()
    global_avg_humidity = df["humidity"].mean()
    global_avg_precip = df["precip_mm"].mean()
    global_avg_pm25 = df["air_quality_PM2.5"].mean()

    fig_temp = px.line(
        monthly,
        x="month",
        y="avg_temperature",
        markers=True,
        title="Global Average Temperature by Month",
    )

    fig_precip = px.bar(
        monthly,
        x="month",
        y="avg_precip",
        title="Global Average Precipitation by Month",
    )

    return render_template(
        "index.html",
        global_avg_temp=round(global_avg_temp, 2),
        global_avg_humidity=round(global_avg_humidity, 2),
        global_avg_precip=round(global_avg_precip, 2),
        global_avg_pm25=round(global_avg_pm25, 2),
        temp_plot=fig_to_html(fig_temp),
        precip_plot=fig_to_html(fig_precip),
    )


@app.route("/regions")
def regions():
    metric = request.args.get("metric", "avg_temperature")
    title_map = {
        "avg_temperature": "Average Temperature by Country",
        "avg_precip": "Average Precipitation by Country",
        "avg_uv": "Average UV Index by Country",
        "avg_pm25": "Average PM2.5 by Country",
    }
    if metric not in title_map:
        metric = "avg_temperature"

    fig_bar = px.bar(
        regional.sort_values(metric, ascending=False).head(30),
        x="country",
        y=metric,
        title=title_map[metric],
    )

    fig_choro = px.choropleth(
        regional,
        locations="country",
        locationmode="country names",
        color=metric,
        title=title_map[metric],
        color_continuous_scale="Viridis",
    )

    return render_template(
        "regions.html",
        metric=metric,
        bar_plot=fig_to_html(fig_bar),
        map_plot=fig_to_html(fig_choro),
    )


@app.route("/correlations")
def correlations_view():
    fig_heat = px.imshow(
        corr.values,
        x=corr.columns,
        y=corr.index,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Correlation Heatmap",
    )

    return render_template(
        "correlations.html",
        heatmap_plot=fig_to_html(fig_heat),
    )


@app.route("/extremes")
def extremes():
    metric = request.args.get("metric", "temperature_celsius")
    metric_map = {
        "temperature_celsius": "Temperature (°C)",
        "precip_mm": "Precipitation (mm)",
        "uv_index": "UV Index",
        "air_quality_PM2.5": "PM2.5",
    }
    if metric not in metric_map:
        metric = "temperature_celsius"
    series = df[metric].dropna()
    if series.empty:
        high_threshold = None
        low_threshold = None
        fig_high = None
        fig_low = None
    else:
        high_threshold = series.quantile(0.95)
        low_threshold = series.quantile(0.05)
        high_df = df[df[metric] >= high_threshold].copy()
        low_df = df[df[metric] <= low_threshold].copy()
        if "month" in high_df.columns:
            x_col = "month"
        else:
            x_col = "last_updated"
        fig_high = px.scatter(
            high_df,
            x=x_col,
            y=metric,
            color="country",
            title=f"Top 5% High {metric_map[metric]} Events",
        )
        fig_low = px.scatter(
            low_df,
            x=x_col,
            y=metric,
            color="country",
            title=f"Bottom 5% Low {metric_map[metric]} Events",
        )
    return render_template(
        "extremes.html",
        metric=metric,
        metric_map=metric_map,
        high_threshold=high_threshold,
        low_threshold=low_threshold,
        high_plot=fig_to_html(fig_high) if series.size else None,
        low_plot=fig_to_html(fig_low) if series.size else None,
    )


@app.route("/scatter")
def scatter():
    numeric_options = [
        "temperature_celsius",
        "humidity",
        "precip_mm",
        "uv_index",
        "air_quality_PM2.5",
        "air_quality_PM10",
    ]
    x_var = request.args.get("x", "temperature_celsius")
    y_var = request.args.get("y", "humidity")
    country = request.args.get("country", "All")
    if x_var not in numeric_options:
        x_var = "temperature_celsius"
    if y_var not in numeric_options:
        y_var = "humidity"
    countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
    if country != "All":
        data = df[df["country"] == country]
    else:
        data = df
    fig_scatter = px.scatter(
        data,
        x=x_var,
        y=y_var,
        color="country" if country == "All" else None,
        opacity=0.7,
        title=f"{y_var} vs {x_var}",
    )
    return render_template(
        "scatter.html",
        x_var=x_var,
        y_var=y_var,
        country=country,
        numeric_options=numeric_options,
        countries=countries,
        scatter_plot=fig_to_html(fig_scatter),
    )


if __name__ == "__main__":
    app.run(debug=True)


