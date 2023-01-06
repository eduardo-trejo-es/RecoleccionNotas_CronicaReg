#librerias web scraping
from os import remove
import os, ssl
import urllib.request
from bs4 import BeautifulSoup
import time

# Downloading images
import random
import requests
    #Mover archivos de ubicación
import shutil
import json

from PyQt5.QtCore import *

class Retiver(QThread):
    RetrivingResult_Progress = pyqtSignal(int)
    ReadyToSend_Progress = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.STR_Title=""
        self.EnsambleMensaje=""
        self.toSend=False
        self.NotesDict={}
        self.SentState=0
        self.FrontMontant=0
        self.ImagesFolderPath="CronicaRegNotesRetriver/Images/"
        self.RetrivingAndDownloadingDone=False

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
        
        
        ## To downloadImages
        if self.toSend:
            links_imagenes = soup.find_all('img', class_="media-object")
            self.ImagesDownloader(self.STR_Title,links_imagenes)
            
        self.RetrivingResult_Progress.emit(1)
        
        self.RetrivingAndDownloadingDone=True
        
        #print(self.STR_Title)
        
        #########################################
        #     once get title and body need to be sent
        #      got to go outside to be sent
        time.sleep(2)
        #self.RetrivingResult_Progress.emit(0)
    
    def getTitleandBodyNote(self):
        return self.STR_Title,self.EnsambleMensaje,self.url
    
    def TitleAndbodyNoteSend(self,dict,tosend):
        self.toSend=tosend
        self.NotesDict=dict
    
    def ReadyToSend(self):
        self.ReadyToSend_Progress.emit(1)
        
    
    def MailSentState(self,state):
        self.SentState=state
      
    def ImagesDownloader(self,Note_title, Links_imagenes):
        note_title=Note_title
        links_imagenes=Links_imagenes
        
        linksLength_imagenes=len(links_imagenes)
        Images_links=[]
        for i in range(0,linksLength_imagenes-1):
            if not str(links_imagenes[i]["src"]).find("Ancho=0&Alto=0")==-1:
                print(links_imagenes[i]["src"])
            Images_links.append(links_imagenes[i]["src"])
        
        #Shuffle images link list
        random.shuffle(Images_links)

        #Filter only 3 or less images per note
        if len(Images_links)>2:
            Images_links.pop(3,)
        
        # Downloadig request
        #Descargar 
        ImagesPath=[]
        for i in range(0,len(Images_links)):
            url_imagen = Images_links[i] # El link de la imagen
            nombre_local_imagen = note_title+" "+str(i)+".jpg" # El nombre con el que queremos guardarla
            imagen = requests.get(url_imagen, verify=False).content
            with open(nombre_local_imagen, 'wb') as handler:
                handler.write(imagen)
            shutil.move(nombre_local_imagen, self.ImagesFolderPath)
            ImagesPath.append(self.ImagesFolderPath+nombre_local_imagen)
    
        self.UpdateImagesJson(note_title,ImagesPath)
    
    def UpdateImagesJson(self,Note_title, ImagesPath):
        with open("CronicaRegNotesRetriver/json/Images.json", "r") as read_file:
            data = json.load(read_file)
        data[Note_title]=ImagesPath 
            
        with open("CronicaRegNotesRetriver/json/Images.json", "w",encoding='utf-8') as write_file:
            json.dump(data, write_file, ensure_ascii=False)
    

        
    def run(self):
        self.RetrivingResult_Progress.emit(0)
        if self.toSend:
            self.RetrivingAndDownloadingDone=False
            print("been calling toSend")
            for i in self.NotesDict.keys():
                self.setUrlToRetrive(self.NotesDict[i])
                self.to_retrive()
                self.FrontMontant=0
                if self.RetrivingAndDownloadingDone==True:
                    while self.SentState==0:
                        if self.FrontMontant==0:
                            self.ReadyToSend()
                            self.FrontMontant=1
                    self.SentState=0
                    time.sleep(2)
                
            self.toSend=False
        else:
            self.to_retrive()