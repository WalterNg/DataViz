import streamlit as st
import numpy as np 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# SET PAGE CONFIG
st.set_page_config(page_title="Data Visualization",layout='wide')
st.sidebar.write("")

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

# HIDE FOOT NOTE
hide_menu_style="""
        <style>
        footer{visibility:hidden;}
        </style>
        """
st.markdown(hide_menu_style,unsafe_allow_html=True)

# Navigation bar
navigation = option_menu(
    menu_title=None,
    options=['Interactive', 'Static'],
    icons=["hand-index-thumb", "image"],
    default_index=0,
    orientation='horizontal',
    key="main_page_key"
)

# Import interactive and static module
from interactive import show_interactive_page
from test import show_static_page

# Page Title
if navigation == 'Interactive':
    show_interactive_page()
elif navigation == "Static":
    show_static_page()
