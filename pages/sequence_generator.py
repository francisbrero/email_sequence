import streamlit as st
import yaml
import os
from utils import load_websites, load_playbooks, save_playbook, generate_sequence, save_sequence, parse_sequence, format_sequence, load_sequence, info_box
from datetime import datetime

st.title("Sequence Generator")

# Sidebar with website dropdown
st.sidebar.title("Websites")
websites = load_websites()
website_names = [site['name'] for site in websites]
selected_website = st.sidebar.selectbox("Select Website", website_names)

# Load selected website information
if selected_website:
    website = next(site for site in websites if site['name'] == selected_website)

# Sidebar with playbook dropdown
st.sidebar.title("Playbooks")
playbooks = load_playbooks()
playbook_titles = [pb['title'] for pb in playbooks]
playbook_titles.append("Create New Playbook")
selected_playbook = st.sidebar.selectbox("Select Playbook", playbook_titles)

if selected_playbook == "Create New Playbook":
    new_playbook_title = st.text_input("Playbook Title")
    new_playbook_description = st.text_area("Description")

    if st.button("Save and Generate Sequence"):
        if new_playbook_title and new_playbook_description:
            new_playbook = {
                'title': new_playbook_title,
                'description': new_playbook_description,
                'conditions': [],  # Ignored for now
                'sequence_link': ""  # Placeholder for now
            }
            save_playbook(new_playbook)

            # Generate the sequence using OpenAI
            sequence = generate_sequence(website, new_playbook)
            st.session_state['sequence'] = sequence

            st.success("New playbook created and sequence generated successfully!")
        else:
            st.error("Please enter both title and description for the new playbook.")
else:
    playbook = next(pb for pb in playbooks if pb['title'] == selected_playbook)
    sequence_file_path = f"data/sequences/{website['name'].replace(' ', '_')}_{playbook['title'].replace(' ', '_')}.yaml"

    if 'sequence' not in st.session_state:
        if os.path.exists(sequence_file_path):
            st.session_state['steps'] = load_sequence(sequence_file_path)
        else:
            st.session_state['sequence'] = ""

    if os.path.exists(sequence_file_path):
        if st.button("Load Existing Sequence"):
            st.session_state['steps'] = load_sequence(sequence_file_path)

        if st.button("Overwrite Sequence"):
            # Generate the sequence using OpenAI
            sequence = generate_sequence(website, playbook)
            st.session_state['sequence'] = sequence
            steps = parse_sequence(sequence)
            st.session_state['steps'] = steps

            st.success("Sequence overwritten successfully!")
    else:
        if st.button("Generate Sequence"):
            # Generate the sequence using OpenAI
            sequence = generate_sequence(website, playbook)
            st.session_state['sequence'] = sequence
            steps = parse_sequence(sequence)
            st.session_state['steps'] = steps

            st.success("Sequence generated successfully!")

    if 'steps' in st.session_state and st.session_state['steps']:
        steps = st.session_state['steps']

        # Ensure session state variables are set before creating widgets
        for idx, step in enumerate(steps):
            if f"step_{idx+1}_subject" not in st.session_state:
                st.session_state[f"step_{idx+1}_subject"] = step['subject']
            if f"step_{idx+1}_body" not in st.session_state:
                st.session_state[f"step_{idx+1}_body"] = step['body']

        for idx, step in enumerate(steps):
            with st.expander(f"Step {idx+1}: {step['title']}"):
                subject_key = f"step_{idx+1}_subject"
                body_key = f"step_{idx+1}_body"
                st.text_input("Subject", st.session_state[subject_key], key=subject_key)
                st.text_area("Body", st.session_state[body_key], key=body_key, height=200)

        if st.button("Save Sequence"):
            updated_steps = []
            for idx in range(len(steps)):
                updated_steps.append({
                    'title': steps[idx]['title'],
                    'subject': st.session_state[f"step_{idx+1}_subject"],
                    'body': st.session_state[f"step_{idx+1}_body"]
                })
            playbook['sequence'] = format_sequence(updated_steps)
            save_playbook(playbook)

            # Save sequence to file
            sequence_data = {
                'name': f"{website['name']} + {playbook['title']}",
                'website': website['name'],
                'playbook': playbook['title'],
                'date_generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'sequence': {f"step {idx+1}": updated_steps[idx] for idx in range(len(updated_steps))}
            }
            save_sequence(sequence_data)

            st.success("Sequence saved successfully!")
    else:
        st.session_state.pop('steps', None)

# Display info box at the bottom of the sidebar
info_box()