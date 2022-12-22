# -*- coding: utf-8 -*-

# send_attachment.py
# import necessary packages
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


# create message object instance
msg = MIMEMultipart()
 
message = "que pedopapu "

# setup the parameters of the message
password = "qwerTyui1"
msg['From'] = "notas.automaticas@gmail.com"
msg['To'] = "notas.automaticas@gmail.com"
msg['Subject'] = "Preuba Photos y mensaje"
 
# attach image to message body
fp = open("imagenes/paisaje_prueba.jpg", 'rb')
image = MIMEImage(fp.read())
fp.close()
msg.attach(image)
#msg.attach(MIMEImage(("imagenes/paisaje_prueba.jpg").read()))
##### Parte Agregada 
# add in the message body
msg.attach(MIMEText(message, 'plain')) 

# create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print("El correo fue enviadó exitosamente a %s:" % (msg['To']))