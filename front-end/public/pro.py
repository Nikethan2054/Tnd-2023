# importing python libraries

import streamlit as st
from streamlit_option_menu import option_menu

# importing local libraries

from short_TL import *
from nominalpi_TL import *

# page customisation

st.set_page_config(
    page_title="TND-Project",
    page_icon="⚒️"
)

# sidebar Menu

with st.sidebar:
    selected = option_menu(
        menu_title= None,
       options=["Home", "Short Transmission Line", "Nominal-pi Transmission Line"],
       default_index=0, 
       menu_icon="cast", 
    )

if selected == "Home":
    st.title("TRANSMISSION AND DISTRIBUTION SYSTEMS")

    col1, col2 = st.columns(2)
    col1.write("P.SAI NIKETHAN")
    col1.write("P.RISHENDRA PRASAD")
    col1.write("P.SURENDRA BABU")

    col2.write("107121071")
    col2.write("107121069")
    col2.write("107121079")

elif selected == "Short Transmission Line":
    input_page_short()

elif selected == "Nominal-pi Transmission Line":
    input_page_nominal()    