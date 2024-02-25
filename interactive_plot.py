import streamlit as st
import numpy as np 
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def plot_line_chart(data,x,y, color=None):
    data_temp = data.copy()
    data_temp = data.sort_values(by=x)
    line_chart = px.line(data_temp, x=x, y=y, color=color)
    st.plotly_chart(line_chart)

def plot_scatter(data, x, y, color=None):
    st.plotly_chart(px.scatter(data,x,y, color=color))

def plot_bar_chart(data, x, y):
    st.plotly_chart(px.bar(data, x=x, y=y))

def plot_histogram(data,x, nbins):
    st.plotly_chart(px.histogram(data, x=x, nbins=nbins))

