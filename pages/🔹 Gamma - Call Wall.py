import streamlit as st
import pandas as pd
import altair as alt
import openpyxl 

st.set_page_config(page_icon=":guardsman:", layout="wide")

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

# Import data
SPYWallsDFrm = pd.read_excel('SpyGammaAppData.xlsx', sheet_name='SPY Walls').tail(50)

# -------- MainPage --------
Call_Wall_1 = SPYWallsDFrm["CW1"].tail(1).values[0]
Prior_Call_Wall_1 = SPYWallsDFrm["CW1"].tail(2).values[0]
Difference_Call_Wall_1 = Call_Wall_1 - Prior_Call_Wall_1

CW1_Net_Gamma = SPYWallsDFrm["CW Gamma (Net) CW1"].tail(1).values[0]
Prior_CW1_Net_Gamma = SPYWallsDFrm["CW Gamma (Net) CW1"].tail(2).values[0]
Difference_CW1_Net_Gamma = CW1_Net_Gamma - Prior_CW1_Net_Gamma

CW1_Call_OI_Change = SPYWallsDFrm["Call OI Change CW1"].tail(1).values[0]
Prior_CW1_Call_OI_Change = SPYWallsDFrm["Call OI Change CW1"].tail(2).values[0]

CW1_Put_OI_Change = SPYWallsDFrm["Put OI Change CW1"].tail(1).values[0]
Prior_CW1_Put_OI_Change = SPYWallsDFrm["Put OI Change CW1"].tail(2).values[0]

left_col, left_col2, right_col, right_col2 = st.columns(4)

# Display metric cards
left_col.metric(label="SPY Call Wall", value=Call_Wall_1, delta=f"{Difference_Call_Wall_1}")
left_col2.metric(label="Net Gamma", value=f"{int(CW1_Net_Gamma):,}", delta=f"{int(Difference_CW1_Net_Gamma):,}")
right_col.metric(label="Call OI Change", value=f"{int(CW1_Call_OI_Change):,}", delta=f"{int(Prior_CW1_Call_OI_Change):,}")
right_col2.metric(label="Put OI Change", value=f"{int(CW1_Put_OI_Change):,}", delta=f"{int(Prior_CW1_Put_OI_Change):,}")

# Slim down the DataFrame to 5 relevant columns
slim_df_cw1 = SPYWallsDFrm[["Date (0DTE)", "CW1"]].copy()
slim_df_cw1["Date (0DTE)"] = slim_df_cw1["Date (0DTE)"].dt.strftime('%m-%d-%Y')

# -------- CANDLESTICK --------
# Build daily OHLC + SDs DataFrame
DailyPriceData = pd.DataFrame({
    'datetime': pd.to_datetime(SPYWallsDFrm["Date (0DTE)"]),
    'open': SPYWallsDFrm["SPY OPEN"],
    'high': SPYWallsDFrm["SPY HIGH"],
    'low': SPYWallsDFrm["SPY LOW"],
    'close': SPYWallsDFrm["SPY CLOSE"],
    'SDs': SPYWallsDFrm["SDs"]
})
DailyPriceData['color'] = DailyPriceData['close'] > DailyPriceData['open']

# Dynamic y-axis for price
min_price = DailyPriceData['low'].min() * 0.98
max_price = DailyPriceData['high'].max() * 1.02

# Base chart
base = alt.Chart(DailyPriceData).encode(
    x=alt.X('datetime:T', axis=alt.Axis(format='%B %d', title='Date'))
)

# Wick lines
rule = base.mark_rule().encode(
    y=alt.Y('low:Q', scale=alt.Scale(domain=[min_price, max_price]), title='Price'),
    y2='high:Q',
    color=alt.condition('datum.color', alt.value('green'), alt.value('red'))
)

# Candle bodies
bars = base.mark_bar(size=6).encode(
    y=alt.Y('open:Q', scale=alt.Scale(domain=[min_price, max_price]), title='Price'),
    y2='close:Q',
    color=alt.condition('datum.open <= datum.close', alt.value('green'), alt.value('red'))
)

# Volume bars (SDs)
volume = base.mark_bar(opacity=0.25, color='orange').encode(
    y=alt.Y('SDs:Q', axis=alt.Axis(title='SDs'))
)

# Final chart without hover
candlestick_chart = alt.layer(volume, rule, bars).resolve_scale(
    y='independent'
).properties(
    width=900,
    height=400
)

# -------- Call Wall Line Chart --------
dfCW1 = pd.DataFrame({
    "Date": SPYWallsDFrm["Date (0DTE)"],
    "Call Wall": SPYWallsDFrm["CW1"],
    "Call Gamma Notional": SPYWallsDFrm["CW Gamma (Net) CW1"],
    "Call OI Change": SPYWallsDFrm["Call OI Change CW1"],
    "Put OI Change": SPYWallsDFrm["Put OI Change CW1"],
    "Average Call Gamma Duration": SPYWallsDFrm["Ave Length CW1"]
})

dfCW1_melted = dfCW1.melt(id_vars=["Date"], value_vars=["Call Wall"], var_name="Metric", value_name="SPY Level")

cw1_lines = alt.Chart(dfCW1_melted).mark_line().encode(
    x='Date',
    y=alt.Y('SPY Level', scale=alt.Scale(domain=[dfCW1_melted['SPY Level'].min(), dfCW1_melted['SPY Level'].max()])),
    color=alt.Color('Metric:N', legend=None)
).properties(width=600, height=400)

# Layout: Left column for DataFrame, Right for charts
left_col, right_col = st.columns([1, 4])

with left_col:
    st.dataframe(slim_df_cw1, use_container_width=True, height=800)

with right_col:
    st.altair_chart(cw1_lines, use_container_width=True)
    st.altair_chart(candlestick_chart, use_container_width=True)

# -------- Bar Charts --------
df_OI_Change_CW1_melted = dfCW1.melt(id_vars=["Date"], value_vars=["Call OI Change", "Put OI Change"], var_name="OI_Metric", value_name="OI Change")

cw1_bars = alt.Chart(df_OI_Change_CW1_melted).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('OI Change', scale=alt.Scale(domain=[df_OI_Change_CW1_melted['OI Change'].min(), df_OI_Change_CW1_melted['OI Change'].max()])),
    color=alt.Color('OI_Metric:N', legend=None)
).properties(width=600, height=400)

df_CW1_Net_Gamma = dfCW1.melt(id_vars=["Date"], value_vars=["Call Gamma Notional"], var_name="Net_Gamma_Metric", value_name="Call Wall Net Gamma")

cw1_gamma_notional_bars = alt.Chart(df_CW1_Net_Gamma).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('Call Wall Net Gamma', scale=alt.Scale(domain=[df_CW1_Net_Gamma['Call Wall Net Gamma'].min(), df_CW1_Net_Gamma['Call Wall Net Gamma'].max()])),
    color=alt.Color('Net_Gamma_Metric:N', legend=None)
).properties(width=600, height=400)

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(cw1_bars, use_container_width=True)

with col2:
    st.altair_chart(cw1_gamma_notional_bars, use_container_width=True)


# -------- Duration Charts --------
df_Duration_CW1_melted = dfCW1.melt(id_vars=["Date"], value_vars=["Average Call Gamma Duration"], var_name="Duration_Metric", value_name="Duration")

cw1_bars_duration = alt.Chart(df_Duration_CW1_melted).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('Duration', scale=alt.Scale(domain=[df_Duration_CW1_melted['Duration'].min(), df_Duration_CW1_melted['Duration'].max()])),
    color=alt.Color('Duration_Metric:N', legend=None)
).properties(width=600, height=400)

st.altair_chart(cw1_bars_duration, use_container_width=True)