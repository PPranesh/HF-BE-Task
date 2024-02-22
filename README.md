# HF-BE-Task
Interview assesment repository for Happy Fox for Backend Engineer role

# Project Setup

## Installation Steps

### Google Auth

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

1. Create the DB schema and update the Database CREDS in the below mentioned file.

   ```bash
    python3 src/Database.py
    ```
3. Run the script to fetch emails:

    ```bash
    python3 src/GmailAPI.py
    ```

4. Edit the rules in the config/rules.json file.

5. Run the script to apply rules:
    ```bash
    python3 src/UpdateEmailsByRules.py
    ```
