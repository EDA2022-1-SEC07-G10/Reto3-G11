﻿"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from datetime import datetime
assert config
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import os
"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

Se define la estructura de un catálogo de libros.
El catálogo tendrá  una lista para los libros.

Los autores, los tags y los años se guardaran en
tablas de simbolos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------

#TODO: Funciones de ordenamiento
#TODO: Agregar funciones de ordenar otras cosas
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los gamenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {"games":m.newMap(numelements=40,maptype='PROBING'),
                "dateGame":om.newMap('RBT'),
                "records":m.newMap(numelements=40,maptype='PROBING'),
                "dateRecord":om.newMap('RBT'),
                "playerRecord":om.newMap('RBT'),
                "triesRecord":om.newMap('RBT')
                }
    return analyzer

def addGame(analyzer,game):

    m.put(analyzer["games"],game['Game_Id'],game)
    updateDateGame(analyzer["dateGame"],game)
    return analyzer

def addRecord(analyzer,record):
    m.put(analyzer["records"],record["Game_Id"],record)

    updateRecordTries(analyzer["triesRecord"],record)
    updateRecordDate(analyzer["dateRecord"],record)
    updatePlayerRecord(analyzer["playerRecord"],record)
    return analyzer


def updateDateGame(map,game):
    gameDate = game["Release_Date"]
    
    if gameDate == "" or gameDate == " " or gameDate == None:
        gameDate="31-12-99"
    
    gameDate = datetime.strptime(gameDate,"%y-%m-%d")
    entry = om.get(map,gameDate)
    if entry is None:
        dateEntry = newDateGameEntry(game)
        om.put(map,gameDate,dateEntry)
    else:
        dateEntry = me.getValue(entry)
        addDateGameIndex(dateEntry,game)
    
    return map
def updateRecordTries(map,record):
    recordTries = record["Num_Runs"]
    entry = om.get(map,recordTries)
    if entry is None:
        triesEntry = newRecordTriesEntry(record)
        om.put(map,recordTries,triesEntry)
    else:
        triesEntry = me.getValue(entry)
        addRecordTriesIndex(triesEntry,record)
    
    return map
def updatePlayerRecord(map,record):
    players = record["Players_0"].split(",")
    players  = [x.strip() for x in players]
    for player in players:
        entry = om.get(map,player)
        if entry is None:
            playerEntry = newPlayerRecordEntry(record)
            om.put(map,player,playerEntry)
        else:
            playerEntry = me.getValue(entry)
            addPlayerRecordIndex(playerEntry,record)
    
    return map

def updateRecordDate(map,record):
    recordDate = record["Record_Date_0"]
    if recordDate == "" or recordDate == " " or recordDate == None:
        recordDate="9999-12-31T23:59:59Z"
    recordDate = datetime.strptime(recordDate,"%Y-%m-%dT%H:%M:%SZ")
    entry = om.get(map,recordDate)
    if entry is None:
        dateEntry = newDateRecordEntry(record)
        om.put(map,recordDate,dateEntry)
    else:
        dateEntry = me.getValue(entry)
        addDateRecordIndex(dateEntry,record)
    
    return map

def addDateGameIndex(dateEntry,game):
    lst = dateEntry["lstgames"]
    lt.addLast(lst,game)
    gamesIndex = dateEntry["gamesIndex"]
    
    gameEntry = m.get(gamesIndex, game["Game_Id"])
    if (gameEntry is None):
         entry = newGameEntry(game["Game_Id"], game)
         m.put(gamesIndex, game["Game_Id"], entry)
    else:
         entry = me.getValue(gameEntry)
         lt.addLast(entry["lstgames"], game)
         m.put(gamesIndex, game["Game_Id"], entry)
    
    return gameEntry

def addRecordTriesIndex(triesEntry,record):
    lst = triesEntry["lstrecords"]
    lt.addLast(lst,record)
    recordsIndex = triesEntry["recordsIndex"]
    
    recordEntry = m.get(recordsIndex, record["Game_Id"])
    if (recordEntry is None):
         entry = newRecordEntry(record["Game_Id"], record)

         m.put(recordsIndex, record["Game_Id"], entry)
    else:
         entry = me.getValue(recordEntry)
         lt.addLast(entry["lstrecords"], record)
    
    return recordEntry

def addPlayerRecordIndex(playerEntry,record):
    lst = playerEntry["lstrecords"]
    lt.addLast(lst,record)
    recordsIndex = playerEntry["recordsIndex"]
    
    recordEntry = m.get(recordsIndex, record["Game_Id"])
    if (recordEntry is None):
         entry = newRecordEntry(record["Game_Id"], record)

         m.put(recordsIndex, record["Game_Id"], entry)
    else:
         entry = me.getValue(recordEntry)
         lt.addLast(entry["lstrecords"], record)
    
    return recordEntry

def addDateRecordIndex(dateEntry,record):
    lst = dateEntry["lstrecords"]
    lt.addLast(lst,record)
    recordsIndex = dateEntry["recordsIndex"]
    
    recordEntry = m.get(recordsIndex, record["Game_Id"])
    if (recordEntry is None):
         entry = newRecordEntry(record["Game_Id"], record)

         m.put(recordsIndex, record["Game_Id"], entry)
    else:
         entry = me.getValue(recordEntry)
         lt.addLast(entry["lstrecords"], record)
    
    return recordEntry


def newGameEntry(gameMap,game):
    entry = {"gamesIndex":gameMap,
            "lstgames":lt.newList('SINGLE_LINKED')   }
    lt.addLast(entry["lstgames"],game)
    return entry

def newPlayerRecordEntry(record):
    entry = {"recordsIndex":m.newMap(numelements=40,maptype='PROBING'),
            "lstrecords":lt.newList('SINGLE_LINKED')   }
    lt.addLast(entry["lstrecords"],record)
    return entry

def newRecordTriesEntry(record):
    entry = {"recordsIndex":m.newMap(numelements=40,maptype='PROBING'),
            "lstrecords":lt.newList('SINGLE_LINKED')   }
    lt.addLast(entry["lstrecords"],record)
    return entry

def newRecordEntry(recordMap,record):
    entry = {"recordsIndex":recordMap,
            "lstrecords":lt.newList('SINGLE_LINKED')   }
    lt.addLast(entry["lstrecords"],record)
    return entry

def newDateGameEntry(game):
    entry = {"gamesIndex":m.newMap(numelements=5,maptype='PROBING'),
            "lstgames":lt.newList('SINGLE_LINKED')   }
    lt.addLast(entry["lstgames"],game)
    return entry

def newDateRecordEntry(record):
    entry = {"recordsIndex":m.newMap(numelements=5,maptype='PROBING'),
            "lstrecords":lt.newList('SINGLE_LINKED')   }
    lt.addLast(entry["lstrecords"],record)
    return entry

def req1(analyzer,floor:str,ceiling:str):

    #TODO: Tabular y ordenar. Quitar prints
    floor = datetime.strptime(floor, '%Y-%m-%d')
    ceiling = datetime.strptime(ceiling, '%Y-%m-%d')
    
    keys = om.keySet(analyzer["dateGame"])
    for key in lt.iterator(keys):
        if key >= floor and key <= ceiling:
            elements = (om.get(analyzer["dateGame"],key))['value']['lstgames']
            print("\n")
            print(key.strftime("%Y-%m-%d"))
            for element in lt.iterator(elements):
                print(element)

def req2(analyzer,player):
    res = (om.get(analyzer["playerRecord"],player)["value"]["lstrecords"])
    
    for k in lt.iterator(res):
        #TODO: Tabular y ordenar
        id = k["Game_Id"]
        nombre_juego =m.get(analyzer["games"],id)["value"]["Name"]
        print(k+" "+nombre_juego)

def req3(analyzer,floor,ceiling):
    #TODO: tabular y ordenar
    keys = om.keySet(analyzer["triesRecord"])
    
    for key in lt.iterator(keys):
        if (int(key) in range(floor,ceiling)):
            print(key)
            elements = om.get(analyzer["triesRecord"],key)["value"]["lstrecords"]
            for element in lt.iterator(elements):
                id = element["Game_Id"]
                game_name = m.get(analyzer["games"],id)["value"]["Name"]
                print(game_name)
                print(element)
                
def bono(analyzer):
    pass

def pruebas(analyzer): #Esto solo son pruebaas
    #Con esto se saca la localizacion del pais solo con el nombre
    locator = Nominatim(user_agent="myLocator")
    colombiaLoc = locator.geocode("Colombia")
    brasilLoc = locator.geocode("Brasil")
    #aqui se genera el mapa
    m=folium.Map()
    #crear un mc para cada pais (un for puede ser buena idea)
    mc = MarkerCluster()
    mc.add_child(folium.Marker(location=(colombiaLoc.latitude,colombiaLoc.longitude),popup="Hola"))
    mc.add_child(folium.Marker(location=(colombiaLoc.latitude,colombiaLoc.longitude),popup="Hola"))
    m.add_child(mc)
    m.save("./index.html")
    os.system("start ./index.html") #abre el mapa en el navegador