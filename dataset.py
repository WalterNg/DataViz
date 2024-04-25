import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from utils.converter import convert2datetime

class Dataset:
    def __init__(self, data: pd.DataFrame) -> None:
       
        self.columns =  data.columns.tolist()
        self.data = data
        
        self.variable_container = {}

    def organize(self):
        '''
        Organize different types of variables in the data
        '''
        self.continuous_var_list = []
        self.categorical_countable_list = []
        self.categorical_uncountable_list = []

        # Define types of variable
        self.numeric_var_list = self.data.describe().columns.tolist()
        self.categorical_var_list = self.data.columns.difference(self.numeric_var_list).tolist()
        self.datetime_list = [col for col in self.columns if self.data[col].dtype == '<M8[ns]']
        COUNTABLE_THRESHOLD = st.sidebar.slider(
            "Countable threshold:", min_value=1, max_value=30, value=10, 
            key="count_threshold", 
            help="By default, countable means less than or equal 10. You can adjust it properly (min is 1 and max is 30)")
    
        for var in self.numeric_var_list:
            if len(self.data[var].unique()) <= COUNTABLE_THRESHOLD: 
                self.categorical_countable_list.append(var)
            else:
                self.continuous_var_list.append(var)

        for var in self.categorical_var_list:
            if len(self.data[var].unique()) <= COUNTABLE_THRESHOLD:
                self.categorical_countable_list.append(var)
            else:
                self.categorical_uncountable_list.append(var)

        self.continuous_var = st.sidebar.multiselect("Continuous variables",
                                                    options=self.columns,
                                                    default=self.continuous_var_list)

        self.categorical_countable_var = st.sidebar.multiselect("Categorical and countable variables",
                                                    options=self.columns,
                                                    default=self.categorical_countable_list)
                                            
        self.categorical_uncountable_var = st.sidebar.multiselect("Categorical and uncountable variables",
                                                    options=self.columns,
                                                    default=self.categorical_uncountable_list)

        self.datetime_var = st.sidebar.multiselect("Datetime objects",
                                                    options=self.columns, default=self.datetime_list,
                                                    help='''Variables in this box will be converted into datetime object.
                                                    It's not always gonna work because date time objects are various, so make sure what you're doing!
                                                    ''')
        self.data, error_date =  convert2datetime(self.data, self.datetime_var)
    
        if error_date:
            st.sidebar.error(error_date)
        self.continuous_categorical_countable_var = list(set(self.continuous_var + self.categorical_countable_var))
    
        # Create a dict to store different variable
        self.variable_container['numeric_var'] = self.numeric_var_list
        self.variable_container['continuous_var'] = self.continuous_var
        self.variable_container['categorical_countable_var'] = self.categorical_countable_var
        self.variable_container['categorical_uncountable_var'] = self.categorical_uncountable_var
        self.variable_container['datetime_var'] = self.datetime_var
        self.variable_container['continuous_categorical_countable_var'] = self.continuous_categorical_countable_var



    def summary(self):
        self.col_types = [self.data[col].dtype.name for col in self.columns]
        with st.expander("General Information"):
            nrow, ncol = self.data.shape
            st.write(f"Data shape:  ({nrow},{ncol})")
            st.markdown("**Number of NA**")
            summary_dict = {'Columns': self.columns, "Data types": self.col_types,"NA's": self.data.isna().sum().values}
            summary = pd.DataFrame(summary_dict)
            st.dataframe(summary)

        with st.expander("Don't know what to plot? See here"):
            image_path = "assets\charts_options.jpeg"
            image = Image.open(image_path)
            st.image(image)

    def set_figure(self, name):

        # Figure size
        figure_width = st.number_input(
            "Figure's Width:", 
            min_value=1.0, max_value=20.0, 
            value=6.0, step=1.0, 
            key='fig_width_' + name, 
            help='Default is 6')
        
        figure_height = st.number_input(
            "Figure's Height:", 
            min_value=1.0, max_value=20.0, 
            value=5.0, step=1.0,
            key='fig_height_' + name, 
            help="Default is 5")
        
        self.figsize = (figure_width, figure_height)

        # Style and resolution of figure
        self.dpi = st.number_input(
            "Dots per inch (DPI):", 
            min_value=100, max_value=300, 
            value=100, step=50, 
            key="dpi_" + name,
            help="Default is 100")
        
        self.theme = st.selectbox(
            "Select theme:", 
            ['white','whitegrid','dark','darkgrid'], 
            key="theme_" + name)

        # Legend location
        self.bbox_to_anchor = None
        legend_loc_list = ['You choose','best','center','upper left', 'upper right', 'lower left', 'lower right','upper center', 'lower center', 'center left', 'center right']

        self.legend_loc = st.selectbox(
                "Legend locate:", 
                options=legend_loc_list, 
                index=1, 
                key="legend_loc_" + name, 
                help="You can locate legend using coordinate")
        if self.legend_loc == 'You choose':
            legend_loc_x = st.number_input(
                "x coordinate of legend:", 
                min_value=0.0, max_value=2.0, 
                value=1.0, step=0.1, 
                key="legend_x_" + name,
                help="x coordinate of legend")
            legend_loc_y = st.number_input(
                "y coordinate of legend:", 
                min_value=0.0, max_value=2.0, 
                value=1.0, step=0.1,
                key="legend_y_" + name,
                help="y coordinate of legend") 
            
            self.legend_loc = None
            self.bbox_to_anchor = (legend_loc_x,legend_loc_y)

        self.rotation_x = st.number_input(
            'x-ticks rotation:', 
            min_value=-90, max_value=90, 
            value=0, step=5, 
            key='rotation_x_' + name,
            help="Vary from -90 degree to 90 degree")
        
        self.rotation_y = st.number_input(
            'y-ticks rotation:', 
            min_value=-90, max_value=90, 
            value=0, step=5, 
            key='rotation_y_' + name,
            help="Vary from -90 degree to 90 degree")
        
        self.xbins = st.selectbox(
            "Number of bins on x-axis:", 
            ['auto','You choose'], 
            key='xbins_' + name, 
            help="How many values you want to display on x-axis")
        
        if self.xbins == 'You choose':
            self.xbins = st.number_input(
                "Number of bins on x-axis:", 
                min_value=0, max_value=30, 
                value=10, step=1, 
                key="xbins_num_" + name,
                help="Only work if x axis is continuous")
        
        self.ybins = st.selectbox(
            "Number of bins on y-axis:", 
            ['auto','You choose'], 
            key='ybins_' + name, 
            help="How many values you want to display on y-axis")
        
        if self.ybins == 'You choose':
            self.ybins = st.number_input(
                "Number of bins on y-axis:", 
                min_value=0, max_value=30, 
                value=10, step=1, 
                key="ybins_num_" + name, 
                help="Only work if y axis is continuous")

    def figure_setting(self, xlabel=None, ylabel=None, title=None):
        plt.legend(loc=self.legend_loc, bbox_to_anchor=self.bbox_to_anchor)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=self.rotation_x)
        plt.yticks(rotation=self.rotation_y)
        if self.xbins != 'auto':
            plt.locator_params(axis='x', nbins=self.xbins, tight=True)
        if self.ybins != 'auto':
            plt.locator_params(axis='y', nbins=self.ybins, tight=True)    