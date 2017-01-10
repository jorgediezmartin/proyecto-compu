#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import re
import pymongo
import json
import time


from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.bolsa2
collection = db['datos']
response = urllib2.urlopen('http://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000')
print "Response:", response

# Get the URL. This gets the real URL.
print "The URL is: ", response.geturl()



# Getting the code
print "This gets the code: ", response.code

# Get the Headers.
# This returns a dictionary-like object that describes the page fetched,
# particularly the headers sent by the server
print "The Headers are: ", response.info()

# Get the date part of the header
print "The Date is: ", response.info()['date']

# Get the server part of the header
#print "The Server is: ", response.info()['server']
#html = response.read()
#print html


while(True):

	to_wait  = -(time.time()%120) + 120
	time.sleep(to_wait)
	response = urllib2.urlopen('http://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000')
	# Get all data
	html = response.read()
  



# Expresiones regulares, primera busqueda 
	abertis=re.search('ABERTIS</a></td><td>([0-9]{1,6}\,[0-9]{1,6}).*[0-9]{1,2}\:[0-9]{1,2}',html)
	j=abertis.group(0)
#	print j
 
  #j=j.replace(',','.')
	#Sub-busqueda del valor de la cotizacion
	abertisv=re.search('([0-9]{1,6}\,[0-9]{1,6})',j)
	v=abertisv.group(0)
	v=v.replace(',','.') 
   #abertisv=re.search('([0-9]{1,6}\.[0-9]{1,6}))',j)
	urllib2.urlopen('https://api.thingspeak.com/update?api_key=63UT1JTLSUL0KV68&field1='+ str(v))
  #https://api.thingspeak.com/update?api_key=63UT1JTLSUL0KV68&field1=v
  
  #Sub-busqueda del valor del umbral, la variacion
#	abertisj=re.search('class="DifClSb">((-|)[0-9]{1,2}\,[0-9]{1,2})',j)
#	u=abertisj.group(0)
#	variacion=re.search('((-|)[0-9]{1,2}\,[0-9]{1,2})',u)
#	varia=variacion.group(0)
  
  
	#Sub-busqueda de la fecha
	abertisf=re.search('[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,4}',j)
	f=abertisf.group(0)
	#Sub-busqueda de la hora
	abertish=re.search('([0-9]{1,2}\:[0-9]{1,2})',j)
	h=abertish.group(0)
 
	print "-----------COTIZACION-----"
	print v
# 	print "-----------VARIACION-----"
#	print varia
	print" -----------FECHA----------"
	print f
	print " -----------HORA----------"
	print h

        #v=json.dumps(v)
        collection.insert_one({'valor':v,
				'fecha':f,
				'hora':h})
	

        #bolsa=[]
        #bolsa["cotizacion"]=v
        #db.BBDD.insert_one(bolsa)

