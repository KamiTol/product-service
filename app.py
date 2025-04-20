from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configuración de la conexión con PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="productos_db",
        user="user",
        password="pass"
    )
    return conn

# Crear producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    nombre = data['nombre']
    precio = data['precio']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id;', (nombre, precio))
    producto_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'id': producto_id, 'nombre': nombre, 'precio': precio}), 201

# Obtener productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos;')
    productos = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([{'id': producto[0], 'nombre': producto[1], 'precio': producto[2]} for producto in productos])

# Obtener un producto por ID
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = %s;', (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if producto:
        return jsonify({'id': producto[0], 'nombre': producto[1], 'precio': producto[2]})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

# Actualizar un producto
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE productos SET nombre = %s, precio = %s WHERE id = %s RETURNING id;', (nombre, precio, producto_id))
    producto = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if producto:
        return jsonify({'id': producto[0], 'nombre': nombre, 'precio': precio})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

# Eliminar un producto
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = %s RETURNING id;', (producto_id,))
    producto = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if producto:
        return jsonify({'mensaje': 'Producto eliminado'})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
