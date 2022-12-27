#librerias web scraping
from os import remove
import os, ssl
import urllib.request
from bs4 import BeautifulSoup
import time

from PyQt5.QtCore import *

class Retiver(QThread):
    RetrivingResult_Progress = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.STR_Title=""
        self.EnsambleMensaje=""

    def setUrlToRetrive(self,Url):
        self.url=Url
    
    def to_retrive(self):
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        
        data = urllib.request.urlopen(self.url).read().decode('Latin-1')#Diferentes medios de codificacion
        
        soup =  BeautifulSoup(data,"html.parser")
        
        ### Getting section where Title and text body is
        
        #Titulo y cuerpo
        title = soup.body.h3
        sentences= soup.body.p
        
        ### Extracting Title and sentences
        
        STR_Sentences=[]
        stringsentence=""
        ## 
        self.STR_Title=str(title.get_text('h3'))
        for i in sentences:
            #### there were two types lines not only the senteces, here is filtered the bs4.element.Tag (the sentences)
            if str(type(i)) == "<class 'bs4.element.Tag'>":
                ### there were a carecter unexpected (\xa0) it's taken off 
                if str(i.get_text('p')) != '\xa0':
                    stringsentence=str(i.get_text('p'))
                    stringsentence.replace('\xa0',"",100)
                    STR_Sentences.append(stringsentence)

        ## The messsage all sentences are joined
        for j in STR_Sentences:
            self.EnsambleMensaje=self.EnsambleMensaje+"\n"
            self.EnsambleMensaje=self.EnsambleMensaje+j
            
        self.RetrivingResult_Progress.emit(1)
        time.sleep(2)
        #self.RetrivingResult_Progress.emit(0)
    
    def getTitleandBodyNote(self):
        return self.STR_Title,self.EnsambleMensaje,self.url
    
    def run(self):
        self.RetrivingResult_Progress.emit(0)
        self.to_retrive()