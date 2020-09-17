from flask import Flask,request,jsonify,abort
import sys
from database import *

app = Flask(__name__)

@app.route("/")
def hola_mundo():
  print("holas")
  return "Adiós, Mundo!"

# http://127.0.0.1:5000/saludo/diego?titulo=dev
@app.route("/saludo/<string:nombre>")
def saludo(nombre):
  titulo = request.args.get('titulo', '')
  return f"Hola {titulo} {nombre}"

# http://127.0.0.1:5000/despedida/jaime?frase=Sayonara
@app.route("/despedida/<string:nombre>")
def despedida(nombre):
  frase = request.args.get('frase', 'Adios')
  return f"{frase} {nombre}!"

# http://127.0.0.1:5000/api/estudiantes/11234224
@app.route("/api/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):
  try:
    estudiante=estudiantes_db[str(id)]
    return jsonify(estudiante),200
  except:
    error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
    return jsonify(error_message),400

# http://127.0.0.1:5000/api/estudiantes
@app.route("/api/estudiantes",methods=['GET'])
def obtener_estudiantes():
  lista_estudiantes=[estudiantes_db[key] for key in estudiantes_db.keys()]
  return jsonify(lista_estudiantes),200

# http://127.0.0.1:5000/api/estudiantes
@app.route("/api/estudiantes",methods=['POST'])
def agregar_estudiante():
  estudiante_id=str(request.json["cedula"])
  if(estudiante_id in estudiantes_db):
    error_message={"error":f"Ya existe un estudiante registrando con el ID {estudiante_id}"}
    return jsonify(error_message),400
    
  try:  
    nuevo_estudiante=dict()
    nuevo_estudiante["cedula"]=request.json["cedula"]
    nuevo_estudiante["nombre"]=request.json["nombre"]
    nuevo_estudiante["apellido"]=request.json["apellido"]
    nuevo_estudiante["carrera"]=request.json["carrera"]
    nuevo_estudiante["correo"]=request.json["correo"]
    estudiantes_db[estudiante_id]=nuevo_estudiante
    return jsonify(nuevo_estudiante),201
  except:
      error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
      return jsonify(error_message),400

# http://127.0.0.1:5000/api/estudiantes/11234224
@app.route("/api/estudiantes/<string:id>",methods=['PUT'])
def actualizar_estudiante(id):
    if(id in estudiantes_db):
      estudiantes_db[str(id)] = request.json
      return jsonify(estudiantes_db[str(id)]), 200
    else:
      error_message={"error":f"No existe un estudiante registrando con el ID {estudiante_id}"}
      return jsonify(error_message),400

# http://127.0.0.1:5000/api/estudiantes/11234224
@app.route("/api/estudiantes/<string:id>",methods=['DELETE'])
def eliminar_estudiante(id):
    if(id in estudiantes_db):
      del estudiantes_db[str(id)]
      result={ "cedula":id , "borrado" : True}
      return jsonify(result), 200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400

if __name__ == '__main__':
    app.run(debug=True)
