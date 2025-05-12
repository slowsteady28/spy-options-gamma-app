import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="SPY Gamma App", page_icon=":guardsman:", layout="wide")

# Import data
SPYWallsDFrm = pd.read_excel('SpyGammaAppData.xlsx', sheet_name='SPY Walls').tail(50)

# -------- MainPage --------
st.subheader(":bar_chart: SPY Key Gamma Strike")

KGS = SPYWallsDFrm["KGS1"].tail(1).values[0]
Prior_KGS = SPYWallsDFrm["KGS1"].tail(2).values[0]
Difference_KGS = KGS - Prior_KGS

KGS_Net_Gamma = SPYWallsDFrm["KGS Gamma KG1"].tail(1).values[0]
Prior_KGS_Net_Gamma = SPYWallsDFrm["KGS Gamma KG1"].tail(2).values[0]
Difference_KGS_Net_Gamma = KGS_Net_Gamma - Prior_KGS_Net_Gamma

KGS_Call_OI_Change = SPYWallsDFrm["Call OI Change KG1"].tail(1).values[0]
Prior_KGS_Call_OI_Change = SPYWallsDFrm["Call OI Change KG1"].tail(2).values[0]

KGS_Put_OI_Change = SPYWallsDFrm["Put OI Change KG1"].tail(1).values[0]
Prior_KGS_Put_OI_Change = SPYWallsDFrm["Put OI Change KG1"].tail(2).values[0]

left_col, left_col2, right_col, right_col2 = st.columns(4)

# Display metric cards
left_col.metric(label="KGS1", value=KGS, delta=f"{Difference_KGS}")
left_col2.metric(label="Net Gamma", value=f"{int(KGS_Net_Gamma):,}", delta=f"{int(Difference_KGS_Net_Gamma):,}")
right_col.metric(label="Call OI Change", value=f"{int(KGS_Call_OI_Change):,}", delta=f"{int(Prior_KGS_Call_OI_Change):,}")
right_col2.metric(label="Put OI Change", value=f"{int(KGS_Put_OI_Change):,}", delta=f"{int(Prior_KGS_Put_OI_Change):,}")

# Slim down the DataFrame
slim_df_kgs = SPYWallsDFrm[["Date (0DTE)", "KGS1"]].copy()
slim_df_kgs["Date (0DTE)"] = slim_df_kgs["Date (0DTE)"].dt.strftime('%m-%d-%Y')

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

# -------- Key Gamma Line Chart --------
dfKGS = pd.DataFrame({
    "Date": SPYWallsDFrm["Date (0DTE)"],
    "Key Gamma Strike": SPYWallsDFrm["KGS1"],
    "Key Gamma Notional": SPYWallsDFrm["KGS Gamma KG1"],
    "Call OI Change": SPYWallsDFrm["Call OI Change KG1"],
    "Put OI Change": SPYWallsDFrm["Put OI Change KG1"],
    "Average Duration - Calls": SPYWallsDFrm["Ave Length (Call) KG1"],
    "Average Duration - Puts": SPYWallsDFrm["Ave Length (Put) KG1"]
})

dfKGS_melted = dfKGS.melt(id_vars=["Date"], value_vars=["Key Gamma Strike"], var_name="Metric", value_name="SPY Level")

kgs_lines = alt.Chart(dfKGS_melted).mark_line().encode(
    x='Date',
    y=alt.Y('SPY Level', scale=alt.Scale(domain=[dfKGS_melted['SPY Level'].min(), dfKGS_melted['SPY Level'].max()])),
    color=alt.Color('Metric:N', legend=None)
).properties(width=600, height=400)

left_col, right_col = st.columns([1, 4])

with left_col:
    st.dataframe(slim_df_kgs, use_container_width=True, height=800)

with right_col:
    st.altair_chart(kgs_lines, use_container_width=True)
    st.altair_chart(candlestick_chart, use_container_width=True)

# -------- Bar Charts --------
df_OI_Change_KGS_melted = dfKGS.melt(id_vars=["Date"], value_vars=["Call OI Change", "Put OI Change"], var_name="OI_Metric", value_name="OI Change")

kgs_bars = alt.Chart(df_OI_Change_KGS_melted).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('OI Change', scale=alt.Scale(domain=[df_OI_Change_KGS_melted['OI Change'].min(), df_OI_Change_KGS_melted['OI Change'].max()])),
    color=alt.Color('OI_Metric:N', legend=None)
).properties(width=600, height=400)

df_KGS_Net_Gamma = dfKGS.melt(id_vars=["Date"], value_vars=["Key Gamma Notional"], var_name="Net_Gamma_Metric", value_name="KGS Gamma KG1")

kgs_gamma_notional_bars = alt.Chart(df_KGS_Net_Gamma).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('KGS Gamma KG1', scale=alt.Scale(domain=[df_KGS_Net_Gamma['KGS Gamma KG1'].min(), df_KGS_Net_Gamma['KGS Gamma KG1'].max()])),
    color=alt.Color('Net_Gamma_Metric:N', legend=None)
).properties(width=600, height=400)

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(kgs_bars, use_container_width=True)

with col2:
    st.altair_chart(kgs_gamma_notional_bars, use_container_width=True)

    print(dfKGS)

# -------- Duration Charts --------
df_Duration_KG1_melted = dfKGS.melt(id_vars=["Date"], value_vars=["Average Duration - Calls", "Average Duration - Puts"], var_name="Duration_Metric", value_name="Duration")

kg1_bars_duration = alt.Chart(df_Duration_KG1_melted).mark_bar(opacity=0.4).encode(
    x='Date',
    y=alt.Y('Duration', scale=alt.Scale(domain=[df_Duration_KG1_melted['Duration'].min(), df_Duration_KG1_melted['Duration'].max()])),
    color=alt.Color('Duration_Metric:N', legend=None)
).properties(width=600, height=400)

st.altair_chart(kg1_bars_duration, use_container_width=True)