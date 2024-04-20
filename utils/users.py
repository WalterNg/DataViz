import streamlit as st
import pandas as pd
from utils.checker import is_csv, is_excel

def get_user_chart(list_of_graph):
    user_chart = st.multiselect("Choose your plot:", list_of_graph)
    return user_chart

def get_user_dataset(filename):
    filename_extension = filename.type
    data = None

    if is_csv(filename_extension):
        data = pd.read_csv(filename)
    elif is_excel(filename_extension):
        data = pd.read_excel(filename)
    else:
        raise ValueError("This file is not supported")

    return data
