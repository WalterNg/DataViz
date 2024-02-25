import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# # container1 = st.container()
# # container2 = st.container()
# # user_text = None

# # if 'n_text' not in st.session_state:
# #     st.session_state['n_text'] = 0
# # if 'button_clicked' not in st.session_state:
# #     st.session_state['button_clicked'] = False

# # def callback():
# #     # Button was clicked
# #     st.session_state.button_clicked = True

# # user_add_text = container2.button("Add text", on_click=callback)
# # if user_add_text or st.session_state['button_clicked']:
# #     st.session_state.n_text += 1
# #     for i in range(st.session_state.n_text):
# #         user_text = container1.text_input("Input your text:", key=i)

# # container1.write(user_text)

# st.set_page_config(page_title="Data Visualization",layout='wide')
# st.sidebar.write("Title")
# font_css = """
# <style>
# button[data-baseweb="tab"] {
#   font-size: 18px;
#   font-weight: bold;
# }
# </style>
# """
# st.write(font_css, unsafe_allow_html=True)

# lst = ['a','b','c']
# lst_tabs = ['Setup',"Style","Advanced","Figure Settings"]
# whitespace = 6
# col1,midcol, col2 = st.columns([1.75,0.15,1.2])
# tabs = col2.tabs([s.center(whitespace, "\u2001") for s in lst_tabs])

# col1.title("HELLO")

# file_uploaded = st.file_uploader("Upload your dataset")
# if file_uploaded:
#     data = pd.read_csv(file_uploaded)
#     st.write(data)
#     columns = data.columns.tolist()

# with tabs[0]:
#     x = st.selectbox("Choose x-axis:", columns, key="x_", help="Can be any value")
#     y = st.selectbox("Choose y-axis:", columns, key="y_", help="Can be any value")
#     xlabel = st.text_input("x-label:", x, key="xlabel_" , help='Can be self-defined')
#     ylabel = st.text_input("y-label:", y, key="ylabel_" , help='Can be self-defined')
#     title = st.text_input("Title:", key='title_', help='Can be self-defined')
# with tabs[1]:
#     hue = st.selectbox("Hue:", lst, key="hue_",
#                         help="Accept any except categorical and uncountable variables")
#     palette = st.selectbox("Palette:", lst, key="palette")
#     size = st.selectbox("Size:", lst, key="size_",
#                         help="Accept any except categorical and uncountable variables")
#     style = st.selectbox("Style:", lst, key="style_",
#                         help="Accept only categorical and countable variables")
# fig = plt.figure()
# ax = sns.scatterplot(x=x, y=y, data=data)
# col1.pyplot(fig)

txt = st.text_area('Text to analyze', '''
     It was the best of times, it was the worst of times, it was
     the age of wisdom, it was the age of foolishness, it was
     the epoch of belief, it was the epoch of incredulity, it
     was the season of Light, it was the season of Darkness, it
     was the spring of hope, it was the winter of despair, (...)
     ''')
st.write(txt)