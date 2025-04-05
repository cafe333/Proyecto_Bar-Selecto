from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"  


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="proyecto_bar_selecto"
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contrasenia = request.form['contrasenia']
        cursor = get_db_connection().cursor()
        cursor.execute("SELECT * FROM empleado WHERE Contrasenia = %s", (contrasenia,))
        empleado = cursor.fetchone()

        if empleado:
            rol_id = empleado[4]  
            
            # Obtén el rol por el ID
            cursor.execute("SELECT nombre_rol FROM roles WHERE ID_Roles = %s", (rol_id,))
            rol = cursor.fetchone()[0]  

            if rol == 'Administrador':
                return redirect(url_for('admin_menu'))
            elif rol == 'Mesero':
                return redirect(url_for('mesero_menu'))
        else:
            flash("Contraseña incorrecta o no registrada", "danger")

    return render_template('login.html')


@app.route('/mesero')
def mesero_menu():
    return render_template('mesero_menu.html')


@app.route('/admin')
def admin_menu():
    return render_template('admin_menu.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        contrasenia = request.form['contrasenia']
        telefono = request.form['telefono']  
        rol = request.form['rol']

      
        cursor = get_db_connection().cursor()
        cursor.execute("SELECT Telefono FROM empleado WHERE Telefono = %s", (telefono,))
        existing_telefono = cursor.fetchone()

        if existing_telefono:
            flash("El teléfono ya está registrado. Intenta con otro.", "danger")
            return render_template('registro.html')
        
        
        cursor.execute("SELECT ID_Roles FROM roles WHERE nombre_rol = %s", (rol,))
        rol_id = cursor.fetchone()[0]

        
        cursor.execute("INSERT INTO empleado (Telefono, Nombre, ApellidoP, ApellidoM, Contrasenia, ID_Roles) VALUES (%s, %s, %s, %s, %s, %s)",
                       (telefono, nombre, apellido_paterno, apellido_materno, contrasenia, rol_id))
        get_db_connection().commit()

        flash("Registro exitoso, ya puedes iniciar sesión.", "success")
        return redirect(url_for('login'))

    return render_template('registro.html')
