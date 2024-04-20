import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
from utils.converter import convert2datetime
from section import static_page
from utils.users import get_user_dataset, get_user_chart
from utils.function import split_tabs
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
        
        user_charts = get_user_chart(chart_type_list)

        for chart in user_charts:
            if chart == 'Scatter plot':
                scatter_plot = ScatterPlot(data)
                col1, col2, tabs = split_tabs()

                with col2:
                    with tabs[0]:
                        scatter_plot.set_axis(variable_container)
                    with tabs[1]:
                        scatter_plot.set_style(variable_container)
                    with tabs[2]:
                        scatter_plot.set_advanced(variable_container)
                    with tabs[3]:
                        scatter_plot.set_figure(scatter_plot.name)
                with col1:
                    scatter_plot.plot()