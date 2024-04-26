import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image
from dataset import Dataset

from utils.converter import convert2datetime
from utils.function import compute_freq
from option_list.palette_list import palette_list
from option_list.colors_list import color_list

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
        
        self.palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette" + self.name,
            help="Select set of colors you want to display")
        
        self.size = st.selectbox(
            "Size:", 
            options=list([None] + continuous_categorical_countable_var),
            key="size_" + self.name,
            help="Accept any except categorical and uncountable variables")
        
        self.style = st.selectbox(
            "Style:", 
            options=list([None] + continuous_categorical_countable_var), 
            key="style_" + self.name,
            help="Accept only categorical and countable variables")
        
    
    def set_advanced(self, variable_container):
        
        self.alpha = st.number_input(
            "Opacity:", 
            min_value=0.0, 
            max_value=1.0, 
            value=1.0, 
            step=0.1, 
            key="alpha_" + self.name,
            help="Default opacity is 1")
        
        self.sizes = None
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
            
            self.sizes = (sizes_lower, sizes_upper)

    def plot(self):
        sns.set_style(self.theme)
        fig = plt.figure(figsize=self.figsize)

        if self.x is None or self.y is None:
            st.info('Please enter x and y axes !')
        else:    
            ax = sns.scatterplot(
                data=self.data, 
                x=self.x, 
                y=self.y, 
                hue=self.hue,
                size=self.size, 
                style=self.style, 
                alpha=self.alpha)

            self.figure_setting(self.xlabel, self.ylabel, self.title)
            st.pyplot(fig)


class BarPlot(Dataset):
    def __init__(self, data, name='bar') -> None:
        super().__init__(data)
        self.name = name
        self.data = data
        
    def set_axis(self, variable_container):
        categorical_countable_var = variable_container['categorical_countable_var']
        numeric_var = variable_container['numeric_var']
        self.x = st.selectbox(
            "Choose x-axis:", 
            list([None] + categorical_countable_var), 
            key="x_" + self.name, 
            help='Only accept categorical and countable variables')
        
        self.y = st.selectbox(
            "Choose y-axis:", 
            list([None] + numeric_var), 
            key="y_" + self.name, 
            help='Only accept numerical variables')
        
        self.xlabel = st.text_input("x-label:", self.x, key="xlabel_" + self.name, help='Can be self-defined')
        self.ylabel = st.text_input("y-label:", self.y, key="ylabel_" + self.name, help='Can be self-defined')
        self.title = st.text_input("Title:", key='title_' + self.name, help='Can be self-defined')


    def set_style(self, variable_container): 

        categorical_countable_var = variable_container['categorical_countable_var']

        self.hue = st.selectbox(
            label="Hue:", 
            options=list([None] + categorical_countable_var), 
            key="hue_" + self.name,
            help="Accept only Categorical and countable variables")
        
        self.palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette_" + self.name,
            help="Select set of colors you want to display")
        
        self.fill = st.selectbox(
            'Use fill:',
            options=[True, False],
            key='fill_' + self.name,
            help='If True, use solid bar. If False, use line art.'
        )
        
        self.alpha = st.number_input(
            "Opacity:", 
            min_value=0.0, 
            max_value=1.0, 
            value=1.0, 
            step=0.1, 
            key="alpha_" + self.name,
            help="Default opacity is 1")
        
    def set_advanced(self, variable_container):
        self.estimator = st.selectbox(
            label='Estimator of y-axis',
            options=['mean', 'sum', 'length'],
            key='estimator_' + self.name,
            help='Select which function to aggregated.'
        )
        if self.estimator == 'mean':
            self.estimator = np.mean
        elif self.estimator == 'sum':
            self.estimator = np.sum
        elif self.estimator == 'length':
            self.estimator = len

        self.error_bar = st.selectbox(
            'Error bar method:',
            options=[None, 'sd', 'ci', 'se', 'pi'],
            key='error_bar_' + self.name,
            help='Name of error bar, most common used is sd and ci'
        )
        
        if self.x is not None:
            self.order = st.multiselect(
                'Select order of x-axis:',
                options=self.data[self.x].unique(),
                default=self.data[self.x].unique(),
                key='order_' + self.name,
                help='Provide the order and appearance of each bar'
            )
        else:
            self.order = st.multiselect(
                'Select order of x-axis:',
                options=[],
                default=None,
                key='order_' + self.name,
                help='Provide the order and appearance of each bar'
            )

    def plot(self):
        sns.set_style(self.theme)
        fig = plt.figure(figsize=self.figsize)

        if self.x is None or self.y is None:
            st.info('Please enter x and y axes !')
        else:    
            ax = sns.barplot(
                data=self.data, 
                x=self.x, 
                y=self.y, 
                hue=self.hue,
                estimator=self.estimator, 
                palette=self.palette, 
                alpha=self.alpha,
                fill=self.fill, 
                errorbar=self.error_bar, 
                order=self.order)

            self.figure_setting(self.xlabel, self.ylabel, self.title)
            st.pyplot(fig)


class LinePlot(Dataset):
    def __init__(self, data, name='line') -> None:
        super().__init__(data)
        self.name = name
        self.data = data

    def set_axis(self, variable_container):
        datetime_var = variable_container['datetime_var']
        continuous_var = variable_container['continuous_var']

        self.x = st.selectbox(
            "Choose x-axis:", 
            list([None] + datetime_var + continuous_var), 
            key="x_" + self.name, 
            help="Should be Date time or continuous variable")

        self.y = st.selectbox(
            "Choose y-axis:", 
            list([None] + continuous_var), 
            key="y_" + self.name, 
            help="Accept continuous value")
        
        self.xlabel = st.text_input("x-label:", self.x, key="xlabel_" + self.name, help='Can be self-defined')
        self.ylabel = st.text_input("y-label:", self.y, key="ylabel_" + self.name, help='Can be self-defined')
        self.title = st.text_input("Title:", key='title_' + self.name, help='Can be self-defined')


    def set_style(self, variable_container): 

        categorical_countable_var = variable_container['categorical_countable_var']

        self.hue = st.selectbox(
            label="Hue:", 
            options=list([None] + categorical_countable_var), 
            key="hue_" + self.name,
            help="Only accept countable categorical variables")
        
        self.palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette" + self.name,
            help="Select set of colors you want to display")
        
        self.markers = st.selectbox(
            "Use markers:",
            options=[False, True],
            key='markers_' + self.name,
        )

        self.linestyle = st.selectbox(
            'Line style:',
            options=[None, 'dotted', 'dashed', 'dashdot'],
            key='linestyle_' + self.name,
        )

        self.alpha = st.number_input(
            "Opacity:", 
            min_value=0.0, 
            max_value=1.0, 
            value=1.0, 
            step=0.1, 
            key="alpha_" + self.name,
            help="Default opacity is 1")

    def set_advanced(self, variable_container):
        categorical_countable_var = variable_container['categorical_countable_var']
        
        addline_clicked = st.button('Add line')

        self.size = st.selectbox(
            "Size:", 
            options=list([None] + categorical_countable_var),
            key="size_" + self.name,
            help="Accept any except categorical and uncountable variables")
        
        self.style = st.selectbox(
            "Style:", 
            options=list([None] + categorical_countable_var), 
            key="style_" + self.name,
            help="Accept only categorical and countable variables")
        
    def plot(self):
        sns.set_style(self.theme)
        fig = plt.figure(figsize=self.figsize)

        if self.x is None or self.y is None:
            st.info('Please enter x and y axes !')
        else:    
            ax = sns.lineplot(
                data=self.data, 
                x=self.x, 
                y=self.y, 
                hue=self.hue, 
                palette=self.palette,
                size=self.size, 
                style=self.style, 
                alpha=self.alpha, 
                markers=self.markers,
                linestyle=self.linestyle)

            self.figure_setting(self.xlabel, self.ylabel, self.title)
            st.pyplot(fig)


class Histogram(Dataset):
    def __init__(self, data, name='hist') -> None:
        super().__init__(data)
        self.name = name
        self.data = data
        
    def set_axis(self, variable_container):
        continuous_var = variable_container['continuous_var']
        numeric_var = variable_container['numeric_var']

        self.x = st.selectbox(
            "Choose x-axis:", 
            list([None] + continuous_var + numeric_var), 
            key="x_" + self.name, 
            help='Should be continuous variable')
        
        self.y = st.selectbox(
            "Choose y-axis:", 
            list([None] + continuous_var + numeric_var), 
            key="y_" + self.name, 
            help='Should be continuous variable')

        self.xlabel = st.text_input("x-label:", self.x, key="xlabel_" + self.name, help='Can be self-defined')
        self.title = st.text_input("Title:", key='title_' + self.name, help='Can be self-defined')


    def set_style(self, variable_container): 

        categorical_countable_var = variable_container['categorical_countable_var']

        self.hue = st.selectbox(
            label="Hue:", 
            options=list([None] + categorical_countable_var), 
            key="hue_" + self.name,
            help="Accept only Categorical and countable variables")
        
        self.palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette_" + self.name,
            help="Select set of colors you want to display")
        
        self.bins = 'auto'
        bins_select = st.text_input(
            "Number of bins:",
            value='Auto',
            placeholder='Enter number of bins',
            key='bins_' + self.name
        )
        
        if bins_select.lower() == 'auto':
            self.bins = 'auto'
        else:
            try:
                self.bins = int(bins_select)
            except ValueError:
                st.error("Invalid number of bins")
        
        self.fill = st.selectbox(
            'Fill:',
            options=[True, False],
            key='fill_' + self.name,
        )
        
        self.color = st.selectbox(
            'Color:',
            options=list([None] + color_list),
            key='color_' + self.name
        )
        url = 'https://matplotlib.org/stable/gallery/color/named_colors.html'
        st.write("Color list: [link](%s)" % url)

        self.alpha = st.number_input(
            "Opacity:", 
            min_value=0.0, 
            max_value=1.0, 
            value=1.0, 
            step=0.1, 
            key="alpha_" + self.name,
            help="Default opacity is 1")
        
    def set_advanced(self, variable_container):

        numeric_var = variable_container['numeric_var']
        self.stat = st.selectbox(
            'Aggregate statistic:',
            options=['count', 'frequency', 'probability', 'percent', 'density'],
            key='stat_' + self.name,
            help='Default is count'
        )

        self.kde = st.selectbox(
            'Integrate KDE:',
            options=[False, True],
            key='kde_' + self.name,
        )

        self.element = st.selectbox(
            'Visual representation:',
            options=['bars', 'step', 'poly'],
            key='element_' + self.name,
            help='Default is bars'
        )

        self.weights = st.selectbox(
            'Weight the contribution:',
            options=list([None] + numeric_var),
            key='weights_' + self.name,
            help='Should be numerical variable.'
        )
        

    def plot(self):
        sns.set_style(self.theme)
        fig = plt.figure(figsize=self.figsize)
        
        if self.x is None:
            st.info('Please enter x axes !')
        else:    
            ax = sns.histplot(
                data=self.data, 
                x=self.x, 
                y=self.y, 
                hue=self.hue, 
                weights=self.weights, 
                stat=self.stat, 
                palette=self.palette, 
                alpha=self.alpha, 
                bins=self.bins, 
                fill=self.fill, 
                kde=self.kde,
                color=self.color, 
                element=self.element
                )

            self.figure_setting(self.xlabel, ylabel=self.stat, title=self.title)
            st.pyplot(fig)


class BoxPlot(Dataset):
    def __init__(self, data, name='box') -> None:
        super().__init__(data)
        self.name = name
        self.data = data
        
    def set_axis(self, variable_container):
        categorical_countable_var = variable_container['categorical_countable_var']
        numeric_var = variable_container['numeric_var']

        self.x = st.selectbox(
            "Choose x-axis:", 
            list([None] + categorical_countable_var), 
            key="x_" + self.name, 
            help='Only accept categorical and countable variables')
        
        self.y = st.selectbox(
            "Choose y-axis:", 
            list([None] + numeric_var), 
            key="y_" + self.name, 
            help='Only accept numerical variables')
        
        self.xlabel = st.text_input("x-label:", self.x, key="xlabel_" + self.name, help='Can be self-defined')
        self.ylabel = st.text_input("y-label:", self.y, key="ylabel_" + self.name, help='Can be self-defined')
        self.title = st.text_input("Title:", key='title_' + self.name, help='Can be self-defined')


    def set_style(self, variable_container): 

        categorical_countable_var = variable_container['categorical_countable_var']

        self.hue = st.selectbox(
            label="Hue:", 
            options=list([None] + categorical_countable_var), 
            key="hue_" + self.name,
            help="Accept only Categorical and countable variables")
        
        self.palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette_" + self.name,
            help="Select set of color. This will overide the color property")
        
        self.fill = st.selectbox(
            'Use fill:',
            options=[True, False],
            key='fill_' + self.name,
            help='If True, use solid bar. If False, use line art.'
        )
        
        self.color = st.selectbox(
            'Color:',
            options=list([None] + color_list),
            key='color_' + self.name
        )
        url = 'https://matplotlib.org/stable/gallery/color/named_colors.html'
        st.write("Color list: [link](%s)" % url)


    def set_advanced(self, variable_container):
        
        self.gap = st.number_input(
            'Gap between hue boxes:',
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            key='gap_' + self.name,
            help='Ranging from 0 to 1'
        )

        if self.x is not None:
            self.order = st.multiselect(
                'Select order of x-axis:',
                options=self.data[self.x].unique(),
                default=self.data[self.x].unique(),
                key='order_' + self.name,
                help='Provide the order and appearance of each bar'
            )
            if self.order == []:
                self.order = None
        else:
            self.order = st.multiselect(
                'Select order of x-axis:',
                options=[],
                default=None,
                key='order_' + self.name,
                help='Provide the order and appearance of each bar'
            )
        
    def plot(self):
        sns.set_style(self.theme)
        fig = plt.figure(figsize=self.figsize)

        if self.x is None or self.y is None:
            st.info('Please enter x and y axes !')
        else:    
            ax = sns.boxplot(
                data=self.data, 
                x=self.x, 
                y=self.y, 
                hue=self.hue,
                fill=self.fill,
                color=self.color,
                palette=self.palette,
                gap=self.gap,
                order=self.order
                )

            self.figure_setting(self.xlabel, self.ylabel, self.title)
            st.pyplot(fig)


class PiePlot(Dataset):
    def __init__(self, data, name='pie') -> None:
        super().__init__(data)
        self.name = name
        self.data = data
        
    def set_axis(self, variable_container):
        categorical_countable_var = variable_container['categorical_countable_var']

        self.x = None
        self.labels = None
        x = st.selectbox(
            "Choose x-axis:", 
            list([None] + categorical_countable_var), 
            key="x_" + self.name, 
            help='Only accept categorical and countable variables')
        
        labels = st.selectbox(
            'Display label:',
            options=[True, False],
            key='label_' + self.name
        )
        
        if x is not None:
            x_unique = self.data[x].unique()
            x_freq = compute_freq(x_unique)
            self.x = list(x_freq.values())
            if labels:
                self.labels = list(x_freq.keys())
            
        self.autopct = None
        autopct = st.selectbox(
            'Display percentage:',
            options=[True, False],
            key='autopct_' + self.name,
            help='Display percentage of each piece. Default to second decimal number'
        ) 
        if autopct:
            self.autopct = '%1.2f%%'

        self.title = st.text_input("Title:", key='title_' + self.name, help='Can be self-defined')


    def set_style(self, variable_container): 

        categorical_countable_var = variable_container['categorical_countable_var']
        
        self.palette = st.selectbox(
            "Palette:", 
            options=list([None] + palette_list), 
            key="palette_" + self.name,
            help="Select set of color. This will overide the color property")
        
        self.explode = None
        # explode = st.number_input(
        #     'Explode by:',
        #     min_value=0.0,
        #     max_value=0.5,
        #     value=0.0,
        #     step=0.05,
        #     key='explode_' + self.name,
        #     help='Explode all pieces of a pie chart.'
        # )
        # self.explode = np.ones(len(self.x)) * explode
       
        self.shadow = st.selectbox(
            'Shadow:',
            options=[False, True],
            key='shadow_' + self.name
        )

    def set_advanced(self, variable_container):
        
        self.startangle = st.number_input(
            'Rotate starting angle by:',
            min_value=0,
            max_value=360,
            value=0,
            step=15,
            key='startangle_' + self.name,
            help='Rotate counter-clockwise'
        )
        
    def plot(self):
        sns.set_style(self.theme)
        fig = plt.figure(figsize=self.figsize)

        if self.x is None:
            st.info('Please enter x and y axes !')
        else:    
            ax = plt.pie(
                data=self.data, 
                x=self.x, 
                labels=self.labels,
                autopct=self.autopct,
                colors=sns.color_palette(self.palette),
                explode=self.explode,
                shadow=self.shadow,
                startangle=self.startangle
                )

            self.figure_setting(xlabel=None, ylabel=None, title=self.title)
            st.pyplot(fig)