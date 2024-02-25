from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd

def show_interactive_page():
    # Page Title
    st.title(":bar_chart: DataViz Interactive")

    # Uploading files
    file_uploaded = st.file_uploader("Upload your dataset")
    if file_uploaded:
        data = pd.read_csv(file_uploaded)
        st.write(data)
        columns = data.columns

        continous_var_list = data.describe().columns.tolist()
        categorical_var_list = data.columns.difference(continous_var_list).tolist()

        # Side bar 
        st.sidebar.header("Choose types of variables")
        continous_var = st.sidebar.multiselect("Please classify which is your continous variable",
                                        options=columns,
                                        default=continous_var_list
                                        )

        categorical_var = st.sidebar.multiselect("Please classify which is your categorical variable",
                                        options=columns,
                                        default=categorical_var_list
                                        )

        # Choose plot type
        graph_list = ['Scatter plot', "Line chart", "Bar chart", "Pie chart", "Boxplot", "Bubble chart", "Histogram"]
        graph_list.sort(reverse=False)

        user_graphs = st.multiselect("What do you want to plot?", graph_list)

        # Plotting section

        # Importing some plot functions from plot
        # from plot1 import all

        # for graph in user_graphs:
        #     if graph == "Scatter plot":
                

