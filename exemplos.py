import urllib.request,urllib.parse,urllib.error
import re
import json
import csv
import os
import time


#Usando reg expressions pq os nomes nao sao estaveis no jeux de données...
def procurarExpressao(regExpr, string):
  return re.search(regExpr,string, flags=re.IGNORECASE) 


#Notre-Dame <-> Condillac(Tram B)
pointA ='NOTRE-DAME - MUS' #PLAINE, HUBERT,...
pointB = 'cea' #Alsace, CEA, condillac...


#Parte 1
print('----------PARTE 1----------')
# Localizaçao de todas as paradas de bus, tram, e gares SNCF da regiao 
locationURL = 'https://data.metromobilite.fr/api/findType/json?types=arret'

uh = urllib.request.urlopen(locationURL)
print('Recuperando JSON...')
data = uh.read().decode()
try:
    js = json.loads(data)
    print('Retrieved',len(data),'characters!')
except:
    print('Failure to retrieve data!', 'Exiting.')
    time.sleep(2)
    exit()

fs = js['features']
for arrt in fs:
    nomeParada = arrt['properties']['LIBELLE']            
    if(procurarExpressao(pointA,nomeParada) != None or procurarExpressao(pointB,nomeParada) != None):
        lon = arrt['geometry']['coordinates'][0]
        lat = arrt['geometry']['coordinates'][1]
        print('Parada:',nomeParada,'location:',lat,lon)
        continue
    

#Parte 2 - frequencia do Tram B em 2016
print('----------PARTE 2----------')
#Se quiser baixar o arquivo Excel inteiro...
baixar = False
url = 'https://data.metropolegrenoble.fr/ckan/dataset/c59ebbee-7ccc-4a18-a4b4-d4d3bf4907c6/resource/8576e223-54c7-4b68-846d-5d115aafc012/download/'
fileName = 'tram-b'
extension='.xls'
path = url+fileName
if baixar:    
    if not os.path.isfile(fileName+extension):
        downloadPath = path+extension
        print('Downloading file',fileName,':',downloadPath)
        try:            
            urllib.request.urlretrieve(downloadPath,fileName+extension )
            print('Download complete!')
        except:
            print('Unable to retrieve file.')
            time.sleep(2)            
    else:
            print(fileName, 'already exists.')    

# Vamos usar o CSV exportado manualmente
print('Passando para nosso CSV...')
with open(fileName+'.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')    
    lines = list(i.rstrip() for i in csvfile)

header = lines[6]
pointAIndexes = None
pointBIndexes = None
for index,value in enumerate(header.split(',')):    
    if procurarExpressao(pointA,value) != None:
        pointA = value
        pointAIndexes = [index+6,index]                
    if procurarExpressao(pointB,value) != None:        
        pointBIndexes = [index+6, index]
        pointB = value

if (pointAIndexes == None or pointBIndexes==None):
    print('Parada nao encontrada!', 'The End.')
else:
    ida = lines[pointAIndexes[0]].split(',')[pointBIndexes[1]]
    if ida == '':
        ida='0'
    volta = lines[pointBIndexes[0]].split(',')[pointAIndexes[1]]
    if volta == '':
        volta='0'
    print('Pessoas que sobem em',pointA,'e descem em',pointB,':',ida)
    print('Pessoas que sobem em',pointB,'e descem em',pointA,':',volta)



