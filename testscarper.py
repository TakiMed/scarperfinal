from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
import pymongo
import json
from bs4 import BeautifulSoup
import requests
import urllib
import urllib.request
import re
from datetime import datetime



myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#myclient.drop_database("scarper")
mydb=myclient["scarper"]
apartman = mydb["Accommodation"]

for i in range(3):

    source = requests.get('https://www.realitica.com/?cur_page='+str(i)+'&for=Najam&pZpa=Crna+Gora&pState=Crna+Gora&type%5B%5D=Apartment&lng=hr').text
    soup = BeautifulSoup(source, 'lxml')
   

    for s in soup.find_all('div', class_='thumb_div'):
        ap = str(s.a)
        linkaa = ap.split('"')[1]
        #print(linkaa)
        theurl = linkaa
        thepage = urllib.request.urlopen(theurl) #pristupam stranici 1 apratmana
        soup1 = BeautifulSoup(thepage, 'lxml')


        #NASLOV
        naslov = soup1.h2.text

        #OGLASIO
        oglasio = soup1.find('strong', text="Oglasio").next_sibling.next_sibling.text
        #oglasio = oglas.text
        #print(oglas)
    
        #SLIKE
        slike = []
        for s in soup1.find_all('a', class_='fancybox'):
            slika = str(s.img)
            img = slika.split(" ")[3].split('"')[1]        
            #print(img)
            slike.append(img)
        #print(slike)
       

        #VRSTA
        if soup1.find('strong', text='Vrsta'):
            vrsta = soup1.find('strong', text='Vrsta').next_sibling
        else:
            vrsta = "Dafault value"
        #PODRUCJE
        if soup1.find('strong', text='Područje'):
            podrucje = soup1.find('strong', text='Područje').next_sibling
        else:
            podrucje = "Dafault value"
        #LOKACIJA
        if soup1.find('strong', text='Lokacija'):
            lokacija = soup1.find('strong', text='Lokacija').next_sibling
        else:
            lokacija = "Default value"
        #BROJ SPAVACIH SOBA
        if soup1.find('strong', text='Spavaćih Soba'):
            br_spavacih= soup1.find('strong', text='Spavaćih Soba').next_sibling           
            br_spavacih_soba = int("".join(re.findall('\d+',br_spavacih)))
        else:
            br_spavacih_soba = "0"
        #CIJENA
        if soup1.find('strong', text='Cijena'): 
            cijena_apartmana = soup1.find('strong', text='Cijena').next_sibling
            #print(float("".join(re.findall('\d+',cijena_apartmana))))
            cijena = float("".join(re.findall('\d+',cijena_apartmana)))            
        else:
            cijena = "Default value"
        #STAMBENA POVRSINA
        if soup1.find('strong', text='Stambena Površina'):    
            stambena_povrsina = soup1.find('strong', text='Stambena Površina').next_sibling
            stambena_povrsina = stambena_povrsina.split(" ")[1] + " m2"
        else:
            stambena_povrsina = "nepoznato m2"
        #OPIS
        if soup1.find('strong', text='Opis'):
            opis = soup1.find('strong', text='Opis').next_sibling
        else:
            opis = "Default value"
        #MOBILNI
        if soup1.find('strong', text='Mobitel'):     
            mobilni = soup1.find('strong', text='Mobitel').next_sibling
        else:
            mobilni = "Default value"
        #BROJ OGLASA
        if soup1.find('strong', text='Oglas Broj'):    
            broj_ogl = soup1.find('strong', text='Oglas Broj').next_sibling
            broj_oglasa = int("".join(re.findall('\d+',broj_ogl)))
        else:
            broj_oglasa = "Default value"
        #KLIMA
        if soup1.find('strong', text='Klima Uređaj'):
            klima1 = soup1.find('strong', text='Klima Uređaj').next_sibling
            klima = True
        else:
            klima = False


        #KUPATILO
        if soup1.find('strong', text='Kupatila'):     
            kupatila = soup1.find('strong', text='Kupatila').next_sibling
            broj_kupatila = int("".join(re.findall('\d+',kupatila)))
        else:
            broj_kupatila = "Default value"
        #ZEMLJISTE
        if soup1.find('strong', text='Zemljište'):    
            zemljiste = soup1.find('strong', text='Zemljište').next_sibling
        else:
            zemljiste= "Default value"
        #PARKING
        if soup1.find('strong', text='Parking Mjesta'):
            park = soup1.find('strong', text='Parking Mjesta').next_sibling
            parking = int("".join(re.findall('\d+',park)))
        else:
            parking = "Default value"   
       #UDALJENOST OD MORA
        if soup1.find('strong', text='Od Mora'):    
            more = soup1.find('strong', text='Od Mora').next_sibling
            od_mora = int("".join(re.findall('\d+',more)))
        else:
            od_mora= "Nepoznata odaljenost"
        #NOVOGRADNJA
        if soup1.find('strong', text='Novogradnja'):
            novogradnja1 = soup1.find('strong', text='Novogradnja').next_sibling
            novogradnja = True
        else:
            novogradnja = False 
        #WEB STRANICA
        web_stranica = linkaa
        #ZADNJA PROMJENA
        if soup1.find('strong', text='Zadnja Promjena'):
            zadnja_prom = soup1.find('strong', text='Zadnja Promjena').next_sibling
            zadnja_prom = zadnja_prom.split(": ")[1].split("\n")[0]
            zadnja_promjena = datetime.strptime(zadnja_prom, "%d %b, %Y")
        else:
            zadnja_promjena = "Default value"         
 
        
        
        apartman.insert_one({"vrsta":vrsta, "podrucje":podrucje,"lokacija":lokacija, "br_spavacih_soba":br_spavacih_soba, "broj_kupatila":broj_kupatila, "cijena":cijena, "stambena_povrsina":stambena_povrsina, "zemljiste":zemljiste, "parking":parking, "od_mora":od_mora, "novogradnja":novogradnja, "klima":klima, "naslov":naslov, "opis": opis, "web_stranica":web_stranica, "oglasio": oglasio, "mobilni":mobilni, "broj_oglasa":broj_oglasa, "zadnja_promjena":zadnja_promjena, "slike":slike, "novogradnja":novogradnja})
print("Uspjesan upis u bazu!")