import pandas as pd
import streamlit as st
from PIL import Image

class Dataset:
    def __init__(self, data: pd.DataFrame) -> None:
       
        self.columns =  data.columns.tolist()
        self.data = data
        self.col_types = [self.data[col].dtype.name for col in self.columns]
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
        self.continuous_categorical_countable_var = list(set(self.continuous_var + self.categorical_countable_var))
    
        self.variable_container['continuous_var'] = self.continuous_var
        self.variable_container['categorical_countable_var'] = self.categorical_countable_var
        self.variable_container['categorical_uncountable_var'] = self.categorical_uncountable_var
        self.variable_container['datetime_var'] = self.datetime_var
        self.variable_container['continuous_categorical_countable_var'] = self.continuous_categorical_countable_var


    def summary(self):
        with st.expander("General Information"):
            nrow, ncol = self.data.shape
            st.write(f"Data shape:  ({nrow},{ncol})")
            st.markdown("**Number of NA**")
            summary_dict = {'Columns': self.columns, "Data types": self.col_types,"NA's": self.data.isna().sum().values}
            summary = pd.DataFrame(summary_dict)
            st.write(summary)

        with st.expander("Don't know what to plot? See here"):
            image_path = "assets\charts_options.jpeg"
            image = Image.open(image_path)
            st.image(image)
