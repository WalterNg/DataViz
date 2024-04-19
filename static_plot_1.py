import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


# FIGURE SETTINGS
def fig_setting(legend_loc, bbox_to_anchor, xlabel, ylabel, title, xbins, ybins, rotation_x, rotation_y):
    plt.legend(loc=legend_loc, bbox_to_anchor=bbox_to_anchor)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=15)
    plt.xticks(rotation=rotation_x)
    plt.yticks(rotation=rotation_y)
    if xbins != 'auto':
        plt.locator_params(axis='x', nbins=xbins, tight=True)
    if ybins != 'auto':
        plt.locator_params(axis='y', nbins=ybins, tight=True)

# SCATTER PLOT
def plot_scatter(data,x,y,hue=None, palette=None, size=None, alpha=None, sizes=None, style=None, xlabel=None, ylabel=None, title=None,
                legend='auto', legend_loc='best', bbox_to_anchor=None, xbins='auto', ybins='auto',theme='white',figsize=None,
                dpi=None, rotation_x=None, rotation_y=None):

    # TODO Get all necessary parameters for scatter plot
    sns.set_style(theme)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = sns.scatterplot(x=x, y=y, data=data, hue=hue, palette=palette, size=size, style=style, legend=legend, sizes=sizes,
                    alpha=alpha)
    fig_setting(legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xlabel=xlabel, ylabel=ylabel, title=title, 
                xbins=xbins, ybins=ybins, rotation_x=rotation_x, rotation_y=rotation_y)
    if x is None or y is None:
        st.info('Please enter x and y axes !')
    else:
        st.pyplot(fig)

# LINE PLOT
def plot_line(data,x,y,hue=None, palette=None, size=None, marker=None, alpha=None, style=None, xlabel=None, ylabel=None, title=None,
            legend='auto', legend_loc='best', bbox_to_anchor=None, ci=None, xbins='auto', ybins='auto',theme='white', figsize=None,
            dpi=None, rotation_x=None, rotation_y=None):
    # TODO Get all necessary parameter for line chart
    sns.set_style(theme)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    if y is not None:
        for y_sub in y:
            ax = sns.lineplot(data=data, x=x, y=y_sub, hue=hue, palette=palette, size=size, dashes=True,
                            marker=marker,style=style, legend=legend, alpha=alpha, ci=ci)
        
        fig_setting(legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xlabel=xlabel, ylabel=ylabel, title=title, 
                xbins=xbins, ybins=ybins, rotation_x=rotation_x, rotation_y=rotation_y)
    if x is None or y is None:
        st.info('Please enter x and y axes !')
    else:
        st.pyplot(fig)

# BAR PLOT
def plot_bar(data, x, y, hue=None, palette=None, color=None, orient=None, saturation=0.75, estimator=np.mean, order=None,
            xlabel=None, ylabel=None, title=None, legend_loc='best', bbox_to_anchor=None, ci=None, xbins='auto',
            ybins='auto',theme='white', figsize=None, dpi=None, rotation_x=None, rotation_y=None):
    # TODO Get all necessary parameter for bar chart
    sns.set_style(theme)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = sns.barplot(x=x, y=y, data=data, hue=hue, palette=palette, color=color, orient=orient, saturation=saturation, 
                    estimator=estimator, ci=ci, dodge=False, order=order)
    fig_setting(legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xlabel=xlabel, ylabel=ylabel, title=title, 
                xbins=xbins, ybins=ybins, rotation_x=rotation_x, rotation_y=rotation_y)
    if x is None or y is None:
        st.info('Please enter x and y axes !')
    else:
        st.pyplot(fig)

# HISTOGRAM
def plot_hist(data, x=None, y=None, hue=None, palette=None, color=None, bins='auto', stat='count',fill=None, kde=None, cbar=None,
            cumulative=None, cmap=None, discrete=None, shrink=None, multiple='layer', element='bars', logscale=None, thresh=None, pthresh=None, xlabel=None, 
            ylabel=None, title=None, legend_loc='best', bbox_to_anchor=None, xbins='auto', ybins='auto',theme='white', figsize=None, dpi=None,
            rotation_x=None, rotation_y=None):
    # TODO Get all necessary parameter for dist plot
    sns.set_style(theme)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    axes = (x,y)
    # 2D
    if all(axis is not None for axis in axes):
        ax = sns.histplot(x=x, y=y, data=data, stat=stat, hue=hue, palette=palette, color=color, bins=bins, kde=kde, fill=fill, cbar=cbar, 
                        cmap=cmap, discrete=discrete, element=element, multiple=multiple, shrink=shrink, log_scale=logscale, cumulative=cumulative,
                        thresh=thresh, pthresh=pthresh, legend=True)
        st.write("1")
    # 1D
    else:
        ax = sns.histplot(x=x, y=y, data=data, stat=stat, hue=hue, palette=palette, color=color, bins=bins, kde=kde, fill=fill, cbar=cbar, 
                        discrete=discrete, element=element, multiple=multiple, shrink=shrink, log_scale=logscale, cumulative=cumulative,
                        thresh=thresh, pthresh=pthresh, legend=True)
        # ax = sns.histplot(x=x, y=y, data=data, hue=hue, legend=True)
        st.write("2")
    fig_setting(legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xlabel=xlabel, ylabel=ylabel, title=title, 
                xbins=xbins, ybins=ybins, rotation_x=rotation_x, rotation_y=rotation_y)
    if x is None and y is None:
        st.info('Please enter x and y axes !')
    else:
        st.pyplot(fig)

# BOXPLOT
def plot_box(data, x=None, y=None, hue=None, order=None, orient=None, palette=None, row=None, col=None, col_wrap=None, 
            theme='white', figsize=None, dpi=None, legend_loc='best', bbox_to_anchor=None, xbins='auto', ybins='auto', 
            xlabel=None, ylabel=None, title=None, rotation_x=None, rotation_y=None):
    # TODO Get all necessary parameter for bar chart
    sns.set_style(theme)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = sns.catplot(data=data, x=x, y=y, hue=hue, row=row, col=col, col_wrap=col_wrap, palette=palette, orient=orient,
                    order=order, kind='box')
    
    fig_setting(legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xlabel=xlabel, ylabel=ylabel, title=title, 
                xbins=xbins, ybins=ybins, rotation_x=rotation_x, rotation_y=rotation_y)
    if x is None or y is None:
        st.info('Please enter x and y axes !')
    else:
        st.pyplot(fig)
