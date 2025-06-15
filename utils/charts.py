from utils.dataframes import dataframe, Ask_data, top_5_markets, md
import pandas as pd
import plotly.express as px


#Region wise distibution of revenue
def region_wise_revenue(year):
    region_data=dataframe.groupby(["Region","Year"])[["Revenue (INR Mn)","Passengers","ASK (Mn km)"]].sum().reset_index()
    data=region_data[region_data["Year"]==year]
    fig=px.pie(data,
            values="Revenue (INR Mn)",
            names="Region",
            title="Revenue by Region"
            )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        title_text=f"Revenue by Region {year}",
        title_x=0.5,
        template="plotly_white"

    )

    return fig

#Market wise distribution of revenue
def market_revenue(year):
    ask_data=Ask_data(year)
    df=dataframe
    market_data=df.groupby(["Market","Month_Name","Year"])["Passengers"].sum().reset_index()
    merged_data=ask_data.merge(market_data[["Passengers","Year","Month_Name","Market"]],on=["Year","Month_Name","Market"], how="left")
    market_data=merged_data.groupby("Market")[["Revenue (INR Mn)","ASK (Mn km)","Passengers"]].sum().reset_index()

    fig=px.scatter(market_data,x=market_data["Revenue (INR Mn)"], y=market_data["Passengers"],
                color="Market", 
                title=f"Market wise distribution for {year}",
                    size="ASK (Mn km)",
                    
                    hover_data=["Passengers"]
                )
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        xaxis_title="Revenue (INR Mn)",
        yaxis_title="Passengers",
        legend_title="Market",
        template="plotly_white"
    )
    return fig

#Monthwise top 5 markets by revenue
def top_market_revenue(year):
    ask_data=Ask_data(year)
    top_markets=ask_data.groupby(["Month_Name"]).head(5).reset_index(drop=True)

    fig=px.scatter(top_markets, x="Month_Name", y="Revenue (INR Mn)",
                color="Market", 
                title=f"Top 5 Markets Monthwise for {year}",
                    size="ASK (Mn km)",
                    size_max=30
                )
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (INR Mn)",
        legend_title="Market",
        template="plotly_white"
    )

    return fig 
#Top 5 routes by passenger count
def top_market_paxcount(year):
    top_markets_data = top_5_markets(year)  # Call once and store
    fig = px.bar(top_markets_data, x="Route", y="Passengers",
            color="Passengers",
            title=f"Top 5 Routes by Passenger Count in {year}",
            text="Passengers",
            color_continuous_scale="Viridis"
    )
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        xaxis_title="Route",
        yaxis_title="Passenger Count",
        legend_title="Passenger Count",
        template="plotly_white",

    )
    return fig

#Monthly PRASK trend 
def monthly_trend():
    pnl=md
    pnl["shifted_year"]=pnl["Year"].astype(int)-1
    pnl_shifted=pnl.copy()
    yoydif=pnl_shifted.merge(pnl[["Year","shifted_year","Month_Name","Monthly_PRASK"]],
                              left_on=["shifted_year","Month_Name"], right_on=["Year","Month_Name"],
                                how="left", suffixes=("_o", "_n"))
    yoydif["YoY"]=round((yoydif["Monthly_PRASK_o"]-yoydif["Monthly_PRASK_n"])/yoydif["Monthly_PRASK_n"]*100,2).astype(str) +"%"
    yoydif["YoY"]=yoydif["YoY"].replace("nan%","")
    yoydif.rename(columns={"Monthly_PRASK_o":"Monthly_PRASK", "Monthly_PRASK_n":"Monthly_PRASK_prev","Year_o":"Year"}, inplace=True)
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    fig=px.line(yoydif, x="Month_Name", y="Monthly_PRASK",
                color="Year",
                title="Monthly PRASK Trend for All Years",
                labels={"Monthly_PRASK":"PRASK (INR)"},
                markers=True,
                category_orders={"Month_Name": month_order},
                hover_data=["YoY"],
                text="Monthly_PRASK"
                )
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), textposition="top center")
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="PRASK (INR)",
        legend_title="Year",
        template="plotly_white"

    )
    return fig