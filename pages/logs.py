import streamlit as st
import os
import yaml
from datetime import datetime

st.set_page_config(page_title="Logs Viewer", page_icon=":scroll:", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title(":scroll: Logs Viewer")

LOGS_FOLDER = "data/logs"
log_files = [f for f in os.listdir(LOGS_FOLDER) if f.endswith('_logs.yaml') or f.endswith('_prompts_responses.yaml')]

def load_logs(file_path):
    with open(file_path, 'r') as file:
        logs = yaml.safe_load(file)
    return logs

if log_files:
    selected_log_file = st.selectbox("Select a log file to view:", log_files)

    if selected_log_file:
        log_file_path = os.path.join(LOGS_FOLDER, selected_log_file)
        logs = load_logs(log_file_path)

        if logs:
            sorted_logs = sorted(logs, key=lambda x: datetime.strptime(x['timestamp'], "%Y-%m-%d %H:%M:%S"), reverse=True)
            for log in sorted_logs:
                st.write(f"Timestamp: {log['timestamp']}")
                st.write(f"User Email: {log['user_email']}")
                if 'event_type' in log:
                    st.write(f"Event Type: {log['event_type']}")
                    st.write(f"Event Details: {log['event_details']}")
                if 'prompt' in log:
                    st.write(f"Prompt: {log['prompt']}")
                    st.write(f"Response: {log['response']}")
                st.write("---")
        else:
            st.write("No logs found in the selected file.")
else:
    st.write("No log files found.")
