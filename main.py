import streamlit as st
import numpy as np 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


st.title("Welcome to My Customized Interactive Data Visualization")

# Uploading files
file_uploaded = st.file_uploader("Upload your dataset")


if file_uploaded:
    data = pd.read_csv(file_uploaded)
    st.write(data)
    columns = data.columns

# List name of chart in right order
list_of_graph = ["Line Chart", "Boxplot", "Scatter Plot", "Pie Chart", "Bar Chart", "Histogram"]
list_of_graph.sort(reverse=False)


user_plot = st.multiselect("Choose your plot:", list_of_graph)
st.write(user_plot)


# Importing chart
from interactive_plot import plot_line_chart, plot_scatter, plot_bar_chart, plot_histogram
from function import add_plot

add_plot(user_chart=user_plot)


if "Line Chart" in user_plot:
    st.markdown("## Line Chart")
    with st.form("Line Chart form"):
        col1, col2 = st.columns(2)
        x_line = col1.selectbox("Choose x-axis:", columns, key="x_line")
        y_line = col2.selectbox("Choose y-axis:", columns, key="y_line")
        # color = st.selectbox("Color based on:", columns, key="color_line")
        # Let's design the sidebar for parameter selection
        submitted = st.form_submit_button()
        if submitted:
            plot_line_chart(data,x_line,y_line)

if "Scatter Plot" in user_plot:
    st.markdown("## Scatter Plot")
    col1, col2 = st.columns(2)
    x_scatter = col1.selectbox("Choose x-axis:", columns, key="x_scatter")
    y_scatter = col2.selectbox("Choose y-axis:", columns, key="y_scatter")

    plot_scatter(data,x_scatter,y_scatter)

if "Bar Chart" in user_plot:
    st.markdown("## Bar Chart")
    col1, col2 = st.columns(2)
    x_bar = col1.selectbox("Choose x-axis:", columns, key="x_bar")
    y_bar = col2.selectbox("Choose y-axis:", columns, key="y_bar")

    plot_bar_chart(data, x_bar, y_bar)

if "Histogram" in user_plot:
    st.markdown("## Histogram")
    col1, col2 = st.columns(2)
    x_hist = col1.selectbox("Choose x-axis:", columns, key="x_hist")
    nbins = st.number_input("Number of bins:", 5, len(data), step=5)
    # y_bar = col2.selectbox("Choose y-axis for histogram: ", columns)

    plot_histogram(data, x= x_hist, nbins=nbins)