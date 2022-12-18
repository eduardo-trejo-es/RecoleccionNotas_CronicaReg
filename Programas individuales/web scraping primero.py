# -*- coding: utf-8 -*-
""" 
Este codigo toma el cuerpo de la nota y lo divide en 
"""
import os, ssl
import urllib.request
from bs4 import BeautifulSoup

"""class cuerpoText:
    def __init__(self):"""


#Permite ignorar las certificaciones, esto lo hace inceguro, pero no es relevante ya que tomamos notas de un dominio publico
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url='https://www.queretaro.gob.mx/prensa/contenido.aspx?q=vUYGbsxLnljEIK42BbZlQyep2qw7dza2WRiq1I1PeekymJHN11WB3A=='

#Extraccion de codigo fuente de la pagina
datos = urllib.request.urlopen(url).read().decode('Latin-1')
soup =  BeautifulSoup(datos)
 

# Buscar los componentes solicitados, con etiqueta y classe
text = soup.find_all('div', class_="col-md-12")

lineas=list()

for i in text:
    lineas.append(i.text)

extracto=str(lineas[0])


#Dar formato Formato

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

print(EnsambleMensaje)
