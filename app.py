import streamlit as st
import pandas as pd
import openai
from PIL import Image
import webbrowser
import os

if os.path.exists('str.png'):
    img = Image.open('str.png')
else:
    st.warning("Image file 'str.png' not found.")
st.set_page_config(page_title='Remarks Co-Pilot', page_icon=img)


def main():
    st.image(img, width=100)
    st.title("Remarks Co-Pilot")
    st.write("Note: Remarks Co-Pilot (Python/ Streamlit is (mostly) deprecated")
    if st.button('For Jennifer - click here for AC vetters tool'):
        webbrowser.open('https://vetter-assistant.streamlit.app/')


main()
# add basic font styling
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
