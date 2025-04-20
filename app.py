from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada en memoria
productos = []
contador_id = 1

# Crear producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    global contador_id
    data = request.get_json()
    producto = {
        'id': contador_id,
        'nombre': data['nombre'],
        'precio': data['precio']
    }
    productos.append(producto)
    contador_id += 1
    return jsonify(producto), 201

# Obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos)

# Obtener un producto por ID
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    for producto in productos:
        if producto['id'] == producto_id:
            return jsonify(producto)
    return jsonify({'error': 'Producto no encontrado'}), 404

# Actualizar producto
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    data = request.get_json()
    for producto in productos:
        if producto['id'] == producto_id:
            producto['nombre'] = data.get('nombre', producto['nombre'])
            producto['precio'] = data.get('precio', producto['precio'])
            return jsonify(producto)
    return jsonify({'error': 'Producto no encontrado'}), 404

# Eliminar producto
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    for producto in productos:
        if producto['id'] == producto_id:
            productos.remove(producto)
            return jsonify({'mensaje': 'Producto eliminado'})
    return jsonify({'error': 'Producto no encontrado'}), 404

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
