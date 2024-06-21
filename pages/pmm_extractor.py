import streamlit as st
import yaml
import os
from utils import load_websites, save_website, generate_website_info, info_box

st.title("PMM Extractor")

# Sidebar with website dropdown
st.sidebar.title("Websites")
websites = load_websites()
website_names = [site['name'] for site in websites]
website_names.append("Create New Website")
selected_website = st.sidebar.selectbox("Select Website", website_names)

if selected_website == "Create New Website":
    new_website_url = st.text_input("Website URL")

    if st.button("Pre-populate fields"):
        if new_website_url:
            # Generate website info using OpenAI
            new_website_info = generate_website_info(new_website_url)
            st.session_state['new_website_info'] = new_website_info
        else:
            st.error("Please enter a website URL")

    if 'new_website_info' in st.session_state:
        new_website_info = st.session_state['new_website_info']
        new_website_name = st.text_input("Website Name", new_website_info['name'])
        new_messaging = st.text_area("Messaging", new_website_info['messaging'])
        new_personas = st.text_area("Personas (one per line)", "\n".join(new_website_info['personas']))
        new_differentiators = st.text_area("Differentiators (one per line)", "\n".join(new_website_info['differentiators']))

        if st.button("Save New Website"):
            new_website = {
                'name': new_website_name,
                'website_url': new_website_url,
                'messaging': new_messaging,
                'personas': new_personas.split("\n"),
                'differentiators': new_differentiators.split("\n")
            }
            save_website(new_website)
            st.success("New website created successfully!")
else:
    website = next(site for site in websites if site['name'] == selected_website)
    messaging = st.text_area("Messaging", website['messaging'])
    personas = st.text_area("Personas", "\n".join(website['personas']))
    differentiators = st.text_area("Differentiators", "\n".join(website['differentiators']))

    if st.button("Save"):
        website['messaging'] = messaging
        website['personas'] = personas.split("\n")
        website['differentiators'] = differentiators.split("\n")
        save_website(website)
        st.success("Data saved successfully!")

# Display info box at the bottom of the sidebar
info_box()