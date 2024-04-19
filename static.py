import os
import json

import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
from utils.converter import convert2datetime
from section import static_page
from utils.users import get_user_dataset
from plots import ScatterPlot
from dataset import Dataset
from option_list.chart_types import chart_type_list


def show_static_page():
    '''
    This is the whole static visualization page
    '''
    # Page Title
    static_page.static_page_title()
    
    # Uploading files
    file_uploaded = st.file_uploader("Upload your dataset")

    if file_uploaded:

        data = get_user_dataset(file_uploaded)
        st.write(data)
        dataset = Dataset(data)
        dataset.organize()
        dataset.summary()
        variable_container = dataset.variable_container
        
        st.markdown("### Choose your plot")
        user_graphs = st.multiselect(
            "What do you want to plot?", 
            chart_type_list
            )
        for graph in user_graphs:
            if graph == 'Scatter plot':
                scatter_plot = ScatterPlot(data)
                scatter_plot.set_axis(variable_container)
                scatter_plot.set_style(variable_container)
                scatter_plot.set_advanced(variable_container)
                scatter_plot.plot()