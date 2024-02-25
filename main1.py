import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

# SET PAGE CONFIG
st.set_page_config(page_title="Data Visualization",layout='wide')

# SET ANIMATED LOTTIE
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Initialize some lotties

lottie1_url = "https://assets2.lottiefiles.com/temp/lf20_TOE9MF.json"
lottie1_json = load_lottieurl(lottie1_url)

lottie2_url = "https://assets2.lottiefiles.com/packages/lf20_22mjkcbb.json"
lottie2_json = load_lottieurl(lottie2_url)

lottie3_url = "https://assets4.lottiefiles.com/packages/lf20_kgyknvpj.json"
lottie3_json = load_lottieurl(lottie3_url)


with st.sidebar.container():
    st_lottie(lottie1_json,height =200,width =300)

# ADJUST SIZE OF EXPANDER
st.markdown(
    """
<style>
.streamlit-expanderHeader {
    font-size: 120%;
    font-weight: bold;
</style>
""",
    unsafe_allow_html=True,
)

# ADJUST FONT OF TABS HEADER
font_css = """
<style>
button[data-baseweb="tab"] {
  font-size: 19px;
  font-weight: bold;
}
</style>
"""
st.write(font_css, unsafe_allow_html=True)

# HIDE FOOT NOTE
hide_menu_style="""
        <style>
        footer{visibility:hidden;}
        </style>
        """
st.markdown(hide_menu_style,unsafe_allow_html=True)

# Show lottie
col1 , col2 = st.columns(2)
with col1:
    st_lottie(lottie2_json,height =300,width =300, quality='medium')
with col2:
    st_lottie(lottie3_json, height= 300, width=300, quality='medium')
# Navigation bar
navigation = option_menu(
    menu_title=None,
    options=['Interactive', 'Static'],
    icons=["hand-index-thumb", "image"],
    default_index=0,
    orientation='horizontal',
    key="main_page_key"
)

# Import interactive and static module
from interactive import show_interactive_page
from static import show_static_page

# Page Title
if navigation == 'Interactive':
    # show_interactive_page()
    st.info("Coming soon !")
elif navigation == "Static":
    show_static_page()
