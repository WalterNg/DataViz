import streamlit as st
from section import static_page
from utils.users import get_user_dataset, get_user_chart
from utils.function import split_tabs
from plots import *
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
        st.dataframe(data)
        dataset = Dataset(data)
        dataset.organize()
        dataset.summary()
        variable_container = dataset.variable_container
        
        user_charts = get_user_chart(chart_type_list)

        for chart in user_charts:
            col1, col2, tabs = split_tabs()
            if chart == 'Scatter plot':
                scatter_plot = ScatterPlot(dataset.data)
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


            elif chart == 'Bar chart':
                bar_plot = BarPlot(dataset.data)
                with col2:
                    with tabs[0]:
                        bar_plot.set_axis(variable_container)
                    with tabs[1]:
                        bar_plot.set_style(variable_container)
                    with tabs[2]:
                        bar_plot.set_advanced(variable_container)
                    with tabs[3]:
                        bar_plot.set_figure(bar_plot.name)
                with col1:
                    bar_plot.plot()


            elif chart == 'Line chart':
                line_plot = LinePlot(dataset.data)
                with col2:
                    with tabs[0]:
                        line_plot.set_axis(variable_container)
                    with tabs[1]:
                        line_plot.set_style(variable_container)
                    with tabs[2]:
                        line_plot.set_advanced(variable_container)
                    with tabs[3]:
                        line_plot.set_figure(line_plot.name)
                with col1:
                    line_plot.plot()


            elif chart == 'Histogram':
                histogram = Histogram(dataset.data)
                with col2:
                    with tabs[0]:
                        histogram.set_axis(variable_container)
                    with tabs[1]:
                        histogram.set_style(variable_container)
                    with tabs[2]:
                        histogram.set_advanced(variable_container)
                    with tabs[3]:
                        histogram.set_figure(histogram.name)
                with col1:
                    histogram.plot()


            elif chart == 'Boxplot':
                boxplot = BoxPlot(dataset.data)
                with col2:
                    with tabs[0]:
                        boxplot.set_axis(variable_container)
                    with tabs[1]:
                        boxplot.set_style(variable_container)
                    with tabs[2]:
                        boxplot.set_advanced(variable_container)
                    with tabs[3]:
                        boxplot.set_figure(boxplot.name)
                with col1:
                    boxplot.plot()


            elif chart == 'Pie chart':
                pie_chart = PiePlot(dataset.data)
                with col2:
                    with tabs[0]:
                        pie_chart.set_axis(variable_container)
                    with tabs[1]:
                        pie_chart.set_style(variable_container)
                    with tabs[2]:
                        pie_chart.set_advanced(variable_container)
                    with tabs[3]:
                        pie_chart.set_figure(pie_chart.name)
                with col1:
                    pie_chart.plot()