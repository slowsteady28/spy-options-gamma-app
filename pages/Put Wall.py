import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="SPY Gamma App", page_icon=":guardsman:", layout="wide")

# Import data
SPYWallsDFrm = pd.read_excel('SpyGammaAppData.xlsx', sheet_name='SPY Walls').tail(50)

# -------- MainPage --------
st.subheader(":bar_chart: SPY Put Wall")

Put_Wall_1 = SPYWallsDFrm["PW1"].tail(1).values[0]
Prior_Put_Wall_1 = SPYWallsDFrm["PW1"].tail(2).values[0]
Difference_Put_Wall_1 = Put_Wall_1 - Prior_Put_Wall_1

PW1_Net_Gamma = SPYWallsDFrm["Put Wall Gamma (Net) PW1"].tail(1).values[0]
Prior_PW1_Net_Gamma = SPYWallsDFrm["Put Wall Gamma (Net) PW1"].tail(2).values[0]
Difference_PW1_Net_Gamma = PW1_Net_Gamma - Prior_PW1_Net_Gamma

PW1_Call_OI_Change = SPYWallsDFrm["Call OI Change PW1"].tail(1).values[0]
Prior_PW1_Call_OI_Change = SPYWallsDFrm["Call OI Change PW1"].tail(2).values[0]

PW1_Put_OI_Change = SPYWallsDFrm["Put OI Change PW1"].tail(1).values[0]
Prior_PW1_Put_OI_Change = SPYWallsDFrm["Put OI Change PW1"].tail(2).values[0]

left_col, left_col2, right_col, right_col2 = st.columns(4)

# Display metric cards
left_col.metric(label="SPY Put Wall", value=Put_Wall_1, delta=f"{Difference_Put_Wall_1}")
left_col2.metric(label="Net Gamma", value=f"{int(PW1_Net_Gamma):,}", delta=f"{int(Difference_PW1_Net_Gamma):,}")
right_col.metric(label="Call OI Change", value=f"{int(PW1_Call_OI_Change):,}", delta=f"{int(Prior_PW1_Call_OI_Change):,}")
right_col2.metric(label="Put OI Change", value=f"{int(PW1_Put_OI_Change):,}", delta=f"{int(Prior_PW1_Put_OI_Change):,}")

# Slim down the DataFrame to 5 relevant columns
slim_df_pw1 = SPYWallsDFrm[["Date (0DTE)", "PW1"]].copy()
slim_df_pw1["Date (0DTE)"] = slim_df_pw1["Date (0DTE)"].dt.strftime('%m-%d-%Y')

# -------- CANDLESTICK --------
DailyPriceData = pd.DataFrame({
    'datetime': pd.to_datetime(SPYWallsDFrm["Date (0DTE)"]),
    'open': SPYWallsDFrm["SPY OPEN"],
    'high': SPYWallsDFrm["SPY HIGH"],
    'low': SPYWallsDFrm["SPY LOW"],
    'close': SPYWallsDFrm["SPY CLOSE"],
    'SDs': SPYWallsDFrm["SDs"]
})
DailyPriceData['color'] = DailyPriceData['close'] > DailyPriceData['open']

min_price = DailyPriceData['low'].min() * 0.98
max_price = DailyPriceData['high'].max() * 1.02

base = alt.Chart(DailyPriceData).encode(
    x=alt.X('datetime:T', axis=alt.Axis(format='%B %d', title='Date'))
)

rule = base.mark_rule().encode(
    y=alt.Y('low:Q', scale=alt.Scale(domain=[min_price, max_price]), title='Price'),
    y2='high:Q',
    color=alt.condition('datum.color', alt.value('green'), alt.value('red'))
)

bars = base.mark_bar(size=6).encode(
    y=alt.Y('open:Q', scale=alt.Scale(domain=[min_price, max_price]), title='Price'),
    y2='close:Q',
    color=alt.condition('datum.open <= datum.close', alt.value('green'), alt.value('red'))
)

volume = base.mark_bar(opacity=0.25, color='orange').encode(
    y=alt.Y('SDs:Q', axis=alt.Axis(title='SDs'))
)

candlestick_chart = alt.layer(volume, rule, bars).resolve_scale(
    y='independent'
).properties(
    width=900,
    height=400
)

# -------- Put Wall Line Chart --------
dfPW1 = pd.DataFrame({
    "Date": SPYWallsDFrm["Date (0DTE)"],
    "Put Wall": SPYWallsDFrm["PW1"],
    "Put Gamma Notional": SPYWallsDFrm["Put Wall Gamma (Net) PW1"],
    "Call OI Change": SPYWallsDFrm["Call OI Change PW1"],
    "Put OI Change": SPYWallsDFrm["Put OI Change PW1"],
    "Average Put Gamma Duration": SPYWallsDFrm["Ave Length PW1"]
})

dfPW1_melted = dfPW1.melt(id_vars=["Date"], value_vars=["Put Wall"], var_name="Metric", value_name="SPY Level")

pw1_lines = alt.Chart(dfPW1_melted).mark_line().encode(
    x='Date',
    y=alt.Y('SPY Level', scale=alt.Scale(domain=[dfPW1_melted['SPY Level'].min(), dfPW1_melted['SPY Level'].max()])),
    color=alt.Color('Metric:N', legend=None)
).properties(width=600, height=400)

left_col, right_col = st.columns([1, 4])

with left_col:
    st.dataframe(slim_df_pw1, use_container_width=True, height=800)

with right_col:
    st.altair_chart(pw1_lines, use_container_width=True)
    st.altair_chart(candlestick_chart, use_container_width=True)

# -------- Bar Charts --------
df_OI_Change_PW1_melted = dfPW1.melt(id_vars=["Date"], value_vars=["Call OI Change", "Put OI Change"], var_name="OI_Metric", value_name="OI Change")

pw1_bars = alt.Chart(df_OI_Change_PW1_melted).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('OI Change', scale=alt.Scale(domain=[df_OI_Change_PW1_melted['OI Change'].min(), df_OI_Change_PW1_melted['OI Change'].max()])),
    color=alt.Color('OI_Metric:N', legend=None)
).properties(width=600, height=400)

df_PW1_Net_Gamma = dfPW1.melt(id_vars=["Date"], value_vars=["Put Gamma Notional"], var_name="Net_Gamma_Metric", value_name="Put Wall Net Gamma")

pw1_gamma_notional_bars = alt.Chart(df_PW1_Net_Gamma).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('Put Wall Net Gamma', scale=alt.Scale(domain=[df_PW1_Net_Gamma['Put Wall Net Gamma'].min(), df_PW1_Net_Gamma['Put Wall Net Gamma'].max()])),
    color=alt.Color('Net_Gamma_Metric:N', legend=None)
).properties(width=600, height=400)

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(pw1_bars, use_container_width=True)

with col2:
    st.altair_chart(pw1_gamma_notional_bars, use_container_width=True)

# -------- Put Charts --------
df_Duration_PW1_melted = dfPW1.melt(id_vars=["Date"], value_vars=["Average Put Gamma Duration"], var_name="Duration_Metric", value_name="Duration")

pw1_bars_duration = alt.Chart(df_Duration_PW1_melted).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('Duration', scale=alt.Scale(domain=[df_Duration_PW1_melted['Duration'].min(), df_Duration_PW1_melted['Duration'].max()])),
    color=alt.Color('Duration_Metric:N', legend=None)
).properties(width=600, height=400)

st.altair_chart(pw1_bars_duration, use_container_width=True)