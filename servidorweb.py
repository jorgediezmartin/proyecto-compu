from flask import Flask
import json
from flask import request
from bson import json_util
from flask import render_template

app = Flask(__name__, static_url_path='')

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.bolsa2
collection = db['datos']
valores=db.datos.find().sort([( '_id' , -1)]).limit(1).next()
#primerv=db.datos.find({},{"_id":0,"hora":0,"fecha":0}).limit(1)
primer=db.datos.find().limit(1).next()
primervalor=primer["valor"]
m=valores["valor"]
z=valores["fecha"]
s=valores["hora"]
print m



@app.route('/')
def index():
	return 'Brihuega Manda'
	return app.send_static_file('index.html')

@app.route('/index.html')
def hello(valor=m,fecha=z,hora=s):
    valores=db.datos.find().sort([( '_id' , -1)]).limit(1).next()
    print valor
    print fecha
    print hora
    return render_template('index.html', valor=valor,fecha=fecha,hora=hora)
    
    

# @app.route('/superior')
#def superior()
#  global umbral_enviado 
#  global sentido
#  
#  if sentido ==  'mayor':
#    if valor> 
  
@app.route('/umbrales.html',methods=['GET'])
def formulario(primervalor=primervalor,ultimovalor=m):
  primer=db.datos.find().limit(1).next()
  primervalor=float(primer["valor"].replace(',','.'))
  nombre = request.args.get('nombre') 
  porcentaje=float(nombre)/100
  l=primervalor*porcentaje
  comparar=l+primervalor
  ultimovalor=float(ultimovalor.replace(',','.'))
  flag=0
  if ultimovalor<comparar :
    flag=1
    print 'Brihuega Manda'


  return render_template('umbrales.html',nombre=nombre,primervalor=primervalor,comparar=comparar,porcentaje=porcentaje,ultimovalor=ultimovalor,flag=flag)
  
  
#    valores_mongo= [\
#    {'fechahora': 'fecha1', 'valor': '5.21', 'Var':'-5.21'},\
#    {'fechahora': 'fecha2', 'valor': '9.21', 'Var':' 5.21'},\
#    ]
#    valores= []
#
#    
#    
#    for x in valores_mongo:
#    valores.append({'fechahora': x['fechahora'], 'valor': float(x['valor']), 'Var' : float(x['Var'])})
#    
#    datos_supera= []

#    print dato_introducido
#    
#    for x in valores:
#       if dato_introducido > 0:
#         if dato_introducido > x['Var'] and x['Var'] > 0:
#           datos_supera.append( x )
#       if dato_introducido < 0:
#         if dato_introducido < x['Var'] and x['Var'] < 0:
#           datos_supera.append( x )


@app.route('/valormedio.html')  
def valormedio():
  cotizaciones=db.datos.find()
  cotizaciones=[float(x["valor"].replace(',','.')) for x in cotizaciones]
  media=sum(cotizaciones)/len(cotizaciones)
  #a=db.datos.aggregate([\{'$group':{'_id':None,'avgvalor':{'$avg':'$valor'}}}\])
  print media
  #return json.dumps(media)
  return render_template('valormedio.html',media=media)

@app.route('/graficas.html')  
def graficas():
  return render_template('graficas.html')
#    
#   try:
#        nombre = request.args.get('nombre') 
#        valores=db.datos.find().sort([( '_id' , -1)]).limit(1).next() 
#        nombre=float(nombre)
#        prueba3='63.5'
#        prueba3=float(prueba3)
#        y=nombre/100.0
#        global umbral_enviado
#        umbral_enviado=(1.0+nombre)*prueba3
        
      
      
    
        
#    except:
#        return render_template('pagina2.html')
#        nombre = request.args.get('nombre') 
#        print nombre
#       
    
       
#@app.route('/pagina2.html', methods=['GET'])
#def login(nombre):
#    if request.method == 'GET':
#        do_the_login()
#    else:
#        show_the_login_form()
#def index1():
#return app.send_static_file('index.html')




@app.route('/getDatosBolsa')
def getDatosBolsa():
	to_return = []
	for document in collection.find():
		print document['_id: -1']
		if 'ABERTIS' in document:
			print document['ABERTIX']
		to_return.append(document)
	return json.dumps(to_return, default=json_util.default)


if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0')
