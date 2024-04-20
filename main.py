import streamlit as st
from streamlit_option_menu import option_menu
from interactive import show_interactive_page
from static import show_static_page

st.set_page_config(page_title="Data Visualization",layout='wide')
# Navigation bar
navigation = option_menu(
    menu_title=None,
    options=['Static', 'Interactive'],
    icons=["image", "hand-index-thumb"],
    default_index=0,
    orientation='horizontal',
    key="main_page_key"
)

# Import interactive and static module
if navigation == "Static":
    show_static_page()
elif navigation == 'Interactive':
    # show_interactive_page()
    st.info("Coming soon !")