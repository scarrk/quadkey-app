import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title='Quadkey Helper Application',
        page_icon='x'
    )

    st.header('Home Page')
    st.markdown('A collection of spatial scripts to assist with working with quadkeys.')

    st.markdown('### Acknowledgements')
    st.markdown("Thanks to Streamlit, Mercantile, Folium")

if __name__ == "__main__":
    run()
