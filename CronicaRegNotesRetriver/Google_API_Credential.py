#librerias para enviar correo
import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type


class Loging_Google_API():
    def __init__(self):
        # Request all access (permission to read/send/receive emails, manage the inbox, and more)
        self.SCOPES = ['https://mail.google.com/']
        self.our_email = 'notas.automaticas@gmail.com'
        self.Token_Pickle="CronicaRegNotesRetriver/GoogleAPI_Credentials/token.pickle"

    def gmail_authenticate(self,Credential_Path):
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists(self.Token_Pickle):
            with open(self.Token_Pickle, "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(Credential_Path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open(self.Token_Pickle, "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)