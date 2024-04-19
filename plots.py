import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image
from dataset import Dataset

from option_list.palette_list import palette_list

class ScatterPlot(Dataset):
    def __init__(self, data, name='scatter') -> None:
        super().__init__(data)
        self.name = name
        self.data = data

    def set_axis(self, variable_container):
        self.x = st.selectbox("Choose x-axis:", list([None] + self.columns), key="x_" + self.name, help="Can be any value")
        self.y = st.selectbox("Choose y-axis:", list([None] + self.columns), key="y_" + self.name, help="Can be any value")
        self.xlabel = st.text_input("x-label:", self.x, key="xlabel_" + self.name, help='Can be self-defined')
        self.ylabel = st.text_input("y-label:", self.y, key="ylabel_" + self.name, help='Can be self-defined')
        self.title = st.text_input("Title:", key='title_' + self.name, help='Can be self-defined')


    def set_style(self, variable_container): 

        continuous_categorical_countable_var = variable_container['continuous_categorical_countable_var']

        self.hue = st.selectbox(
            label="Hue:", 
            options=list([None] + continuous_categorical_countable_var), 
            key="hue_" + self.name,
            help="Accept any except categorical and uncountable variables")
        
        palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette" + self.name,
            help="Select set of colors you want to display")
        
        size = st.selectbox(
            "Size:", 
            options=list([None] + continuous_categorical_countable_var),
            key="size_" + self.name,
            help="Accept any except categorical and uncountable variables")
        
        style = st.selectbox(
            "Style:", 
            options=list([None] + continuous_categorical_countable_var), 
            key="style_" + self.name,
            help="Accept only categorical and countable variables")
        
    
    def set_advanced(self, variable_container):
        
        alpha = st.number_input(
            "Opacity:", 
            min_value=0.0, 
            max_value=1.0, 
            value=1.0, 
            step=0.1, 
            key="alpha_" + self.name,
            help="Default opacity is 1")
        
        sizes = None
        sizes_select = st.selectbox(
            "Range of sizes:", 
            options=['auto', 'You choose'], 
            key='sizes_select_' + self.name, 
            help='Range of sizes when size is used') 
        
        if sizes_select == 'You choose':
            sizes_lower = st.number_input(
                "Select lower limit of sizes:", 
                min_value=10, 
                max_value=200, 
                value=10, 
                step=10,
                key='sizes_lower_' + self.name, 
                help='Min is 10 and max is 200')
            
            sizes_upper = st.number_input(
                "Select upper limit of sizes:", 
                min_value=10, 
                max_value=200, 
                value=60, 
                step=10,
                key='sizes_upper_' + self.name, 
                help='Min is 10 and max is 200')
            
            sizes = (sizes_lower, sizes_upper)

        return alpha, sizes
    
    def plot(self):
        fig = plt.figure()
        ax = sns.scatterplot(data=self.data, x=self.x, y=self.y, hue=self.hue)
        if self.x is None or self.y is None:
            st.info('Please enter x and y axes !')
        else:
            st.pyplot(fig)