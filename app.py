from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret_key' 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123", 
        database="bar_selecto" 
    )

# Ruta para la página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contrasenia = request.form['contrasenia']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # asumiendo que el teléfono ya está guardado en la base de datos.
        cursor.execute("SELECT * FROM empleado WHERE contrasenia = %s", (contrasenia,))
        user = cursor.fetchone()

        if user:
            # Guarda el telefono para no pedir otra vez
            session['telefono'] = user['telefono']

            if user['id_roles'] == 1: 
                return redirect('/dashboard_mesero')
            elif user['id_roles'] == 2:  
                return redirect('/dashboard_administrador')
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/registrar_empleado', methods=['GET', 'POST'])
def registrar_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidop = request.form['apellidop']
        apellidom = request.form['apellidom']
        telefono = request.form['telefono']
        contrasenia = request.form['contrasenia']
        id_roles = request.form['id_roles']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(""" 
                INSERT INTO empleado (nombre, apellidop, apellidom, telefono, contrasenia, id_roles)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellidop, apellidom, telefono, contrasenia, id_roles))
            
            conn.commit()
            flash('Empleado registrado exitosamente', 'success')

            # Guardar el teléfono en la sesión después de registro
            session['telefono'] = telefono

            return redirect('/')  # Redirige al login
        except Exception as e:
            conn.rollback()  
            flash(f'Ocurrió un error: {e}', 'danger')
            return redirect('/registrar_empleado')
        finally:
            cursor.close()
            conn.close()

    return render_template('registrar_empleado.html')

@app.route('/dashboard_mesero', methods=['GET', 'POST'])
def dashboard_mesero():
    return render_template('dashboard_mesero.html')

@app.route('/dashboard_administrador', methods=['GET', 'POST'])
def dashboard_administrador():
    return render_template('dashboard_administrador.html')

if __name__ == "__main__":
    app.run(debug=True)
