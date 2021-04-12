from flask import Flask, render_template, url_for, redirect, request,jsonify, flash, session
import hashlib,os
import time
import requests
import json
import math
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL


#Mysql Connection
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'reserva_db'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'


#CONSUMIR API
@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        url = "http://localhost:3000/user/login"
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        response = requests.post(url, json= {"correo": correo,"contraseña":contraseña})
        if response.status_code == 200:
            session["user"] = correo
            return redirect(url_for("crear_reserva"))
        
        if response.status_code == 404:
            flash('Ingrese datos validos.','error')
            return redirect(url_for("login"))

        if response.status_code == 401:
            flash('Ingrese datos validos.','error')
            return redirect(url_for("login"))

        if response.status_code == 500:
            flash('Ingrese datos validos.','error')
            return redirect(url_for("login"))

@app.route("/logout", methods = ['GET','POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

    


@app.route("/create-reservation", methods=['GET', 'POST'])
def crear_reserva():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))

    if request.method == 'GET':
        url_users = "http://localhost:3000/user"
        url_salas = "http://localhost:3000/sala"
        response = requests.get(url_users)
        response2 = requests.get(url_salas)
        if response.status_code == 200:
            users = json.loads(response.text)

        if response2.status_code == 200:
            salas = json.loads(response2.text)

        return render_template("form_crearReserva.html", datos=users, salas=salas)

    if request.method == 'POST':
        id_usuario = request.form.get("id_usuario")
        id_sala = request.form.get("id_sala")
        fecha = request.form.get("fecha")
        hora_inicio = request.form.get("hora_inicio")
        hora_final = request.form.get("hora_final")
        url = "http://localhost:3000/reserva"
        response = requests.post(url,json={"id_usuario":id_usuario,
        "id_sala":id_sala,"fecha":fecha,"hora_inicio":hora_inicio,"hora_final":hora_final})
        if response.status_code == 400:
            flash('Hora o fecha invalidas.','error')
        
        if response.status_code == 201:
            flash('Sala reservada.','bien')

        if response.status_code == 405:
            flash('Horario ocupado.','error')

        if response.status_code == 401:
            flash('Inserte datos Validos.','error')
        return redirect(url_for('crear_reserva'))


@app.route("/create-user", methods=['GET','POST'])
def crear_user():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))

    if request.method == 'GET':
    
        return render_template("form_crearUsuario.html")

    if request.method == 'POST':
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        ci_usuario = request.form.get("ci_usuario")
        cel_usuario = request.form.get("cel_usuario")
        direccion = request.form.get("direccion")
        url = "http://localhost:3000/user"
        response = requests.post(url,json={"nombre":nombre,
        "apellido":apellido,"correo":correo,"contraseña":contraseña,"ci_usuario":ci_usuario,"cel_usuario":cel_usuario,
        "direccion":direccion})        

        if response.status_code == 201:
            flash('Usuario Agregado Correctamente.','bien')
        
        if response.status_code == 401:
            flash('El usuario ya posee una cuenta.','error')

        if response.status_code == 403:
            flash('Datos invalidos.','error')

        return redirect(url_for('crear_user'))


@app.route("/create-sala", methods=['GET','POST'])
def crear_sala():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))

    if request.method == 'GET':
    
        return render_template("form_crearSala.html")

    if request.method == 'POST':
        descripcion = request.form.get("descripcion")
        capacidad = request.form.get("capacidad")
        url = "http://localhost:3000/sala"
        response = requests.post(url,json={"descripcion":descripcion,"capacidad":capacidad})        

        if response.status_code == 201:
            flash('Sala Creada Correctamente.','bien')
        
        if response.status_code == 401:
            flash('Inserte datos.','error')

        return redirect(url_for('crear_sala')) 

@app.route("/manage-clients", methods=['GET','POST'])
def admin_clientes():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))

    if request.method == 'GET':
        url_users = "http://localhost:3000/user"
        response = requests.get(url_users)
        if response.status_code == 200:
            users = json.loads(response.text)
        return render_template("manage_cliente.html", datos=users)


@app.route("/user_preview/<int:id>", methods=['GET','POST'])
def user_preview(id):
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))

    if request.method == 'GET':
        url = "http://localhost:3000/user/"+str(id)
        response = requests.get(url)
        if response.status_code == 200:
            users = json.loads(response.text)
            return render_template("user_preview.html", datos=users)


    if request.method == 'POST':
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        ci_usuario = request.form.get("ci_usuario")
        cel_usuario = request.form.get("cel_usuario")
        direccion = request.form.get("direccion")
        url = "http://localhost:3000/user/"+str(id)
        response = requests.put(url,json={"nombre":nombre,
        "apellido":apellido,"correo":correo,"contraseña":contraseña,"ci_usuario":ci_usuario,"cel_usuario":cel_usuario,
        "direccion":direccion})

        if response.status_code == 201:
            flash('Cliente Actualizado Correctamente.','bien')
        
        if response.status_code == 404:
            flash('Cliente no encontrado.','error')

        if response.status_code == 401:
            flash('Datos invalidos.','error')

        return redirect(request.url)
    

@app.route("/user_delete/<int:id>", methods=['POST'])
def user_delete(id):
    if request.method == 'POST':
        url = "http://localhost:3000/user/"+str(id)
        response = requests.delete(url)
        if response.status_code == 201:
            flash('Cliente Eliminado.','bien')
            return redirect(url_for('admin_clientes'))
        if response.status_code == 404:
            flash('Cliente no encontrado.','error')
            return redirect(url_for('admin_clientes'))
        if response.status_code == 401:
            flash('Error.','error')
            return redirect(url_for('admin_clientes'))
        
@app.route("/manage-reservas", methods=['GET','POST'])
def admin_reservas():
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))

    if request.method == 'GET':
        url = "http://localhost:3000/reserva"
        response = requests.get(url)
        if response.status_code == 200:
            reservas = json.loads(response.text)
            return render_template("manage_reservas.html", datos=reservas)

    return render_template("manage_reservas.html")

@app.route("/reserva-preview/<int:id>", methods=['GET','POST'])
def reserva_preview(id):
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for("login"))


    if request.method == 'GET':
        url_reserva = "http://localhost:3000/reserva/"+str(id)
        url_salas = "http://localhost:3000/sala"
        response = requests.get(url_reserva)
        response_sala = requests.get(url_salas)
        if response.status_code == 200:
            reserva = json.loads(response.text)

        if response_sala.status_code == 200:
            salas = json.loads(response_sala.text)

        return render_template("reserva_preview.html", datos=reserva, salas=salas)
    

    if request.method == "POST":
        id_sala = request.form.get("id_sala")
        fecha = request.form.get("fecha")
        hora_inicio = request.form.get("hora_inicio")
        hora_final = request.form.get("hora_final")
        print(hora_final)
        url = "http://localhost:3000/reserva/"+str(id)
        response = requests.put(url,json={"id_sala":id_sala,"fecha":fecha,"hora_inicio":hora_inicio,
        "hora_final":hora_final})
        if response.status_code == 400:
            flash('Hora o fecha invalidas.','error')
            return redirect(request.url)

        if response.status_code == 201:
            flash('Actualizado con exito.','bien')
            return redirect(request.url)

        if response.status_code == 405:
            flash('Horario ocupado.','error')
            return redirect(request.url)

        if response.status_code == 401:
            flash('Inserte datos o problemas en la base de datos.','error')
            return redirect(request.url)

@app.route("/reserva-delete/<int:id>", methods=['POST'])
def reserva_delete(id):
    if request.method == 'POST':
        url = "http://localhost:3000/reserva/"+str(id)
        response = requests.delete(url)
        if response.status_code == 404:
            flash('La reserva no existe.','error')
            return redirect(url_for('admin_reservas'))

        if response.status_code == 201:
            flash('Reserva eliminada con exito.','bien')
            return redirect(url_for('admin_reservas'))

        if response.status_code == 401:
            flash('Error.','error')
            return redirect(url_for('admin_reservas'))


        
#force=True,silent=False
#COMIENZO API
@app.route("/user/login", methods = ["POST"])
def api_usuarios():
    try:
        correo = request.get_json()['correo'] 
        contraseña = request.get_json()['contraseña']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s and contraseña = %s;",(correo,contraseña))
        data = cur.fetchall()
        cur.close()
        if (len(data)>0): 
            return jsonify(data),200
        else:
            jsonify({"Error": "No registrado."}),404

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401

@app.route("/user", methods = ["GET"])
def api_getUsers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios;")
        data = cur.fetchall()
        cur.close()
        return jsonify(data),200
    except:
        return jsonify({"Error": " Error al conectar con la base de datos."}),405

@app.route("/user/<int:id>", methods = ["GET"])
def api_getOneUsers(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id_usuario = %s;",(id,))
        data = cur.fetchall()
        cur.close()
        if (len(data)>0): 
            return jsonify(data),200
        else:
            return jsonify({"Error": " Cliente no encontrado."}),404
    except:
        return jsonify({"Error": " Error al conectar con la base de datos."}) ,405       


@app.route("/sala", methods = ["GET"])
def api_getSalas():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM salas;")
        data = cur.fetchall()
        cur.close()
        return jsonify(data),200
    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401



@app.route("/user", methods = ["POST"])
def api_add_user():
    try:
        if request.method == 'POST':
            nombre = request.get_json()['nombre']
            apellido = request.get_json()['apellido']
            correo = request.get_json()['correo']
            contraseña = request.get_json()['contraseña']
            tipo_usuario = 1
            ci_usuario = request.get_json()['ci_usuario']
            cel_usuario = request.get_json()['cel_usuario']
            direccion = request.get_json()['direccion']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE correo = %s OR ci_usuario = %s",(correo,ci_usuario))
            data = cur.fetchall()
            if (len(data)==0):
                cur.execute("INSERT INTO usuarios (nombre,apellido,correo,contraseña,tipo_usuario,ci_usuario,cel_usuario,direccion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);",(nombre,apellido,correo,contraseña,tipo_usuario,ci_usuario,cel_usuario,direccion))
                mysql.connection.commit()
                cur.close()
                return jsonify({"Message": "Cliente Agregado Correctamente."}),201
            else:
                return jsonify({"Message": "El cliente ya posee una cuenta."}),401

    except:
        return jsonify({"Error": "Datos invalidos."}),403


@app.route("/user/<int:id>", methods = ["PUT"])
def api_update_user(id):
    try:
            id_user = id
            nombre = request.get_json()['nombre']
            apellido = request.get_json()['apellido']
            correo = request.get_json()['correo']
            contraseña = request.get_json()['contraseña']
            tipo_usuario = 1
            ci_usuario = request.get_json()['ci_usuario']
            cel_usuario = request.get_json()['cel_usuario']
            direccion = request.get_json()['direccion']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id_usuario = %s",(id_user,))
            data = cur.fetchall()
            if (len(data)==0):
                return jsonify({"Message": "El Cliente no existe."}),404
            else:
                cur.execute("""UPDATE usuarios SET nombre = %s ,apellido = %s,correo = %s,contraseña = %s,
                tipo_usuario = %s,ci_usuario = %s,cel_usuario = %s,direccion = %s
                 WHERE id_usuario = %s;""",(nombre,apellido,correo,contraseña,tipo_usuario,ci_usuario,cel_usuario,direccion,id_user))
                mysql.connection.commit()
                cur.close()
                return jsonify({"Message": "El Cliente ha sido actualizado."}),201

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401


@app.route("/user/<int:id>", methods = ["DELETE"])
def api_delete_user(id):
    try:
        id_user = id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id_usuario = %s",(id_user,))
        data = cur.fetchall()
        cur.close()
        if (len(data)==0):
            return jsonify({"Error": "Cliente no existe."}),404
        else:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM reservas WHERE id_usuario = %s",(id_user,))
            mysql.connection.commit()
            cur.execute("DELETE FROM usuarios WHERE id_usuario = %s",(id_user,))
            mysql.connection.commit()
            cur.close()
            return jsonify({"Message": "Cliente eliminado con exito."}),201

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401
 
    
@app.route("/sala", methods = ["POST"])
def api_add_sala():
    try:
        if request.method == 'POST':
            descripcion = request.get_json()['descripcion']
            capacidad = request.get_json()['capacidad']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO salas (descripcion,capacidad) VALUES (%s,%s);",(descripcion,capacidad))
            mysql.connection.commit()
            cur.close()
            return jsonify({"Message": "Sala agregada Correctamente."}),201

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401


@app.route("/sala/<int:id>", methods = ["PUT"])
def api_update_sala(id):
    try:
            id_sala = id
            descripcion = request.get_json()['descripcion']
            capacidad = request.get_json()['capacidad']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM salas WHERE id_sala = %s",(id_sala,))
            data = cur.fetchall()
            if (len(data)==0):
                return jsonify({"Message": "La sala no existe."}),404
            else:
                cur.execute("""UPDATE salas SET descripcion = %s ,capacidad = %s
                 WHERE id_sala = %s;""",(descripcion,capacidad,id_sala))
                mysql.connection.commit()
                cur.close()
                return jsonify({"Message": "La sala ha sido actualizada."}),201

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401


@app.route("/sala/<int:id>", methods = ["DELETE"])
def api_delete_sala(id):
    try:
        id_sala = id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM salas WHERE id_sala = %s",(id_sala,))
        data = cur.fetchall()
        if (len(data)==0):
            return jsonify({"Error": "La sala no existe."}),404
        else:
            cur.execute("DELETE FROM salas WHERE id_sala = %s",(id_sala,))
            mysql.connection.commit()
            cur.close()
            return jsonify({"Message": "Sala eliminada con exito."}),201

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401


@app.route("/reserva", methods = ["POST"])
def api_add_reserva():
    try:
        id_usuario = request.get_json()['id_usuario']
        id_sala = request.get_json()['id_sala']
        fecha = datetime.strptime(request.get_json()['fecha'], '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(request.get_json()['hora_inicio'], '%H:%M')
        hora_final = datetime.strptime(request.get_json()['hora_final'], '%H:%M')
        fecha_actual = datetime.now()
        if ( hora_inicio >= hora_final or str(fecha) < str(fecha_actual.date())):
            return jsonify({"Message": "Hora o fecha invalidas."}),400
        else:   
            cur = mysql.connection.cursor()
            cur.execute("CALL mostrarReservas(%s,%s)",(fecha,id_sala))
            data = cur.fetchall()
            if (len(data)==0):
                cur.execute("INSERT INTO reservas (id_usuario,id_sala,fecha,hora_inicio,hora_final) VALUES (%s,%s,%s,%s,%s);",(id_usuario,id_sala,fecha,hora_inicio,hora_final))
                mysql.connection.commit()
                cur.close()
                return jsonify({"Message": "Sala reservada."}),201
            else:
                for x in data:
                    if (datetime.strptime(x[1],'%H:%M') <= hora_final and datetime.strptime(x[2],'%H:%M') >= hora_inicio):
                        cur.close()
                        return jsonify({"Message": "Horario ocupado."}),405
                    else:
                        cur.execute("INSERT INTO reservas (id_usuario,id_sala,fecha,hora_inicio,hora_final) VALUES (%s,%s,%s,%s,%s);",(id_usuario,id_sala,fecha,hora_inicio,hora_final))
                        mysql.connection.commit()
                        cur.close()
                        return jsonify({"Message": "Sala reservada."}),201
               
    except:
        return jsonify({"Error": "Inserte datos correctos."}),401

@app.route("/reserva/<int:id>", methods = ["PUT"])
def api_update_reserva(id):
    try:
        id_reserva = id
        id_sala = request.get_json()['id_sala']
        fecha = datetime.strptime(request.get_json()['fecha'], '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(request.get_json()['hora_inicio'], '%H:%M')
        hora_final = datetime.strptime(request.get_json()['hora_final'], '%H:%M')
        fecha_actual = datetime.now()
        if ( hora_inicio > hora_final or str(fecha) < str(fecha_actual.date())):
            return jsonify({"Message": "Hora o fecha invalidas."}),400
        else:   
            cur = mysql.connection.cursor()
            cur.execute("CALL mostrarReservasUpdate(%s,%s,%s)",(fecha,id_sala,id_reserva))
            data = cur.fetchall()
            if (len(data)==0):
                cur.execute("UPDATE reservas SET id_sala = %s,fecha = %s,hora_inicio = %s,hora_final = %s WHERE id_reserva = %s;",(id_sala,fecha,hora_inicio,hora_final,id_reserva))
                mysql.connection.commit()
                cur.close()
                return jsonify({"Message": "Reserva actualizada."}),201
            else:
                for x in data:
                    if (datetime.strptime(x[1],'%H:%M') <= hora_final and datetime.strptime(x[2],'%H:%M') >= hora_inicio):
                        cur.close()
                        return jsonify({"Message": "Horario ocupado."}),405
                    else:
                        cur.execute("UPDATE reservas SET id_sala = %s,fecha = %s,hora_inicio = %s,hora_final = %s WHERE id_reserva = %s;",(id_sala,fecha,hora_inicio,hora_final,id_reserva))
                        mysql.connection.commit()
                        cur.close()
                        return jsonify({"Message": "Reserva actualizada."}),201
               
    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401

@app.route("/reserva/<int:id>", methods = ["DELETE"])
def api_delete_reserva(id):
    try:
        id_reserva = id
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_reserva FROM reservas WHERE id_reserva = %s",(id_reserva,))
        data = cur.fetchall()
        if (len(data)==0):
            return jsonify({"Error": "La reserva no existe."}),404
        else:
            cur.execute("DELETE FROM reservas WHERE id_reserva = %s",(id_reserva,))
            mysql.connection.commit()
            cur.close()
            return jsonify({"Message": "Reserva eliminada con exito."}),201

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),401

@app.route("/reserva", methods = ["GET"])
def api_getReservas():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM vista_reservas;"),200
        data = cur.fetchall()
        cur.close()
        return jsonify(data),200

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),400



@app.route("/reserva/<int:id>", methods = ["GET"])
def api_getOnlyReservas(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("call mostrarReservaID(%s)",(id,))
        data = cur.fetchall()
        cur.close()
        return jsonify(data),200

    except:
        return jsonify({"Error": "inserte datos o problemas con la base de datos."}),400






if __name__ == '__main__':
    app.run(port=3000, debug=True)