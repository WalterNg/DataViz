import streamlit as st
import numpy as np

def split_tabs():
    lstTabs = ['Setup',"Style","Advanced","Figure Setting"]
    whitespace = 6

    col1, col2 = st.columns([1.5,1], gap='medium')
    tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])

    return col1, col2, tabs

def compute_freq(x_unique: np.array):
    '''
    Return a dictionary of key and frequency of occurrence of that key.
    Args:
        x_unique: must be a list of countable variables
    '''
    x_unique = list(x_unique.astype(str))
    x_freq = {key: x_unique.count(key) for key in x_unique}
    return x_freq