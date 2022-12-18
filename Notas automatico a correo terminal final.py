# -*- coding: utf-8 -*-
import random

#Libreria random

#librerias web scraping
from os import remove
import os, ssl
import urllib.request
from bs4 import BeautifulSoup

#librerias para descargar y guardar imagenes
    #Para hacerlo sin certificaciones
import os, ssl
    #Descargar imagen
import requests
    #Mover archivos de ubicación
import shutil

#librerias para enviar correo
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

#variables web scraping
#link donde se encuentra la nota
url='https://www.queretaro.gob.mx/prensa/contenido.aspx?q=vUYGbsxLnljEIK42BbZlQ0+l8jDVq69PyrYjaUyZ2NTYQ4HUMPRgZA=='
#Variables descargar imagenes

carpertaImg="imagenes/"

#Variables de correo



#Permite ignorar las certificaciones, esto lo hace inceguro, pero no es relevante ya que tomamos notas de un dominio publico
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context



#Extraccion de codigo fuente de la pagina
datos = urllib.request.urlopen(url).read().decode('Latin-1')
soup =  BeautifulSoup(datos)
 

# Buscar los componentes solicitados, titulo y cuerpo con etiqueta y classe

#https://www.queretaro.gob.mx/prensa/
text = soup.find_all('div', class_="col-md-12")

#https://fiscaliageneralqro.gob.mx/      
#text = soup.find_all('div', class_="entry-content clearfix")

lineas=list()

for i in text:
    lineas.append(i.text)

extracto=str(lineas[0])


#inicios del formato

    #Tomar titulo
Titulo=""
i=0
UltimoSaltoTitulo=0

while True:
    if  not(extracto[i] == '\n'):
        Titulo=Titulo+extracto[i]
        #print(Titulo)
    elif extracto[i] == '\n' and i>=5:
        #print("salio aqui")
        UltimoSaltoTitulo=i
        break
    i=i+1
#print(Titulo)

NumSalto=0

#Tomar cuerpo
#contar \n , 
for i in range(0,len(extracto)):
    if extracto[i] == '\n':
        NumSalto=NumSalto+1
        LugarSaltoMax=i
        #print(NumSalto)
#Lugar \n ante ante penultimo

NumSaltoAnte=0
MenosUltimosSaltos=5 #Determinar cuando ultimas lineas de texto no seran tomada en cuenta
for i in range(0,len(extracto)):
    if extracto[i] == '\n':
        NumSaltoAnte=NumSaltoAnte+1
        if NumSaltoAnte == (NumSalto-MenosUltimosSaltos):
            LugarSaloAnteAnte=i

#Tomar cuerpo, salvo las ultimas lineas o saltos de linea
cuerpo=extracto[UltimoSaltoTitulo:LugarSaloAnteAnte]
#print(cuerpo)

#Formato de mensaje
TituloEntreCuerpo=":ExcerptStart"+"\n"+Titulo+"\n"+":ExcerptEnd"
LineasFinaleMensaje="#img1 caption="+"'"+Titulo+"'"+"#"
  #linea depues del titulo


#Ensamble de mensaje
EnsambleMensaje=Titulo+"\n"+TituloEntreCuerpo+"\n"+cuerpo+"\n"+"\n"+LineasFinaleMensaje

#print(EnsambleMensaje)

######################################
#      Links y descargar imagenes    #
######################################

# Buscar los componentes solicitados, links imagenes con etiqueta y classe
links_imagenes = soup.find_all('img', class_="media-object")
extracto_imagenes=str(links_imagenes)
#print("extracto_imag= "+extracto_imagenes)
longitudlinks_imagenes=len(links_imagenes)
longitudLinks=len(extracto_imagenes)

#print("Tamaño total link: "+str(longitudLinks))

links=[]
posiC=[]
siS=False
siR=False
siC=False
siInclinado=False
siMayorQ=False
iniLink=0
finLink=0
Filtroextracto_imagen=""
soloImpares=0

#print(extracto_imagenes[2])
#posicion encuentra inicio y final de link
#print(links_imagenes[2])

for a in range(0,longitudLinks-1):
    if extracto_imagenes[a] == "s":
        siS=True
    elif extracto_imagenes[a] == "r" and  siS==True:
        siR=True
    else:
        siS=False

    if extracto_imagenes[a] == "c" and siR==True:
        #print("vi una r y paso una s y ahora hay una c")
        siC=True
    elif extracto_imagenes[a] == "=" and siC==True:
        iniLink=a+1
        siS=False
        siR=False
        siC=False
    else: 
        pass

    if extracto_imagenes[a] == "/":
        siInclinado=True
    elif extracto_imagenes[a] == ">" and siInclinado==True:
        siMayorQ=True
        finLink=a-1
        
    if iniLink > 0 and finLink>0:
        
        #print(str(soloImpares%2))
        if (soloImpares%2)==1: #solo queremos los links numeros impares
            Filtroextracto_imagen=extracto_imagenes[iniLink:finLink]
            Filtroextracto_imagen=Filtroextracto_imagen.replace("\"","")
            links.append(Filtroextracto_imagen.replace("amp;",""))
        else:
            pass
        soloImpares=soloImpares+1
        #print("SOlo imperes: "+ str(soloImpares))
        iniLink=0 
        finLink=0
#Revolver lista para descargar imagenes al azar
random.shuffle(links)
#print("Numero de links: "+str(len(links)))

#Solo tener max 3 links de fotos
if len(links)>3:
    links.pop(3,)

"""for i in links:
    print("\n cada link: "+str(i))"""

#Descargar 

for i in range(0,len(links)):
    url_imagen = links[i] # El link de la imagen
    nombre_local_imagen = Titulo+" "+str(i)+".jpg" # El nombre con el que queremos guardarla
    imagen = requests.get(url_imagen, verify=False).content
    with open(nombre_local_imagen, 'wb') as handler:
	    handler.write(imagen)

    #Mover imagen a la ubicación correcta
    # Mueve el archivo desde la ubicación actual a la
    # carpeta "Documentos".
    shutil.move(nombre_local_imagen, "imagenes/")


######################################
#       Enviar correo con imagen     #
######################################

# Crear instacia de objeto de mensaje
msg = MIMEMultipart()
 
#Aqui va el mensaje anteriormente armado
message = EnsambleMensaje

# setup the parameters of the message
password = "qwerTyui1"
msg['From'] = "notas.automaticas@gmail.com"
msg['To'] = "notas.automaticas@gmail.com"
msg['Subject'] = Titulo


# attach image to message body
for i in range(0,len(links)):
    fp = open(carpertaImg+Titulo+" "+str(i)+".jpg", 'rb')
    image = MIMEImage(fp.read())
    fp.close()
    msg.attach(image)
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


#Una vez enviado el correo se eliminan las fotos

for i in range(0,len(links)):  
    remove(carpertaImg+Titulo+" "+str(i)+".jpg")