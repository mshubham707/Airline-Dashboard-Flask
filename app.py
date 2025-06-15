from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly
import json
from utils.kpis import revenue, passenger_count, ASK
from utils.charts import region_wise_revenue, market_revenue, top_market_revenue, top_market_paxcount, monthly_trend

app = Flask(__name__)

# Load data once to get list of available years
try:
    data = pd.read_csv("data/airline_monthly_data.csv")
    available_years = sorted(data['Year'].unique(), reverse=True)
except FileNotFoundError:
    print("Error: airline_monthly_data.csv not found. Please ensure it's in the 'data/' directory.")
    available_years = [2024] # Provide a default or handle error appropriately

@app.route("/")
@app.route("/home")
def home():
    # Default year for home page
    year = available_years[0]  # Use most recent year
    
    # Generate all charts including the multi-year trend
    fig1 = region_wise_revenue(year)
    fig2 = market_revenue(year)
    fig3 = top_market_revenue(year)
    fig4 = top_market_paxcount(year)    
    fig5 = monthly_trend()  # Multi-year chart (not year-specific)
    
    # Debug prints to verify data - kept for your reference
    print(f"--- Home Page ({year}) Data ---")
    print(f"Revenue (INR Mn) for Region-wise Revenue (fig1): {fig1.data[0].values[:5] if fig1.data else 'N/A'}")
    print(f"Revenue (INR Mn) for Market Revenue (fig2): {fig2.data[0].x[:5] if fig2.data else 'N/A'}")
    print(f"Revenue (INR Mn) for Top Market Revenue (fig3): {fig3.data[0].y[:5] if fig3.data else 'N/A'}")
    print(f"Passengers for Top Market Pax Count (fig4): {fig4.data[0].y[:5] if fig4.data else 'N/A'}")
    print(f"Monthly PRASK for Monthly Trend (fig5): {fig5.data[0].y[:5] if fig5.data else 'N/A'}")
    print("----------------------------")

    return render_template(
        "dashboard.html",
        total_revenue=revenue(year),
        total_passengers=passenger_count(year),
        total_ask=ASK(year),
        graph1=json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder),
        graph5=json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder),
        year=year,
        available_years=available_years,
        is_home=True  # Flag to identify home page
    )

@app.route("/<int:year>")
def dashboard(year):
    # Generate only year-specific charts
    fig1 = region_wise_revenue(year)
    fig2 = market_revenue(year)
    fig3 = top_market_revenue(year)
    fig4 = top_market_paxcount(year)
    
    # Debug prints to verify data - kept for your reference
    print(f"--- Dashboard Page ({year}) Data ---")
    print(f"Revenue (INR Mn) for Region-wise Revenue (fig1): {fig1.data[0].values[:5] if fig1.data else 'N/A'}")
    print(f"Revenue (INR Mn) for Market Revenue (fig2): {fig2.data[0].x[:5] if fig2.data else 'N/A'}")
    print(f"Revenue (INR Mn) for Top Market Revenue (fig3): {fig3.data[0].y[:5] if fig3.data else 'N/A'}")
    print(f"Passengers for Top Market Pax Count (fig4): {fig4.data[0].y[:5] if fig4.data else 'N/A'}")
    print("----------------------------")

    return render_template(
        "dashboard.html",
        total_revenue=revenue(year),
        total_passengers=passenger_count(year),
        total_ask=ASK(year),
        graph1=json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        graph2=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        graph3=json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        graph4=json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder),
        graph5=None,  # No multi-year chart on year-specific pages
        year=year,
        available_years=available_years,
        is_home=False  # Not home page
    )

if __name__ == "__main__":
    app.run(debug=True)
