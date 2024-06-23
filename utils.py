import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st

load_dotenv()

def load_websites():
    data_folder = "data/websites"
    websites = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".yaml"):
            with open(os.path.join(data_folder, filename), 'r') as file:
                websites.append(yaml.safe_load(file))
    return websites

def save_website(website):
    data_folder = "data/websites"
    website['last_saved'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(os.path.join(data_folder, f"{website['name']}.yaml"), 'w') as file:
        yaml.safe_dump(website, file)

def load_playbooks():
    data_folder = "data/playbooks"
    playbooks = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".yaml"):
            with open(os.path.join(data_folder, filename), 'r') as file:
                playbooks.append(yaml.safe_load(file))
    return playbooks

def save_playbook(playbook):
    data_folder = "data/playbooks"
    with open(os.path.join(data_folder, f"{playbook['title']}.yaml"), 'w') as file:
        yaml.safe_dump(playbook, file)

def generate_website_info(url):
    prompt_file = "prompts/pmm_extractor_prompt.txt"
    with open(prompt_file, 'r') as file:
        prompt_template = file.read()

    prompt = prompt_template.format(url=url)

    client = OpenAI(
        api_key=st.session_state.get('openai_api_key', os.getenv("OPENAI_API_KEY")),  # use session key if available
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    result = response.choices[0].message.content.strip()
    print(result)

    # Parse the result
    lines = result.split('\n')
    website_info = {}
    personas = []
    differentiators = []
    is_personas = False
    is_differentiators = False
    for line in lines:
        if line.startswith("Name:"):
            website_info["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Messaging:"):
            website_info["messaging"] = line.split(":", 1)[1].strip()
        elif line.startswith("Personas:"):
            is_personas = True
            is_differentiators = False
        elif line.startswith("Differentiators:"):
            is_personas = False
            is_differentiators = True
        elif is_personas:
            if line.strip().startswith("-"):
                personas.append(line.strip().lstrip("-").strip())
        elif is_differentiators:
            if line.strip().startswith("-"):
                differentiators.append(line.strip().lstrip("-").strip())

    website_info["personas"] = personas
    website_info["differentiators"] = differentiators

    return website_info

def generate_sequence(website, playbook):
    prompt_file = "prompts/generate_sequence_prompt.txt"
    with open(prompt_file, 'r') as file:
        prompt_template = file.read()

    prompt = prompt_template.format(
        website_name=website['name'],
        messaging=website['messaging'],
        personas=", ".join(website['personas']),
        differentiators=", ".join(website['differentiators']),
        playbook_title=playbook['title'],
        playbook_description=playbook['description']
    )

    client = OpenAI(
        api_key=st.session_state.get('openai_api_key', os.getenv("OPENAI_API_KEY")),  # use session key if available
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    result = response.choices[0].message.content.strip()

    return result

def parse_sequence(sequence):
    steps = sequence.split('### Step ')[1:]
    parsed_steps = []
    for step in steps:
        title = step.split('\n')[0].strip()
        subject = ""
        body = ""
        in_body = False
        for line in step.split('\n')[1:]:
            if line.startswith("**Subject:**") or line.startswith("Subject:"):
                subject = line.split(":", 1)[1].strip()
            elif line.startswith("**Body:**"):
                in_body = True
            else:
                if in_body or not subject:
                    body += line + "\n"
        parsed_steps.append({
            'title': title,
            'subject': subject.strip(),
            'body': body.strip()
        })
    return parsed_steps

def format_sequence(steps):
    formatted_sequence = ""
    for step in steps:
        formatted_sequence += f"### Step {step['title']}\n"
        formatted_sequence += f"**Subject:** {step['subject']}\n"
        formatted_sequence += f"**Body:** {step['body']}\n\n"
    return formatted_sequence

def save_sequence(sequence_data):
    data_folder = "data/sequences"
    os.makedirs(data_folder, exist_ok=True)
    filename = f"{sequence_data['website'].replace(' ', '_')}_{sequence_data['playbook'].replace(' ', '_')}.yaml"
    with open(os.path.join(data_folder, filename), 'w') as file:
        yaml.safe_dump(sequence_data, file)

def load_sequence(file_path):
    with open(file_path, 'r') as file:
        sequence_data = yaml.safe_load(file)
    steps = []
    for key, value in sorted(sequence_data['sequence'].items(), key=lambda x: int(x[0].split()[-1])):
        steps.append({
            'title': value['title'],
            'subject': value['subject'],
            'body': value['body']
        })
    return steps

def log_event(user_email, event_type, event_details):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_email": user_email,
        "event_type": event_type,
        "event_details": event_details
    }
    log_file_path = os.path.join("data/logs", f"{user_email}_logs.yaml")
    with open(log_file_path, 'a') as file:
        yaml.dump([log_entry], file)

def log_prompt_response(user_email, prompt, response):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_email": user_email,
        "prompt": prompt,
        "response": response
    }
    log_file_path = os.path.join("data/logs", f"{user_email}_prompts_responses.yaml")
    with open(log_file_path, 'a') as file:
        yaml.dump([log_entry], file)

def info_box():
    st.sidebar.info("""
    **Sales Email Sequence Generator**
    - Author: Francis Brero
    - Code: [GitHub Repository](https://github.com/francisbrero/email_sequence)
    - Version: 1.6.22.2
    """)
