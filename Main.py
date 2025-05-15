import streamlit as st
import pandas as pd
import altair as alt
import openpyxl

st.set_page_config(page_title="Combined Gamma View", page_icon="📊", layout="wide")

# Custom sidebar background color (soft green)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #343c47;
            color: #fcfcfe;
        }
        [data-testid="stSidebar"] * {
            color: #fcfcfe !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
SPYWallsDFrm = pd.read_excel('SpyGammaAppData.xlsx', sheet_name='SPY Walls').tail(50)

# Format date column
SPYWallsDFrm["Date (0DTE)"] = pd.to_datetime(SPYWallsDFrm["Date (0DTE)"])

# -------- CW1, PW1, KGS1 Line Chart --------
df_price_levels = SPYWallsDFrm[["Date (0DTE)", "CW1", "PW1", "KGS1"]].rename(columns={"Date (0DTE)": "Date"})
df_price_levels_melted = df_price_levels.melt(id_vars=["Date"], var_name="Metric", value_name="SPY Level")

chart_price_levels = alt.Chart(df_price_levels_melted).mark_line().encode(
    x=alt.X('Date:T', title='Date'),
    y=alt.Y('SPY Level:Q', title='SPY Level', scale=alt.Scale(domain=[df_price_levels_melted['SPY Level'].min(), df_price_levels_melted['SPY Level'].max()])),
    color=alt.Color('Metric:N', legend=alt.Legend(title="Gamma Markers"))
).properties(title="CW1, PW1, and KGS1 Levels", height=400)

# -------- Net Change in Call and Put OI --------
df_oi_change = SPYWallsDFrm[["Date (0DTE)", "Net Change in Call OI", "Net Change in Put OI"]].rename(columns={"Date (0DTE)": "Date"})
df_oi_melted = df_oi_change.melt(id_vars=["Date"], var_name="OI Type", value_name="OI Change")

chart_oi_change = alt.Chart(df_oi_melted).mark_bar(opacity=0.6).encode(
    x=alt.X('Date:T'),
    y=alt.Y('OI Change:Q'),
    color=alt.Color('OI Type:N', legend=alt.Legend(title="OI Net Change"))
).properties(title="Net Change in Call and Put OI", height=400)

# -------- Gamma Tilt --------
chart_gamma_tilt = alt.Chart(SPYWallsDFrm).mark_line(color='purple').encode(
    x=alt.X('Date (0DTE):T'),
    y=alt.Y('Gamma Tilt:Q'),
).properties(title="Gamma Tilt", height=400)

# -------- Total Call/Put/Net Gamma --------
df_total_gamma = SPYWallsDFrm[["Date (0DTE)", "Total Call Gamma", "Total Put Gamma", "Total Net Gamma"]].rename(columns={"Date (0DTE)": "Date"})
df_gamma_melted = df_total_gamma.melt(id_vars=["Date"], var_name="Gamma Type", value_name="Gamma Value")

chart_total_gamma = alt.Chart(df_gamma_melted).mark_line().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Gamma Value:Q'),
    color=alt.Color('Gamma Type:N', legend=alt.Legend(title="Gamma Components"))
).properties(title="Total Call, Put, and Net Gamma", height=400)

# -------- Layout (1 chart per row) --------
st.title("📊 SPY Combined Gamma Overview")

st.altair_chart(chart_price_levels, use_container_width=True)
st.altair_chart(chart_oi_change, use_container_width=True)
st.altair_chart(chart_gamma_tilt, use_container_width=True)
st.altair_chart(chart_total_gamma, use_container_width=True)