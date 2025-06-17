import streamlit as st
from utils.disease_data import load_historical_data, get_available_diseases
import plotly.express as px

st.title("🦠 Disease Insights – Real-time + Historical")

disease_input = st.text_input("🔍 Enter Disease Name", placeholder="e.g. Malaria")

if disease_input:
    hist_data = load_historical_data(disease_input)

    if hist_data.empty:
        st.warning(f"No historical data found for '{disease_input}'")
    else:
        st.success(f"Showing data for: {disease_input.title()}")

        st.subheader("📊 Historical Trends (Last 50 Years)")
        fig = px.line(hist_data, x="Year", y="Cases", title="Cases Over Time", markers=True)
        st.plotly_chart(fig)

        st.dataframe(hist_data)

        # Optionally show deaths too
        fig2 = px.line(hist_data, x="Year", y="Deaths", title="Deaths Over Time", markers=True, color_discrete_sequence=["red"])
        st.plotly_chart(fig2)
