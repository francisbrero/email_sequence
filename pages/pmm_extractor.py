import streamlit as st
from utils import load_websites, save_website, generate_website_info, info_box

st.title("PMM Extractor")

# Sidebar with website dropdown
st.sidebar.title("Websites")
websites = load_websites()
website_names = [site['name'] for site in websites] + ["Create New Website"]
selected_website = st.sidebar.selectbox("Select Website", website_names)

if selected_website == "Create New Website":
    new_website_url = st.text_input("Enter the website URL")
    if st.button("Pre-populate fields"):
        if new_website_url:
            website_info = generate_website_info(new_website_url)
            websites.append(website_info)
            save_website(website_info)
            st.session_state['selected_website'] = website_info['name']
            st.rerun()  # Refresh the page to show the new website information
        else:
            st.error("Please enter a valid website URL.")
else:
    website = next(site for site in websites if site['name'] == selected_website)
    name = st.text_input("Name", website['name'])
    messaging = st.text_area("Messaging", website['messaging'])
    personas = st.text_area("Personas", ", ".join(website['personas']))
    differentiators = st.text_area("Differentiators", ", ".join(website['differentiators']))

    if st.button("Save Changes"):
        website['name'] = name
        website['messaging'] = messaging
        website['personas'] = personas.split(', ')
        website['differentiators'] = differentiators.split(', ')
        save_website(website)
        st.success("Website information saved successfully.")
        st.session_state['selected_website'] = name
        st.rerun()  # Refresh the page to update the dropdown

# Ensure the dropdown reflects the selected website
if 'selected_website' in st.session_state:
    selected_website = st.session_state['selected_website']

# Display info box at the bottom of the sidebar
info_box()