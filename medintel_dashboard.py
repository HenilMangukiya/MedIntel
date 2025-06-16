import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/medintel.db")
df = pd.read_sql("SELECT * FROM drug_events", conn)

st.set_page_config(page_title="MedIntel Dashboard", layout="wide")

# Title
st.title("💊 MedIntel - Real-Time Drug Event Dashboard")

# Filters
with st.sidebar:
    st.header("🔍 Filters")

    # Filter by date (if exists)
    if "receivedate" in df.columns:
        df["receivedate"] = pd.to_datetime(df["receivedate"], errors="coerce")
        start_date = st.date_input("From Date", df["receivedate"].min())
        end_date = st.date_input("To Date", df["receivedate"].max())

        df = df[(df["receivedate"] >= pd.to_datetime(start_date)) & (df["receivedate"] <= pd.to_datetime(end_date))]

    # Filter by seriousness
    if "serious" in df.columns:
        serious_filter = st.selectbox("Serious Cases Only?", ["All", "Yes (1)", "No (2)"])
        if serious_filter == "Yes (1)":
            df = df[df["serious"] == 1]
        elif serious_filter == "No (2)":
            df = df[df["serious"] == 2]

# Show Data
st.subheader("📋 Filtered Drug Event Records")
st.dataframe(df, use_container_width=True)

# Charts
if "serious" in df.columns:
    st.subheader("📊 Serious vs Non-Serious Cases")
    serious_count = df["serious"].value_counts().rename({1: "Serious", 2: "Non-Serious"})
    st.bar_chart(serious_count)

if "receivedate" in df.columns:
    st.subheader("🕒 Events Over Time")
    time_chart = df.groupby(df["receivedate"].dt.date).size()
    st.line_chart(time_chart)

    st.markdown("---")
st.header("🦠 COVID-19 Stats by Country")

conn = sqlite3.connect("data/medintel.db")
df_covid = pd.read_sql("SELECT * FROM covid_data", conn)

# Country filter
selected_country = st.selectbox("Select Country", sorted(df_covid["country"].unique()))
df_selected = df_covid[df_covid["country"] == selected_country]

# Show stats
if not df_selected.empty:
    st.metric("Total Cases", int(df_selected["cases"].values[0]))
    st.metric("Total Deaths", int(df_selected["deaths"].values[0]))
    st.metric("Active", int(df_selected["active"].values[0]))
    st.metric("Recovered", int(df_selected["recovered"].values[0]))
    st.metric("Tests Done", int(df_selected["tests"].values[0]))
    st.metric("Population", int(df_selected["population"].values[0]))

# Plot top 10 countries by total cases
st.subheader("🌍 Top 10 Countries by Total Cases")
df_top10 = df_covid.sort_values(by="cases", ascending=False).head(10)
st.bar_chart(df_top10.set_index("country")["cases"])

conn.close()



