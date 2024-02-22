import os.path,pickle,re,base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from Database import Email,Session
from Datas import Datas

class GmailAPI:
    def __init__(self, token_file="../config/token.pickle", credentials_file="../config/client_secret.json"):
        self.token_file = token_file
        self.credentials_file = credentials_file
        self.credentials = None
        self.service = None
    
    """ Gmail authentication function """
    def authenticate(self, scopes):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, scopes)
                self.credentials = flow.run_local_server(port=0)
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.credentials, token)

        self.service = build('gmail', 'v1', credentials=self.credentials)
    
    """ Fetching the emails from Email API """
    def fetch_emails(self, maxResults=100, fltrEmailsFrom=[]):
        try:
            results = self.service.users().messages().list(maxResults=maxResults, userId='me', labelIds=fltrEmailsFrom).execute()
            messages = results.get('messages', [])
            
            if not messages:
                print('No emails found.')
            else:
                for message in messages:
                    email_dicts = {}
                    email_obj = self.service.users().messages().get(userId='me', id=message['id']).execute()
                    
                    _emailLables = email_obj['labelIds']
                    _payloads = email_obj['payload']
                    email_dicts['mail_thread_id'] = message['id']
                    email_dicts['status'] = 'U' if 'UNREAD' in _emailLables else 'R'
                    
                    payload_headers = email_obj["payload"]["headers"] if email_obj["payload"]["headers"] else []
                    for eachData in payload_headers:
                        if eachData['name'] == 'Subject':
                            email_dicts['subject'] = eachData['value']
                        if eachData['name'] == 'From':
                            email_dicts['sender'] = re.search(r'[\w\.-]+@[\w\.-]+', eachData['value']).group() if re.search(r'[\w\.-]+@[\w\.-]+', eachData['value']) else None
                        if eachData['name'] == 'Date':
                            email_dicts['mail_rec_time'] = Datas.formatting_datetime_values(eachData['value'])
                    
                    """
                        The Body of the message is in Encrypted format.
                        Read the data & decode it with base 64 decoder.
                    """
                    # parts = _payloads.get('parts')[0] if _payloads.get('parts') else _payloads
                    
                    # decoded_data = None
                    # _data = parts['body']['data'] if parts else None
                    # if _data is not None:
                    #     _data = _data.replace("-","+").replace("_","/") 
                    #     decoded_data = base64.urlsafe_b64decode(_data.encode('UTF-8')).decode('utf-8')

                    # email_dicts['body'] = decoded_data
                    email_dicts['body'] = "-"
                    
                    session = Session()
                    Email().insert_emails_db(session,email_dicts)
                    session.commit()
                    session.close()
        except (Exception) as e:
            print(f'GmailAPI -> fetch_emails_error -> {e}')
    
    def apply_actions(self, emails, actions):
        try:
            resp = None
            email_ids = [email[0] for email in emails]
                        
            for action in actions:
                """
                    If:     Action  ->  "Mark as"       ->  "Read"
                    elIf:   Action  ->  "Mark as"       ->  "Un Read"
                    elIf:   Action  ->  "Move Message"  ->  "As Important"
                """
                if(action["action"] == 'Mark as' and action["field"] == "READ"):
                    resp = self.service.users().messages().batchModify( userId='me', body={'ids': email_ids, 'removeLabelIds': ['UNREAD']}).execute()
                elif(action["action"] == 'Mark as' and action["field"] == "UNREAD"):
                    resp = self.service.users().messages().batchModify( userId='me', body={'ids': email_ids, 'addLabelIds': ['UNREAD']}).execute()
                elif(action["action"] == 'Move Message'):
                    resp = self.service.users().messages().batchModify( userId='me', body={'ids': email_ids, 'addLabelIds': [action["field"]]}).execute()
                
                print("---"*4)
                if resp=="":
                    print("Action performed successfully!!")
                    return True
                else:
                    print("Action failed! check the code..!")
                    print(f"Response -> {resp}")
                print("---"*4)
                return False
        except (Exception) as e:
            print(f' GmailAPI -> apply_actions error -> {e}')
            return False


if __name__ == "__main__":
    gmail_api = GmailAPI()
    gmail_api.authenticate(scopes=['https://www.googleapis.com/auth/gmail.readonly'])
    gmail_api.fetch_emails(maxResults=20, fltrEmailsFrom=['INBOX'])
