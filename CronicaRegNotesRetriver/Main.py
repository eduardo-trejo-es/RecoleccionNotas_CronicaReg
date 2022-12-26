
from Google_API_Credential import Loging_Google_API
from GmailAPI import Mailing


## Instances init
GoogleClientAPI = Loging_Google_API()
GmailMailling = Mailing("notas.automaticas@gmail.com")



## Authenticate app and PC to be able to use Google API
Service = GoogleClientAPI.gmail_authenticate("CronicaRegNotesRetriver/GoogleAPI_Credentials/credentials.json")




imeges_attached=["/Users/eduardo/Desktop/RecoleccionNotas_CronicaReg/CronicaRegNotesRetriver/Images/Titular de SEDESU presenta avances en agenda ambiental0.jpg"]
mail_to= "paginalalo9@gmail.com"
mail_obj = "Titulo de nota"
mail_body = " messages automatique de part de lalo !!! Dounia est la plus belle ¡¡¡¡"


GmailMailling.send_message(Service, mail_to, mail_obj, mail_body, imeges_attached)