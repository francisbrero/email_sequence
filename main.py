import streamlit as st
from utils import info_box

st.set_page_config(page_title="Sales Sequence Generator", page_icon=":money_with_wings:", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title(":money_with_wings: Sales Email Sequence Generator")

# Input for OpenAI API key
api_key = st.text_input("Please enter your OpenAI API key to use this app", type="password")
if api_key:
    st.session_state['openai_api_key'] = api_key

# Allow user to select or create a new website
st.sidebar.title("Instructions")
# Instructions
st.sidebar.markdown("""
1. **Go to PMM Extractor**: This will allow you to select a website and extract information about it.
2. **Go to Sequence Generator**: Select a website and a playbook you want to generate a sales email sequence for.
3. **Generate Sequence**: Generate a sales email sequence based on the selected website and playbook.
4. **Edit and Save Sequence**: Edit the generated sequence as needed and save it.
""")


# Display info box at the bottom of the sidebar
info_box()
