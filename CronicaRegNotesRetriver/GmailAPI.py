# -*- coding: utf-8 -*-

#librerias para enviar correo
import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from PyQt5.QtCore import *
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

import time


class Mailing(QThread):
    SendingResult_Progress = pyqtSignal(int)
    
    def __init__(self,OURMAIL):
        super().__init__()
        self.our_email=OURMAIL
        
    def SetValues(self,Service, Destination, Obj, Body, Attachments):
        self.service = Service
        self.destination = Destination
        self.obj = Obj
        self.body = Body
        self.attachments = Attachments

    # Adds the attachment with the given filename to the given message
    def add_attachment(self,message, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            #fp = open(filename, 'rb',encoding="utf-8")
            print("Gmail______1"+str(filename))
            fp = open(filename, "rb")
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        print("Gmail______2"+str(filename))
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)
        
        
    def build_message(self,destination, obj, body, attachments=[]):
        if not attachments: # no attachments given
            message = MIMEText(body)
            message['to'] = destination
            message['from'] = self.our_email
            message['subject'] = obj
        else:
            message = MIMEMultipart()
            message['to'] = destination
            message['from'] = self.our_email
            message['subject'] = obj
            message.attach(MIMEText(body))
            for filename in attachments:
                self.add_attachment(message, filename)
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    
    def send_message(self,service, destination, obj, body, attachments=[]):
        return service.users().messages().send(userId="me",body=self.build_message(destination, obj, body, attachments)).execute()
    
    def run(self):
        self.send_message(self.service, self.destination, self.obj, self.body, self.attachments)
        try:
            #self.send_message(self.service, self.destination, self.obj, self.body, self.attachments)
            print("mail sent")
            self.SendingResult_Progress.emit(1)
        except:
            print("problem mailing")
            self.SendingResult_Progress.emit(2)
        time.sleep(3)
        self.SendingResult_Progress.emit(0)