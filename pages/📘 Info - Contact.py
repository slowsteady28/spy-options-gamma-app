import streamlit as st

st.set_page_config(page_title="About Me", page_icon="🧑‍💻")

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

st.title("About Me")

st.markdown("""
Hi, I'm **Eliezer Nunez** — an independent trader and data-driven market analyst with a focus on **SPY options gamma** and its impact on short-term price action.

Since 2019, I've been developing strategies rooted in market microstructure, gamma dynamics, and behavioral flow. My work blends **macro context**, **option positioning**, and **quant-driven insights** to understand where liquidity supports or pressures price.

This site provides ongoing commentary and analysis based on those models.

🔗 [Connect with me on LinkedIn](https://www.linkedin.com/in/eli-nunez)
""")