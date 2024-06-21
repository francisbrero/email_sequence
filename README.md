# Streamlit PMM Extractor and Sequence Generator

This Streamlit application allows users to extract Product Marketing Messages (PMM) and generate sales email sequences for products based on website data and playbook information.

## Features

- **PMM Extractor**: Extract and edit website messaging, personas, and differentiators.
- **Sequence Generator**: Generate and edit email sequences using OpenAI GPT-4 Turbo based on selected playbooks.

## Prerequisites

- Python 3.10+
- pip (Python package installer)

## Setup

### 1. Clone the Repository

```sh
git clone git@github.com:francisbrero/email_sequence.git
cd email_sequence
```

2. Create and Activate a Virtual Environment

```sh
python3 -m venv venv
source venv/bin/activate
```

3. Install Requirements

```sh
pip install -r requirements.txt
```

4. Set Up Environment Variables

Create a .env file in the root directory of the project and add your OpenAI API key:

```text
OPENAI_API_KEY=your_openai_api_key
```

5. Run the Streamlit App

```sh
streamlit run main.py
```

### File Structure

```plaintext
streamlit_app/
    ├── data/
    │   ├── websites/
    │   │   └── website1.yaml
    │   │   └── website2.yaml
    │   ├── sequences/
    │   │   └── sequence1.yaml
    │   │   └── sequence2.yaml
    │   ├── playbooks/
    │   │   └── playbook1.yaml
    │   │   └── playbook2.yaml
    ├── pages/
    │   ├── pmm_extractor.py
    │   └── sequence_generator.py
    ├── prompts/
    │   ├── generate_sequence_prompt.txt
    │   └── pmm_extractor_prompt.txt
    ├── main.py
    ├── utils.py
    ├── .env
    ├── requirements.txt
    ├── README.md
```

## Usage

### PMM Extractor

Select a website from the dropdown.
View and edit the messaging, personas, and differentiators.
Click the "Save" button to save changes.

### Sequence Generator

Select a playbook from the dropdown.
View and edit the playbook title, description, and conditions.
Click the "Save and Generate" button to generate a sequence.
Edit the generated sequence steps.
Click the "Save" button to save the sequence.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the MIT License.
