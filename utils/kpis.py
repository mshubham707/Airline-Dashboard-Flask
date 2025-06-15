from utils.dataframes import dataframe
import pandas as pd


#Function to calculate revenue for a year
def revenue(year):
    df = dataframe
    revenue_value = float(df[df["Year"] == int(year)]["Revenue (INR Mn)"].sum())
    return f"{revenue_value}"

#Function to find out passenger count for a year
def passenger_count(year):
    df = dataframe
    return int(df[df["Year"] == int(year)]["Passengers"].sum())

#function to calculate ASK for a year
def ASK(year):
    df = dataframe
    ask_value = float(df[df["Year"] == int(year)]["ASK (Mn km)"].sum())
    return f"{ask_value}"