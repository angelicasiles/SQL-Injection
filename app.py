from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',  # Cambia la contraseña si es diferente
    'database': 'banco'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    # Obtener los datos del formulario
    busqueda = request.form['busqueda']

    # Crear la consulta SQL vulnerable a inyección
    query = f"SELECT * FROM cuentas_bancarias WHERE nombre_usuario = '{busqueda}' OR numero_cuenta = '{busqueda}'"

    # Conectar a la base de datos y ejecutar la consulta
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)

    # Obtener los resultados
    cuentas = cursor.fetchall()

    if cuentas:
        return render_template('index.html', cuentas=cuentas)
    else:
        return jsonify({"message": "Usuario no encontrado"}), 400

if __name__ == "__main__":
    app.run(debug=True)
