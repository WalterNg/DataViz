import streamlit as st


def split_tabs():
    lstTabs = ['Setup',"Style","Advanced","Figure Setting"]
    whitespace = 6

    col1, col2 = st.columns([1.5,1], gap='medium')
    tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])

    return col1, col2, tabs

def add_lineplot():
    return