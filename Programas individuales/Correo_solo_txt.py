# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Thank you \n I cant belive it\n this is the thirt line\n and finaly the lats \n :D "
 
# setup the parameters of the message
password = "qwerTyui1"
msg['From'] = "notas.automaticas@gmail.com"
msg['To'] = "notas.automaticas@gmail.com"
msg['Subject'] = "Prueba"
 
# add in the message body
msg.attach(MIMEText(message, 'plain'))
 
#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print ("successfully sent email to %s:" % (msg['To']))