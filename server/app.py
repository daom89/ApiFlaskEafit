from flask import Flask,request,jsonify,abort
from firebase_admin import credentials, firestore, initialize_app
import sys
from database import *
from models import Estudiante, Peticion

app = Flask(__name__)

# Inicializar Firestore DB

cred = credentials.Certificate('server/key/key.json')
default_app = initialize_app(cred)
db = firestore.client()
estudiantes_ref = db.collection('Estudiantes')
peticiones_ref = db.collection('Peticiones')

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

# http://127.0.0.1:5000/api/estudiantes
@app.route("/api/estudiantes",methods=['POST'])
def agregar_estudiante():
  try:
    data=request.json
    estudiante_id=str(request.json["cedula"])
    estudiantes_doc=estudiantes_ref.document(estudiante_id)
    if(estudiantes_doc.get().exists):
      error_message={"error":f"Ya existe un estudiante registrando con el ID {estudiante_id}"}
      return jsonify(error_message),400

    nuevo_estudiante = Estudiante(
                        data["cedula"], 
                        data["nombre"], 
                        data["apellido"],
                        data["correo"], 
                        data["carrera"]).to_dict()
    estudiantes_ref.document(estudiante_id).set(nuevo_estudiante)
    return jsonify(nuevo_estudiante),201
  except:
      error_message={"error":"Los datos del estudiante no están completos o son incorrectos"}
      return jsonify(error_message),400


# http://127.0.0.1:5000/api/estudiantes/11234224
@app.route("/api/estudiantes/<string:id>",methods=['PUT'])
def actualizar_estudiante(id):
    data=request.json
    estudiante_doc=estudiantes_ref.document(str(id)).get()
    if(estudiante_doc.exists):
      data_estudiante = Estudiante(
                    data["cedula"], 
                    data["nombre"], 
                    data["apellido"],
                    data["correo"], 
                    data["carrera"]).to_dict()
      estudiante_doc=estudiantes_ref.document(str(id)).set(data)
      return jsonify(data_estudiante), 200
    else:
      error_message={"error":f"No existe un estudiante registrando con el ID {estudiante_doc}"}
      return jsonify(error_message),400

# http://127.0.0.1:5000/api/estudiantes/11234224
@app.route("/api/estudiantes/<string:id>",methods=['DELETE'])
def eliminar_estudiante(id):
    estudiante = estudiantes_ref.document(str(id)).get()
    if(estudiante.exists):
      estudiantes_ref.document(str(id)).delete()
      result={ "cedula":id , "borrado" : True}
      return jsonify(result), 200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400

# http://127.0.0.1:5000/api/estudiantes/11234224
@app.route("/api/estudiantes/<int:id>",methods=['GET'])
def obtener_estudiante(id):
    estudiante_doc=estudiantes_ref.document(str(id)).get()
    if(estudiante_doc.exists):
      return jsonify(estudiante_doc.to_dict()),200
    else:
      error_message={"error":f"No se encontró ningún estudiante con el ID {id}"}
      return jsonify(error_message),400


# http://127.0.0.1:5000/api/estudiantes
@app.route("/api/estudiantes",methods=['GET'])
def obtener_lista_estudiantes():
    results=estudiantes_ref.stream()
    lista_estudiantes=[item.to_dict() for item in results]

    return jsonify({"data":lista_estudiantes}),200
  # lista_estudiantes=[estudiantes_db[key] for key in estudiantes_db.keys()]
  # return jsonify(lista_estudiantes),200


if __name__ == '__main__':
    app.run(debug=True)
