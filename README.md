# HF-BE-Task
Interview assesment repository for Happy Fox for Backend Engineer role

# Project Setup

## Installation Steps

# Create a Virtual Environment

1. Install the `virtualenv` library using pip:

    ```bash
    pip3 install virtualenv
    ```

2. To use venv in your project, in your terminal, create a new project folder

    ```
    mkdir projectFolderName
    cd projectFolderName
    python3 -m venv <virtual-environment-name>
    ```

3. To Activate the Virtual Environment

    ```
    source <virtual-environment-name>/bin/activate
    ```
   

## Google Auth

1. Follow the [Google Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python) to setup OAuth for your account and download credentials file

2. Install the `google-auth` library using pip:

    ```bash
    pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

3. Make sure to download the Google client secret file (`client_secret.json`) and save it inside the `config` folder.

4. Install all required packages for the project using the below command.

	```bash
	pip3 install -r requirements.txt
	```

# Getting Started

1. Update the database credentials in the below mentioned file and create the database schema and rename the same.

   ```bash
    python3 src/Database.py
    ```
    
2. Run the script to fetch emails:

    ```bash
    python3 src/GmailAPI.py
    ```

3. Edit the rules in the below mentioned file.

   ```bash
    config/rules.json
    ```

5. You can find more sample rules in the below mentioned file.

   ```bash
    config/all_rules.txt
    ```

9. Run the script to apply rules:

    ```bash
    python3 src/UpdateEmailsByRules.py
    ```
