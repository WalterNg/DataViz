import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image


def show_static_page():
    '''
    This is the whole static visualization page
    '''
    # Page Title
    st.title(":bar_chart: DataViz Static")
    
    # Uploading files
    file_uploaded = st.file_uploader("Upload your dataset")
    if file_uploaded:
        data = pd.read_csv(file_uploaded)
        st.write(data)
        columns = data.columns.tolist()
        col_types = [data[col].dtype.name for col in columns]
        ############ CREATE SIDEBAR FOR TYPE SPLITTING ##############

        # Split variables into numeric and categorical  
        # TODO Create 4 types of variables  
        numeric_var_list = data.describe().columns.tolist()
        categorical_var_list = data.columns.difference(numeric_var_list).tolist()
        datetime_list = [col for col in data.columns if data[col].dtype == '<M8[ns]']
        
        continuous_var_list = []
        categorical_countable_list = []
        categorical_uncountable_list = []
        

        st.sidebar.header("Types of variables")
        st.sidebar.warning("Done this before visualize your data")
        COUNTABLE_THRESHOLD = st.sidebar.number_input("Countable threshold:", min_value=1, max_value=30, value=10, 
                                key="count_threshold", 
                                help="By default, countable means less than or equal 10. You can adjust it properly (min is 1 and max is 30)")
        # Check for numeric countable or uncountable
        for var in numeric_var_list:
            if len(data[var].unique()) <= COUNTABLE_THRESHOLD:
                categorical_countable_list.append(var)
            else:
                continuous_var_list.append(var)

        for var in categorical_var_list:
            if len(data[var].unique()) <= COUNTABLE_THRESHOLD:
                categorical_countable_list.append(var)
            else:
                categorical_uncountable_list.append(var)


        # Side bar (default splitting by function, you can adjust later)
        continuous_var = st.sidebar.multiselect("Continuous variables",
                                                    options=columns,
                                                    default=continuous_var_list)

        categorical_countable_var = st.sidebar.multiselect("Categorical and countable variables",
                                                    options=columns,
                                                    default=categorical_countable_list)
                                            
        categorical_uncountable_var = st.sidebar.multiselect("Categorical and uncountable variables",
                                                    options=columns,
                                                    default=categorical_uncountable_list)

        datetime_var = st.sidebar.multiselect("Datetime objects",
                                                    options=columns, default=datetime_list,
                                                    help='''Variables in this box will be converted into datetime object.
                                                    It's not always gonna work because date time objects are various, so make sure what you're doing!
                                                    ''')

        from static_plot import datetime_converter
        data, err_date = datetime_converter(data=data, datetime_var=datetime_var)

        # General information
        with st.expander("General Information"):
            nrow, ncol = data.shape
            st.write(f"Data shape:  ({nrow},{ncol})")
            st.markdown("**Number of NA**")
            summary_dict = {'Columns': columns, "Data types": col_types,"NA's": data.isna().sum().values}
            summary = pd.DataFrame(summary_dict)
            st.write(summary)

        with st.expander("Don't know what to plot? See here"):
            image_path = "media/charts_options.jpeg"
            image = Image.open(image_path)
            st.image(image)
            
        ############ CHOOSE PLOT TYPE ##############

        # Some param list
        st.markdown("### Choose your plot")

        graph_list = ['Scatter plot', "Line chart", "Bar chart", "Pie chart", "Boxplot", "Bubble chart", "Histogram", "Violin Plot", 
                        "Joint Plot", "Heatmap", "KDE Plot", "Contour plot", "Candlestick Charts"]
        graph_list.sort(reverse=False)

        palette_list = ["viridis","plasma","inferno","magma","cividis","YlOrRd","PuBuGn","spring","summer","autumn","winter",
        "cool","hot","cooper","coolwarm","Spectral","seismic","twilight",'Pastel1', 'Pastel2', "husl","Set2","Set2","Set3","flare","Dark2"]
        palette_list.sort(reverse=True)

        legend_loc_list = ['You choose','best','center','upper left', 'upper right', 'lower left', 'lower right','upper center', 'lower center', 'center left', 'center right']

        user_graphs = st.multiselect("What do you want to plot?", graph_list)
        marker_dict = {None:None, "circle":"o", "triangle":"v", "square":"s", "plus":"P", "X":"X"}
        marker_list = [m for m in marker_dict.keys()]
        # ---------------------------------------------------------------------------------
        

        ###########################################################################
        #               FUNCTION DEFINITION IN ORDER TO PLOT GRAPH
        ###########################################################################    
        #   
        def get_setup(key): 
            # TODO Initialize all necessary parameters
            x = None
            y = None
            xlabel = None
            ylabel = None
            title = None
            stat = None
            
            # TODO Apply on each kind of graph
            if key == 'scatter':
                x = st.selectbox("Choose x-axis:", list([None] + columns), key="x_" + key, help="Can be any value")
                y = st.selectbox("Choose y-axis:", list([None] + columns), key="y_" + key, help="Can be any value")
                xlabel = st.text_input("x-label:", x, key="xlabel_" + key, help='Can be self-defined')
                ylabel = st.text_input("y-label:", y, key="ylabel_" + key, help='Can be self-defined')
                title = st.text_input("Title:", key='title_' + key, help='Can be self-defined')

                return x, y, xlabel, ylabel, title

            elif key == 'line':
                x = st.selectbox("Choose x-axis:", list([None] + datetime_var + continuous_var), key="x_" + key, help="Should be datetime object")
                y = st.multiselect("Choose y-axis:", continuous_var, key="y_" + key, help="Only accept continuous variables")
                xlabel = st.text_input("x-label:", x, key="xlabel_" + key)
                ylabel = st.text_input("y-label:", "", key="ylabel_" + key)
                title = st.text_input("Title:", key='title_' + key)
                if len(y) == 0:
                    y = None

                return x, y, xlabel, ylabel, title

            elif key == 'bar':
                x = st.selectbox("Choose x-axis:", list([None] + categorical_countable_var), key="x_" + key, help='Only accept categorical and countable variables')
                y = st.selectbox("Choose y-axis:", list([None] + continuous_var), key="y_" + key, help='Only accept continuous variables')
                xlabel = st.text_input("x-label:", x, key="xlabel_" + key)
                ylabel = st.text_input("y-label:", y, key="ylabel_" + key)
                title = st.text_input("Title:", key='title_' + key)

                return x, y, xlabel, ylabel, title

            elif key == 'hist':
                continuous_categorical_countable = list(set(continuous_var + categorical_countable_var))
                x = st.selectbox("Choose x-axis:", list([None] + continuous_categorical_countable), key="x_" + key, help="Accept any except categorical and uncountable variables.")
                y = st.selectbox("Choose y-axis:", list([None] + columns), key="y_" + key, help="Accept any except categorical and uncountable variables.")
                stat = st.selectbox("Choose statistical measure:", ['count', 'frequency', 'probability', 'percent', 'density'], 
                                    key='stat_' + key, help="Aggregate statistic to compute in each bin.")

                if y is None:
                    xlabel = st.text_input("x-label:", x, key="xlabel_" + key)
                    ylabel = st.text_input("y-label:", stat, key="ylabel_" + key)
                elif x is None:
                    xlabel = st.text_input("x-label:", stat, key="xlabel_" + key)
                    ylabel = st.text_input("y-label:", y, key="ylabel_" + key)
                else:
                    xlabel = st.text_input("x-label:", x, key="xlabel_" + key)
                    ylabel = st.text_input("y-label:", y, key="ylabel_" + key)
                title = st.text_input("Title:", key='title_' + key)

                return x, y, stat, xlabel, ylabel, title

            elif key == 'box':
                x = st.selectbox("Choose x-axis:", list([None] + categorical_countable_var), key="x_" + key, help='Only accept categorical and countable variables')
                y = st.selectbox("Choose y-axis:", list([None] + continuous_var), key="y_" + key, help='Only accept continuous variables')
                xlabel = st.text_input("x-label:", x, key="xlabel_" + key)
                ylabel = st.text_input("y-label:", y, key="ylabel_" + key)
                title = st.text_input("Title:", key='title_' + key)

                return x, y, xlabel, ylabel, title


        def get_style(key): 
            # TODO Initialize all necessary parameters  
            hue = None 
            palette = None
            size = None
            style = None
            marker = None
            color = None 
            orient = None
            bins = None
            kde = None
            fill = None
            cmap = None

            # TODO Apply on each kind of graph
            if key == 'scatter':
                conti_cate_countable = list(set(continuous_var + categorical_countable_var))
                hue = st.selectbox("Hue:", list([None] + conti_cate_countable), key="hue_" + key,
                                    help="Accept any except categorical and uncountable variables")
                palette = st.selectbox("Palette:", list([None] + palette_list), key="palette" + key,
                                    help="Select set of colors you want to display")
                size = st.selectbox("Size:", list([None] + conti_cate_countable), key="size_" + key,
                                    help="Accept any except categorical and uncountable variables")
                style = st.selectbox("Style:", list([None] + categorical_countable_var), key="style_" + key,
                                    help="Accept only categorical and countable variables")
                
                return hue, palette, size, style

            elif key == 'line':
                hue = st.selectbox("Hue:", list([None] + categorical_countable_var), key="hue_" + key, help="Only accept categorical and countable variables")
                palette = st.selectbox("Palette:", list([None] + palette_list), key="palette" + key)
                size = st.selectbox("Size:", list([None] + categorical_countable_var), key="size_" + key, help="Only accept categorical and countable variables")
                style = st.selectbox("Style:", list([None] + categorical_countable_var), key="style_" + key, help="Only accept categorical and countable variables")
                marker = st.selectbox("Marker:", marker_list, key="marker_" + key)
                marker = marker_dict[marker]
                return hue, palette, size, style, marker

            
            elif key == "bar":
                hue = st.selectbox("Hue:", list([None] + categorical_countable_var), key="hue_" + key, help="Only accept categorical and countable variables")
                palette = st.selectbox("Palette:", list([None] + palette_list), key="palette" + key)
                orient_dict = {"Vertical": "v", "Horizontal": "h"}
                orient_set = st.selectbox("Orient:", ["Vertical", "Horizontal"], key="orient_" + key)
                orient = orient_dict[orient_set]
                color_set = st.text_input("Select color:", value='Default', key='color_' + key)
                st.write("[Color table](https://matplotlib.org/stable/gallery/color/named_colors.html)")
                if color_set != 'Default':
                    color = color_set

                return hue, palette, color, orient

            elif key == "hist":
                hue = st.selectbox("Hue:", list([None] + columns), key="hue_" + key)
                palette = st.selectbox("Palette:", list([None] + palette_list), key="palette" + key)
                color_set = st.text_input("Select color:", value='Default', key='color_' + key)
                st.write("[Color table](https://matplotlib.org/stable/gallery/color/named_colors.html)")
                if color_set != 'Default':
                    color = color_set
                bins_select = st.selectbox("Bins:", ['auto','You choose'], key='bins_select_' + key)
                if bins_select == 'You choose':
                    bins = st.number_input("Number of bins:", min_value=1, max_value=50, value=20, step=1, key="bins_" + key)
                else:
                    bins = 'auto'
                kde = st.selectbox("KDE:", [False, True], key='kde_' + key)
                fill = st.selectbox("Fill:", [True,False], key='fill_' + key)
                cbar = st.selectbox("Color bar:", [True, False], key="cbar_" + key, help="Color bar when 2D histogram is used.")
                cmap = st.selectbox("Choose color map:", list([None] + palette_list), key="cmap_" + key, help="Color map applied when 2D histogram is used.")

                return hue, palette, color, bins, kde, fill, cbar, cmap

            elif key == 'box':
                hue = st.selectbox("Hue:", list([None] + categorical_countable_var), key="hue_" + key, help="Only accept categorical and countable variables")
                palette = st.selectbox("Palette:", list([None] + palette_list), key="palette" + key)
                orient_dict = {"Vertical": "v", "Horizontal": "h"}
                orient_set = st.selectbox("Orient:", ["Vertical", "Horizontal"], key="orient_" + key)
                orient = orient_dict[orient_set]

                return hue, palette, orient

        def get_advanced(key, x=None):
            # TODO Initialize all necessary parameters 
            alpha = None
            sizes = None
            ci = None  
            saturation = None
            estimator = None 
            order = None
            discrete = None
            element = None
            multiple = None
            shrink = None
            logscale = None
            thresh = None
            pthresh = None
            cumulative = None


            # TODO Apply on each kind of graph
            if key == 'scatter':
                alpha = st.number_input("Opacity:", min_value=0.0, max_value=1.0, value=1.0, step=0.1, key="alpha_" + key,
                                        help="Default opacity is 1")
                sizes_select = st.selectbox("Range of sizes:", ['auto', 'You choose'], key='sizes_select_' + key, 
                                        help='Range of sizes when size is used') 
                if sizes_select == 'You choose':
                    sizes_lower = st.number_input("Select lower limit of sizes:", min_value=10, max_value=200, value=10, step=10,
                                                    key='sizes_lower_' + key, help='Min is 10 and max is 200')
                    sizes_upper = st.number_input("Select upper limit of sizes:", min_value=10, max_value=200, value=60, step=10,
                                                    key='sizes_upper_' + key, help='Min is 10 and max is 200')
                    sizes = (sizes_lower, sizes_upper)

                return alpha, sizes

            elif key == 'line':
                ci_set = st.selectbox("Confidence Interval:", [None, 'Standard Deviation', 'You choose'], key='ci_set' + key, 
                                    help='Auto will use standard deviation. If pass in a number, it is the size of confidence interval')
                if ci_set == 'Standard Deviation':
                    ci = 'sd'
                elif ci_set == 'You choose':
                    ci = st.number_input("Size of confidence interval:", min_value=0, max_value=100, value=90, step=10,
                                        key='ci_' + key, help='Default is 90')
                alpha = st.number_input("Opacity:", min_value=0.0, max_value=1.0, value=1.0, step=0.1, key="alpha_" + key)
                return ci, alpha

            elif key == 'bar':
                saturation = st.number_input("Saturation:", min_value=0.0, max_value=1.0, value=0.75, step=0.1, key="saturation_" + key,
                                            help="Default is 0.75")

                estimator_set = st.selectbox("Choose estimator:", ['Mean','Median','Min','Max'], key="estimator_" + key,
                                        help="Select function to apply on (Default to mean)")

                ci_set = st.selectbox("Confidence Interval:", [None, 'Standard Deviation', 'You choose'], key='ci_set' + key, 
                                    help='Auto will use standard deviation. If pass in a number, it is the size of confidence interval')
                if ci_set == 'Standard Deviation':
                    ci = 'sd'
                elif ci_set == 'You choose':
                    ci = st.number_input("Size of confidence interval:", min_value=0, max_value=100, value=90, step=10,
                                        key='ci_' + key, help='Default is 90')
                estimator_dict = {'Mean':np.mean, 'Median': np.median, 'Min': np.min, 'Max': np.max}
                estimator = estimator_dict[estimator_set]

                if x is not None:
                    order = st.multiselect("Select order of x-axis:", list(data[x].unique()), key="order_" + key, help="Specify the order on x-axis")
                    if len(order) == 0:
                        order = None

                return saturation, estimator, ci, order

            elif key == 'hist':
                discrete = st.selectbox("Discrete form:", [None, True, False], key="discrete_" + key, 
                                        help="""If True, default to bin width = 1 and draw the bars so that they are centered on their 
                                        corresponding data points. This avoids “gaps” that may otherwise appear when using discrete 
                                        (integer) data.""")

                element = st.selectbox("Visual representation:", ["bars", "step", "poly"], key="element_" + key,
                                        help="Visual representation of the histogram statistic. Only relevant with univariate data.")

                multiple = st.selectbox("Multiple elements:", ["layer", "dodge", "stack", "fill"], key="multiple_" + key,
                                        help="Approach to resolving multiple elements when semantic mapping creates subsets. Only relevant with univariate data.")
                
                shrink = st.number_input("Shrink:", min_value=0.0, max_value=1.0, value=1.0, step=0.1, key="shrink_" + key,
                                        help="Scale the width of each bar relative to the binwidth by this factor. Only relevant with univariate data.")
                
                logscale = st.selectbox("Set axes to log scale:", [False, True], key="logscale_" + key, help="Set axis scale(s) to log")

                thresh = st.number_input("Threshold:", min_value=-10e9, max_value=10e9, value=0.0, step=1.0, key="thresh_" + key,
                                        help="Cells with a statistic less than or equal to this value will be transparent. Only relevant with bivariate data.")

                pthresh = st.number_input("Threshold in Proportion:", min_value=0.0, max_value=1.0, step=0.1, key="pthresh_" + key,
                                        help="Like thresh, but a value in [0, 1] such that cells with aggregate counts (or other statistics, when used) up to this proportion of the total will be transparent.")
                
                cumulative = st.selectbox("Cumulative:", [False, True], key="cumulative_" + key,
                                        help="If True, plot the cumulative counts as bins increase.")

                return discrete, element, multiple, shrink, logscale, thresh, pthresh, cumulative

        def get_figure_setting(key):
            bbox_to_anchor = None
            legend_loc = st.selectbox("Legend locate:", legend_loc_list, index=1, key="legend_loc_" + key, 
                                        help="You can locate legend using coordinate")
            if legend_loc == 'You choose':
                legend_loc_x = st.number_input("x coordinate of legend:", min_value=0.0, max_value=2.0, value=1.0, step=0.1, key="legend_x_" + key,
                                                help="x coordinate of legend")
                legend_loc_y = st.number_input("y coordinate of legend:", min_value=0.0, max_value=2.0, value=1.0, step=0.1,key="legend_y_" + key,
                                                help="y coordinate of legend") 
                legend_loc = None
                bbox_to_anchor = (legend_loc_x,legend_loc_y)

            rotation_x = st.number_input('x-ticks rotation:', min_value=-90, max_value=90, value=0, step=1, key='rotation_x_' + key,
                                            help="Vary from -90 degree to 90 degree")
            rotation_y = st.number_input('y-ticks rotation:', min_value=-90, max_value=90, value=0, step=1, key='rotation_y_' + key,
                                            help="Vary from -90 degree to 90 degree")
            figure_width = st.number_input("Figure's Width:", min_value=1.0, max_value=20.0, value=6.0, step=1.0, key='fig_width_' + key, help='Default is 6')
            figure_height = st.number_input("Figure's Height:", min_value=1.0,max_value=20.0, value=5.0, step=1.0,key='fig_height_' + key, help="Default is 5")
            figsize = (figure_width, figure_height)
            dpi = st.number_input("Dots per inch (DPI):", min_value=100, max_value=300, value=100, step=50, key="dpi_" + key,
            help="Default is 100")
            theme = st.selectbox("Select theme:", ['white','whitegrid','dark','darkgrid'], key="theme_" + key)

            xbins = st.selectbox("Number of bins on x-axis:", ['auto','You choose'], key='xbins_' + key, help="How many values you want to display on x-axis")
            if xbins == 'You choose':
                xbins = st.number_input("Number of bins on x-axis:", min_value=0, max_value=30, value=10, step=1, key="xbins_num_" + key,
                                        help="Only work if x axis is continuous")
            
            ybins = st.selectbox("Number of bins on y-axis:", ['auto','You choose'], key='ybins_' + key, help="How many values you want to display on y-axis")
            if ybins == 'You choose':
                ybins = st.number_input("Number of bins on y-axis:", min_value=0, max_value=30, value=10, step=1, key="ybins_num_" + key, 
                                        help="Only work if y axis is continuous")

            return figsize, theme, dpi, rotation_x, rotation_y,legend_loc, bbox_to_anchor, xbins, ybins


        ###########################################################################
        #                           PLOTTING SECTION 
        ###########################################################################
        from static_plot import plot_scatter, plot_line, plot_bar, plot_hist
        for graph in user_graphs:

            # Tab Settings
            lstTabs = ['Setup',"Style","Advanced","Figure Setting"]
            whitespace = 6
            ###########################################
            # SCATTER PLOT
            ###########################################  
            if graph == "Scatter plot":
                col1, col2 = st.columns([1.5,1], gap='medium')
                tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])
                # Perform scatter plot
                # TODO get parameters for the plot
                with col2:
                    with tabs[0]:
                        x, y, xlabel, ylabel, title = get_setup(key='scatter')

                    with tabs[1]:
                        hue, palette, size, style = get_style(key='scatter')

                    with tabs[2]:
                        alpha, sizes = get_advanced(key='scatter')

                    with tabs[3]:
                        figsize, theme, dpi, rotation_x, rotation_y, legend_loc, bbox_to_anchor, xbins, ybins = get_figure_setting(key='scatter')
                with col1:
                    if err_date is not None:
                        col1.error(err_date)
                    else:
                        plot_scatter(data=data, x=x, y=y, hue=hue, palette=palette, xlabel=xlabel, ylabel=ylabel, size=size, 
                                    style=style, alpha=alpha, sizes=sizes, title=title, legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, 
                                    xbins=xbins, ybins=ybins,figsize=figsize,theme=theme,dpi=dpi, rotation_x=rotation_x, rotation_y=rotation_y)
                

            ###########################################
            # LINE CHART
            ###########################################    
            elif graph == "Line chart":
                col1, col2 = st.columns([1.5,1], gap='medium')
                tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])
                # Perform line chart
                # TODO get parameter for the plot
                with col2:
                    with tabs[0]:
                        x, y, xlabel, ylabel, title = get_setup(key='line')

                    with tabs[1]:
                        hue, palette, size, style, marker = get_style(key='line')
                                
                    with tabs[2]:
                        ci, alpha = get_advanced(key='line')

                    with tabs[3]:
                        figsize, theme, dpi, rotation_x, rotation_y, legend_loc, bbox_to_anchor, xbins, ybins = get_figure_setting(key='line')

                with col1:
                    if err_date is not None:
                        col1.error(err_date)
                    else:
                        plot_line(data=data, x=x, y=y, hue=hue, palette=palette, xlabel=xlabel, ylabel=ylabel, size=size, marker=marker, 
                                style=style, alpha=alpha, title=title, legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xbins=xbins, 
                                ybins=ybins, ci=ci,figsize=figsize,theme=theme,dpi=dpi,rotation_x=rotation_x, rotation_y=rotation_y)

            
            ###########################################
            # BAR PLOT
            ###########################################  

            elif graph == "Bar chart":
                col1, col2 = st.columns([1.5,1], gap='medium')
                tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])
                # Perform bar chart
                # TODO get parameter for the plot
                with col2:
                    with tabs[0]:
                        x, y, xlabel, ylabel, title = get_setup(key='bar')

                    with tabs[1]:
                        hue, palette, color, orient = get_style(key='bar')
                                
                    with tabs[2]:
                        saturation, estimator, ci, order = get_advanced(key='bar', x=x)

                    with tabs[3]:
                        figsize, theme, dpi, rotation_x, rotation_y, legend_loc, bbox_to_anchor, xbins, ybins = get_figure_setting(key='bar')

                with col1:
                    try:
                        if orient == "v":
                            plot_bar(data, x, y, hue=hue, palette=palette, color=color, orient=orient, saturation=saturation, ci=ci,
                                    estimator=estimator, order=order,xlabel=xlabel, ylabel=ylabel, title=title, legend_loc=legend_loc, 
                                    bbox_to_anchor=bbox_to_anchor, xbins=xbins, ybins=ybins,figsize=figsize,theme=theme, dpi=dpi)
                        else:
                            plot_bar(data, x=y, y=x, hue=hue, palette=palette, color=color, orient=orient, saturation=saturation, ci=ci,
                                    estimator=estimator, order=order,xlabel=ylabel, ylabel=xlabel, title=title, legend_loc=legend_loc, 
                                    bbox_to_anchor=bbox_to_anchor, xbins=xbins, ybins=ybins,figsize=figsize,theme=theme, dpi=dpi)
                    except TypeError:
                        st.info("Please enter x and y axes !")
                    
            ###########################################
            # DISTRIBUTION PLOT
            ########################################### 
            elif graph == 'Histogram':
                col1, col2 = st.columns([1.5,1], gap='medium')
                tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])
                # Perform bar chart
                # TODO get parameter for the plot
                with col2:
                    with tabs[0]:
                        x, y, stat, xlabel, ylabel, title = get_setup(key='hist')

                    with tabs[1]:
                        hue, palette, color, bins, kde, fill, cbar, cmap = get_style(key='hist')
                                
                    with tabs[2]:
                        discrete, element, multiple, shrink, logscale, thresh, pthresh, cumulative = get_advanced(key='hist', x=x)

                    with tabs[3]:
                        figsize, theme, dpi, rotation_x, rotation_y, legend_loc, bbox_to_anchor, xbins, ybins = get_figure_setting(key='hist')

                with col1:
                    plot_hist(data, x=x, y=y, hue=hue, palette=palette, color=color, bins=bins, cumulative=cumulative,
                    shrink=shrink, fill=fill, kde=kde, cbar=cbar, thresh=thresh, pthresh=pthresh, stat=stat, cmap=cmap,
                    discrete=discrete, element=element, multiple=multiple, logscale=logscale, xlabel=xlabel, ylabel=ylabel, 
                    title=title, legend_loc=legend_loc, bbox_to_anchor=bbox_to_anchor, xbins=xbins, ybins=ybins,theme=theme, 
                    figsize=figsize, dpi=dpi)
                

            ###########################################
            # BOX PLOT
            ###########################################
            elif graph == 'Boxplot':
                col1, col2 = st.columns([1.5,1], gap='medium')
                tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lstTabs])
                # Perform bar chart
                # TODO get parameter for the plot
                with col2:
                    with tabs[0]:
                        x, y, xlabel, ylabel, title = get_setup(key='box')

                    with tabs[1]:
                        hue, palette, orient = get_style(key='box')
                                
                    # with tabs[2]:
                    #     discrete, element, multiple, shrink, logscale, thresh, pthresh, cumulative = get_advanced(key='box', x=x)

                    # with tabs[3]:
                    #     figsize, theme, dpi, rotation_x, rotation_y, legend_loc, bbox_to_anchor, xbins, ybins = get_figure_setting(key='box')
                    
