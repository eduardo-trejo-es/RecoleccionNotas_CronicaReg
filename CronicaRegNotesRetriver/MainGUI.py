# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/QTdesiner/GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import json
### own created classes
from Google_API_Credential import Loging_Google_API
from GmailAPI import Mailing

from Process import Process
from Note_Retiver import Retiver
#borrar capeta
from os import remove



class Ui_CronicaRegNotesRetriver(object):
    def __init__(self):
        ####  App Instances 
            ## Instances init
        
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/appConfig.json", "r") as read_file:
            self.data = json.load(read_file)
        self.GoogleClientAPI = Loging_Google_API()
        self.GmailMailling_Suggestions = Mailing(self.data["MailFrom"])
        self.GmailMailling_Notes_sender = Mailing(self.data["MailFrom"])

        self.process = Process()
        self.notes_retriver = Retiver()
        
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/VerifyNotes.json", "r") as read_file:
            self.verifyNotesDict = json.load(read_file)
        
        
        ## global var init
        self.BarProgresVar=0
        self.resulta_suggestSent=0
        self.RetrivingState=0
        self.CountPressSenNo_PB_Clear=0
        self.emptyDict={}
        
    
    def setupUi(self, CronicaRegNotesRetriver):
        CronicaRegNotesRetriver.setObjectName("CronicaRegNotesRetriver")
        CronicaRegNotesRetriver.resize(605, 399)
        self.centralwidget = QtWidgets.QWidget(CronicaRegNotesRetriver)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 591, 351))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setIconSize(QtCore.QSize(40, 40))
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.TabMailConf = QtWidgets.QWidget()
        self.TabMailConf.setObjectName("TabMailConf")
        self.label = QtWidgets.QLabel(self.TabMailConf)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.TabMailConf)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 171, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.TabMailConf)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 171, 21))
        self.label_3.setObjectName("label_3")
        self.APIConf_PB_Apply = QtWidgets.QPushButton(self.TabMailConf)
        self.APIConf_PB_Apply.setGeometry(QtCore.QRect(450, 290, 131, 32))
        self.APIConf_PB_Apply.setObjectName("APIConf_PB_Apply")
        self.APIConf_LEdit_CredPath = QtWidgets.QLineEdit(self.TabMailConf)
        self.APIConf_LEdit_CredPath.setGeometry(QtCore.QRect(20, 40, 311, 21))
        self.APIConf_LEdit_CredPath.setObjectName("APIConf_LEdit_CredPath")
        self.APIConf_LEdit_AddFrom = QtWidgets.QLineEdit(self.TabMailConf)
        self.APIConf_LEdit_AddFrom.setGeometry(QtCore.QRect(20, 90, 311, 21))
        self.APIConf_LEdit_AddFrom.setObjectName("APIConf_LEdit_AddFrom")
        self.APIConf_LEdit_AddTo = QtWidgets.QLineEdit(self.TabMailConf)
        self.APIConf_LEdit_AddTo.setGeometry(QtCore.QRect(20, 143, 311, 21))
        self.APIConf_LEdit_AddTo.setObjectName("APIConf_LEdit_AddTo")
        self.APIConf_PB_Log = QtWidgets.QPushButton(self.TabMailConf)
        self.APIConf_PB_Log.setGeometry(QtCore.QRect(360, 50, 231, 51))
        self.APIConf_PB_Log.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.APIConf_PB_Log.setAutoRepeatDelay(300)
        self.APIConf_PB_Log.setObjectName("APIConf_PB_Log")
        self.label_5 = QtWidgets.QLabel(self.TabMailConf)
        self.label_5.setGeometry(QtCore.QRect(368, 56, 40, 38))
        self.label_5.setText("")
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setPixmap(QtGui.QPixmap("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/QTdesiner/GoogleBTNLOGO.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.APIConf_LB_State = QtWidgets.QLabel(self.TabMailConf)
        self.APIConf_LB_State.setGeometry(QtCore.QRect(295, 100, 290, 20))
        self.APIConf_LB_State.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.APIConf_LB_State.setObjectName("APIConf_LB_State")
        self.tabWidget.addTab(self.TabMailConf, "")
        self.TabSendNotes = QtWidgets.QWidget()
        self.TabSendNotes.setObjectName("TabSendNotes")
        self.SenNo_PB_Verify = QtWidgets.QPushButton(self.TabSendNotes)
        self.SenNo_PB_Verify.setGeometry(QtCore.QRect(240, 250, 113, 32))
        self.SenNo_PB_Verify.setObjectName("SenNo_PB_Verify")
        self.SenNo_PB_Send = QtWidgets.QPushButton(self.TabSendNotes)
        self.SenNo_PB_Send.setGeometry(QtCore.QRect(420, 250, 113, 32))
        self.SenNo_PB_Send.setObjectName("SenNo_PB_Send")
        self.SenNo_PB_Clear = QtWidgets.QPushButton(self.TabSendNotes)
        self.SenNo_PB_Clear.setGeometry(QtCore.QRect(70, 250, 113, 32))
        self.SenNo_PB_Clear.setObjectName("SenNo_PB_Clear")
        self.SenNo_LEdit_Link = QtWidgets.QLineEdit(self.TabSendNotes)
        self.SenNo_LEdit_Link.setGeometry(QtCore.QRect(10, 40, 551, 21))
        self.SenNo_LEdit_Link.setObjectName("SenNo_LEdit_Link")
        self.label_4 = QtWidgets.QLabel(self.TabSendNotes)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 191, 16))
        self.label_4.setObjectName("label_4")
        self.SenNo_progressBar = QtWidgets.QProgressBar(self.TabSendNotes)
        self.SenNo_progressBar.setGeometry(QtCore.QRect(110, 300, 341, 31))
        self.SenNo_progressBar.setProperty("value", self.BarProgresVar)
        self.SenNo_progressBar.setObjectName("SenNo_progressBar")
        self.SenNo_LB_State = QtWidgets.QLabel(self.TabSendNotes)
        self.SenNo_LB_State.setGeometry(QtCore.QRect(110, 290, 271, 16))
        self.SenNo_LB_State.setObjectName("SenNo_LB_State")
        self.SenNo_TEdit_VerTitle = QtWidgets.QTextEdit(self.TabSendNotes)
        self.SenNo_TEdit_VerTitle.setGeometry(QtCore.QRect(10, 90, 551, 155))
        self.SenNo_TEdit_VerTitle.setObjectName("SenNo_TEdit_VerTitle")
        self.SenNo_TEdit_VerTitle.setDisabled(False)
        self.label_7 = QtWidgets.QLabel(self.TabSendNotes)
        self.label_7.setGeometry(QtCore.QRect(10, 70, 191, 16))
        self.label_7.setObjectName("label_7")
        self.tabWidget.addTab(self.TabSendNotes, "")
        self.TabAppComments = QtWidgets.QWidget()
        self.TabAppComments.setObjectName("TabAppComments")
        self.AppCom_TEdit_body = QtWidgets.QTextEdit(self.TabAppComments)
        self.AppCom_TEdit_body.setGeometry(QtCore.QRect(20, 80, 541, 201))
        self.AppCom_TEdit_body.setObjectName("AppCom_TEdit_body")
        self.AppCom_LEdit_Title = QtWidgets.QLineEdit(self.TabAppComments)
        self.AppCom_LEdit_Title.setGeometry(QtCore.QRect(20, 40, 541, 21))
        self.AppCom_LEdit_Title.setText("")
        self.AppCom_LEdit_Title.setObjectName("AppCom_LEdit_Title")
        self.AppCom_PB_Submit = QtWidgets.QPushButton(self.TabAppComments)
        self.AppCom_PB_Submit.setGeometry(QtCore.QRect(450, 290, 113, 32))
        self.AppCom_PB_Submit.setObjectName("AppCom_PB_Submit")
        self.label_6 = QtWidgets.QLabel(self.TabAppComments)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 221, 16))
        self.label_6.setObjectName("label_6")
        self.AppCom_PB_Clear = QtWidgets.QPushButton(self.TabAppComments)
        self.AppCom_PB_Clear.setGeometry(QtCore.QRect(330, 290, 113, 32))
        self.AppCom_PB_Clear.setObjectName("AppCom_PB_Clear")
        self.SenNo_LB_State_2 = QtWidgets.QLabel(self.TabAppComments)
        self.SenNo_LB_State_2.setGeometry(QtCore.QRect(20, 290, 271, 16))
        self.SenNo_LB_State_2.setObjectName("SenNo_LB_State_2")
        self.tabWidget.addTab(self.TabAppComments, "")
        CronicaRegNotesRetriver.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CronicaRegNotesRetriver)
        self.statusbar.setObjectName("statusbar")
        CronicaRegNotesRetriver.setStatusBar(self.statusbar)

        self.retranslateUi(CronicaRegNotesRetriver)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CronicaRegNotesRetriver)
        
        #--------- thread emit signals -----------
        self.notes_retriver.Update_Progress.connect(self.Event_UpdateProgress_SP)
        self.GmailMailling_Suggestions.SendingResult_Progress.connect(self.Event_ResultaSendingSuggest)
        self.notes_retriver.RetrivingResult_Progress.connect(self.Event_RetrivingNote)
        self.notes_retriver.ReadyToSend_Progress.connect(self.SentNoteMail)
        self.notes_retriver.Update_Progress_String.connect(self.Event_UpdateProgress_string)
        
        #####  Buttons calls #####
    
            ### Tab API Conf  
        self.APIConf_PB_Log.clicked.connect(self.API_Log)
        self.APIConf_PB_Apply.clicked.connect(self.ApplyConfig)
        
            ### TabSendNotes
        self.SenNo_PB_Clear.clicked.connect(self.SenNo_Clear)
        self.SenNo_PB_Verify.clicked.connect(self.SenNo_Verify)
        self.SenNo_PB_Send.clicked.connect(self.SenNo_Send)
        
            ### TabAppComments
        self.AppCom_PB_Clear.clicked.connect(self.AppCom_Clear)
        self.AppCom_PB_Submit.clicked.connect(self.AppCom_Submit)

    def retranslateUi(self, CronicaRegNotesRetriver):
        _translate = QtCore.QCoreApplication.translate
        CronicaRegNotesRetriver.setWindowTitle(_translate("CronicaRegNotesRetriver", "CronicaRegNotesRetriver"))
        self.label.setText(_translate("CronicaRegNotesRetriver", "Credentials Path"))
        self.label_2.setText(_translate("CronicaRegNotesRetriver", "Address mail from"))
        self.label_3.setText(_translate("CronicaRegNotesRetriver", "Address mail to"))
        self.APIConf_PB_Apply.setText(_translate("CronicaRegNotesRetriver", "Apply changes"))
        self.APIConf_PB_Log.setText(_translate("CronicaRegNotesRetriver", "Log-In With google"))
        if self.data["Veryfication"] == 1 :
            self.APIConf_LB_State.setGeometry(QtCore.QRect(465, 100, 120, 20))
            self.APIConf_LB_State.setStyleSheet("background-color: lightgreen")
            self.APIConf_LB_State.setText(_translate("CronicaRegNotesRetriver", "Succesfully verified"))
            self.APIConf_PB_Log.setDisabled(True)
        else:
            self.APIConf_LB_State.setStyleSheet("background-color: none")
            self.APIConf_LB_State.setText(_translate("CronicaRegNotesRetriver", "Need to verify"))
            self.APIConf_PB_Log.setDisabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabMailConf), _translate("CronicaRegNotesRetriver", "API/Gmail config"))
        self.SenNo_PB_Verify.setText(_translate("CronicaRegNotesRetriver", "Verify"))
        self.SenNo_PB_Send.setText(_translate("CronicaRegNotesRetriver", "Send"))
        self.SenNo_PB_Clear.setText(_translate("CronicaRegNotesRetriver", "Clear"))
        self.label_4.setText(_translate("CronicaRegNotesRetriver", "Link to get its note"))
        self.SenNo_LB_State.setText(_translate("CronicaRegNotesRetriver", "Ready to get notes"))
        self.label_7.setText(_translate("CronicaRegNotesRetriver", "Verify note title to be send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabSendNotes), _translate("CronicaRegNotesRetriver", "Sending notes"))
        self.AppCom_TEdit_body.setHtml(_translate("CronicaRegNotesRetriver", "Send a comment to developper"))
        self.AppCom_PB_Submit.setText(_translate("CronicaRegNotesRetriver", "Submit"))
        self.label_6.setText(_translate("CronicaRegNotesRetriver", "Improvement name"))
        self.AppCom_PB_Clear.setText(_translate("CronicaRegNotesRetriver", "Clear"))
        self.SenNo_LB_State_2.setText(_translate("CronicaRegNotesRetriver", "Ready to send comment"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabAppComments), _translate("CronicaRegNotesRetriver", "App comments"))
        self.UpdateObjectsTabAPI()
        if self.data["Veryfication"] == 1:
            self.API_Log()
        else:
            pass

    #####  Buttons  def #####
    
        ### Tab API Conf
        
    def API_Log(self):
        #print("pressed")
        ## Authenticate app and PC to be able to use Google API
        self.APIConf_LB_State.setText("trying to verify...")
        self.Service = self.GoogleClientAPI.gmail_authenticate("CronicaRegNotesRetriver/GoogleAPI_Credentials/credentials.json")
        try:
            #####    this process most be a threaded
            self.Service = self.GoogleClientAPI.gmail_authenticate("CronicaRegNotesRetriver/GoogleAPI_Credentials/credentials.json")
            #####    this process most be a threaded
            #condition missing when Service get the valid value
            #print(self.Service)
            self.LB_State_faces(1)
        except:
            self.LB_State_faces(0)
    
    def ApplyConfig(self):
        #Update credentials path
        self.update_AppConfigJson("CredentialPath",str(self.APIConf_LEdit_CredPath.text()))
        #Update Mail from
        self.update_AppConfigJson("MailFrom",str(self.APIConf_LEdit_AddFrom.text()))
        #Update Mail to
        self.update_AppConfigJson("MailTo",str(self.APIConf_LEdit_AddTo.text()))
        self.UpdateObjectsTabAPI()
        ### TabSendNotes
        
    def SenNo_Clear(self):
        self.SenNo_LEdit_Link.setText("")
        self.CountPressSenNo_PB_Clear=self.CountPressSenNo_PB_Clear+1
        #print(self.CountPressSenNo_PB_Clear)
        if self.CountPressSenNo_PB_Clear>=3 :
            self.emptyDict={}
            ## Borrar imagenes de carpeta
            with open("CronicaRegNotesRetriver/json/Images.json", "r") as read_file:
                data = json.load(read_file)
                #print(data)
                #print(len(data))
            for i in data.keys():
                #print(i)
                for j in data[i]:
                    #print(j)
                    try:
                        remove(j)
                    except:
                        print("was not possible to delete imaged automatically")
                        
                    
            self.ModifItems_VerifyNotesJson(self.emptyDict)
            self.ModifItems_Imagesjson(self.emptyDict)
            
            self.verifyNotesDict=self.emptyDict
            self.ShowNotesAddToDict()
            self.CountPressSenNo_PB_Clear=0
            
        
    def SenNo_Verify(self):
        self.CountPressSenNo_PB_Clear=0
        self.notes_retriver.setUrlToRetrive(str(self.SenNo_LEdit_Link.text()))
        self.notes_retriver.start()
        
        
    def toVerifyTitleandBodyNote(self):
        Title,body,url=self.notes_retriver.getTitleandBodyNote()
        self.verifyNotesDict[Title]=url
        self.ModifItems_VerifyNotesJson(self.verifyNotesDict)    
        self.ShowNotesAddToDict()
    
    def ShowNotesAddToDict(self):
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/VerifyNotes.json", "r") as read_file:
            data = json.load(read_file)
        keys=""
        onlyfirst=True
        for i in data.keys():
            if onlyfirst:
                keys="*- "+i+"\n"
                onlyfirst=False
            else:
                keys=keys+"*- "+i+"\n"
        self.SenNo_TEdit_VerTitle.setPlainText(keys)
    
    def SenNo_Send(self):
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/VerifyNotes.json", "r") as read_file:
            data = json.load(read_file)
        self.notes_retriver.TitleAndbodyNoteSend(data,True)
        self.notes_retriver.start()
    
    def SentNoteMail(self):
        with open("CronicaRegNotesRetriver/json/Images.json", "r") as read_file:
            data = json.load(read_file)
        
        Service=self.Service
        mail_to= str(self.APIConf_LEdit_AddTo.text())
        mail_obj,mail_body,url = self.notes_retriver.getTitleandBodyNote()
        imeges_attached=data[mail_obj]
        #print("image attached "+ str(imeges_attached))
        self.GmailMailling_Notes_sender.SetValues(Service, mail_to, mail_obj, mail_body, imeges_attached)
        self.GmailMailling_Notes_sender.start()
        #Can I get a real mail sending confirmation this will be a pull request
        self.notes_retriver.MailSentState(1)
        
        
        ### TabAppComments
    
    def AppCom_Clear(self):
        self.AppCom_LEdit_Title.setText("")
        self.AppCom_TEdit_body.setText("")
    
    def AppCom_Submit(self):
        imeges_attached=[]
        Service=self.Service
        mail_to= "notas.automaticas@gmail.com"
        mail_obj = "App suggestion "+ str(self.AppCom_LEdit_Title.text())
        mail_body = str(self.AppCom_TEdit_body.toPlainText())
        self.GmailMailling_Suggestions.SetValues(Service, mail_to, mail_obj, mail_body, imeges_attached)
        self.GmailMailling_Suggestions.start()
        
    #### General functions
    
        ###### Update appConfig json file
    def update_AppConfigJson(self,param,new_value):
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/appConfig.json", "r") as read_file:
            data = json.load(read_file) 
        data[param]=new_value
            
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/appConfig.json", "w",encoding='utf-8') as write_file:
            json.dump(data, write_file, ensure_ascii=False)
    
    def ModifItems_VerifyNotesJson(self,dict):
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/VerifyNotes.json", "w", encoding='utf-8') as write_file:
            #print(dict)
            json.dump(dict, write_file, ensure_ascii=False)
    
    def ModifItems_Imagesjson(self,dict):
        with open("CronicaRegNotesRetriver/json/Images.json", "w", encoding='utf-8') as write_file:
            #print(dict)
            json.dump(dict, write_file, ensure_ascii=False)
    

    def LB_State_faces(self, NumFace):
        if NumFace == 1:
            self.APIConf_LB_State.setGeometry(QtCore.QRect(465, 100, 120, 20))
            self.APIConf_LB_State.setStyleSheet("background-color: lightgreen")
            self.APIConf_LB_State.setText("Succesfully verified")
            self.update_AppConfigJson("Veryfication",1)
            self.APIConf_PB_Log.setDisabled(True)
        elif NumFace == 0 :
            self.APIConf_LB_State.setGeometry(QtCore.QRect(385, 100, 200, 20))
            self.APIConf_LB_State.setStyleSheet("background-color: red")
            self.APIConf_LB_State.setText("Can't verify,  not com with server")
            self.update_AppConfigJson("Veryfication",0)
            self.APIConf_PB_Log.setDisabled(False)
    
    ##### Updated objects GUI
    
        ### Tab API Conf  
    def UpdateObjectsTabAPI(self):
        with open("/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/json/appConfig.json", "r") as read_file:
            data = json.load(read_file)
        self.APIConf_LEdit_CredPath.setText(data["CredentialPath"])
        self.APIConf_LEdit_AddFrom.setText(data["MailFrom"])
        self.APIConf_LEdit_AddTo.setText(data["MailTo"])
            
        
        ### TabSendNotes
    def UpdateObjectsTabSendNotes(self):
        self.SenNo_progressBar.setProperty("value",self.BarProgresVar)
        #print('called')
        
        ### TabAppComments
        
    ##### Emit thread signals
    
        ### Update appConfig json file
        
        ### TabSendNotes
    def Event_UpdateProgress_SP(self, val):
        if val<=100:
            self.BarProgresVar =val
        else:
            self.BarProgresVar =100
        
        self.UpdateObjectsTabSendNotes()    
    
    def Event_UpdateProgress_string(self,val):
        self.SenNo_LB_State.setText(val)
        
        ### TabAppComments
        
    def Event_ResultaSendingSuggest(self, val):
        self.resulta_suggestSent=val
        if self.resulta_suggestSent == 0:
            self.SenNo_LB_State_2.setText("Ready to send comment")
        elif self.resulta_suggestSent == 1:
            self.SenNo_LB_State_2.setText("Message succesfully sent")
        elif self.resulta_suggestSent == 2:
            self.SenNo_LB_State_2.setText("Error, message not sent")
           
    def Event_RetrivingNote(self, val):
        #0 not done
        #1 retriving done
        self.RetrivingState=val
        if self.RetrivingState == 1:
            self.toVerifyTitleandBodyNote()
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CronicaRegNotesRetriver = QtWidgets.QMainWindow()
    ui = Ui_CronicaRegNotesRetriver()
    ui.setupUi(CronicaRegNotesRetriver)
    CronicaRegNotesRetriver.show()
    sys.exit(app.exec_())
