import streamlit as st

from interactive_plot import plot_line_chart, plot_scatter


def get_user_chart(list_of_graph):
    user_chart = st.multiselect("Choose your plot:", list_of_graph)
    return user_chart

def add_plot(user_chart):
    for i in user_chart:
        st.write(i)

# def get_user_feature():
    