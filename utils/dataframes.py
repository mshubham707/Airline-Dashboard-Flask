import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



df=pd.read_csv("data/airline_monthly_data.csv")

def data(df):

    df["Yield"]=(df["Revenue (INR Cr)"]/df["RPK (Mn km)"]).round(2)
    df["PRASK"]=(df["PRASK"]/10).round(2)
    df["Revenue (INR Mn)"]=df["Revenue (INR Cr)"]
    df.drop(columns=["Revenue (INR Cr)"], inplace=True)
    df["Market"]=df["Route"].apply(lambda x: "-".join(sorted(x.split("-"))))
    df["Cost (INR Mn)"]=df["CASK"]*df["ASK (Mn km)"]



    df["Month_Name"] = df["Month_Name"].str.capitalize()
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    df["Month_Name"] = pd.Categorical(df["Month_Name"], categories=month_order, ordered=True)

    return df

dataframe=data(df)

def monthly_data(df):
    pnl=df.groupby(["Year","Month_Name"])[["Revenue (INR Mn)","Cost (INR Mn)","ASK (Mn km)"]].sum().reset_index()
    pnl["Monthly_PRASK"]=(pnl["Revenue (INR Mn)"]/pnl["ASK (Mn km)"]).round(2)
    return pnl

md=monthly_data(dataframe)


def top_5_markets(year):
    df=dataframe
    group=df.groupby(['Year','Route'])["Passengers"].sum().reset_index().sort_values(by=["Passengers"], ascending=False)
    top_routes=group.groupby(["Year"]).head(5).reset_index(drop=True).sort_values(by=["Year","Passengers"], ascending=[True,False]).reset_index(drop=True)
    return top_routes[top_routes["Year"]==int(year)].reset_index(drop=True)

def Ask_data(year):
    ask_data=df[df["Year"]==int(year)].groupby(["Month_Name","Market"]).agg({"Revenue (INR Mn)":"sum","ASK (Mn km)":"sum"}).reset_index().sort_values(by=["Month_Name","Revenue (INR Mn)"], ascending=[True,False])
    ask_data.reset_index(drop=True, inplace=True)
    ask_data["Year"]=int(year)
    return ask_data






