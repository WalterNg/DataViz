import streamlit as st
import numpy as np 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

import streamlit as st

# SET PAGE CONFIG
st.set_page_config(page_title="Data Visualization",layout='wide')

# ADJUST SIZE OF EXPANDER
st.markdown(
    """
<style>
.streamlit-expanderHeader {
    font-size: 120%;
    font-weight: bold;
</style>
""",
    unsafe_allow_html=True,
)

# ADJUST FONT OF TABS HEADER
font_css = """
<style>
button[data-baseweb="tab"] {
  font-size: 19px;
  font-weight: bold;
}
</style>
"""
st.write(font_css, unsafe_allow_html=True)

# HIDE FOOT NOTE
hide_menu_style="""
        <style>
        footer{visibility:hidden;}
        </style>
        """
st.markdown(hide_menu_style,unsafe_allow_html=True)

st.title("Welcome to My Customized Interactive Data Visualization")
