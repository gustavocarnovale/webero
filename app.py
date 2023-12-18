from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS  # Importa la extensión CORS
from firebase_admin import credentials, db
from barcode import generate
from barcode.writer import ImageWriter

# Inicializar Firebase
cred = credentials.Certificate('stockero-40e02-firebase-adminsdk-zi40z-5de78aa07f.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://stockero-40e02-default-rtdb.firebaseio.com/'})
ref = db.reference('/')

app = Flask(__name__, static_url_path='/static')
CORS(app)  # Configura CORS

@app.route('/')
def index():
    return "Hello, this is the Flask backend!"

@app.route('/save_product', methods=['POST'])
def save_product():
    barcode = request.form.get('barcode')
    category = request.form.get('category').lower() 
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))

    # Utiliza la categoría como nombre del nodo en Realtime Database
    category_ref = ref.child('products').child(category)

    # Verifica si ya existe un producto con el mismo código de barras en esa categoría
    existing_product = category_ref.order_by_child('barcode').equal_to(barcode).get()

    if existing_product:
        # Si el producto ya existe, actualiza la cantidad y el precio
        product_id = list(existing_product.keys())[0]
        category_ref.child(product_id).update({
            'quantity': existing_product[product_id]['quantity'] + quantity,
            'price': price  # Puedes optar por actualizar el precio o mantener el original, según tus necesidades
        })
    else:
        # Si el producto no existe, crea uno nuevo
        unique_key = f'{category}'
        products_ref = ref.child('products').child(unique_key)
        new_product_ref = category_ref.push({
            'barcode': barcode,
            'quantity': quantity,
            'price': price
        })

    return "Product saved successfully!"

@app.route('/view_stock')
def view_stock():
    # Obtener todos los productos desde la base de datos
    all_products = ref.child('products').get()

    # Puedes procesar la lista de productos según tus necesidades
    # En este ejemplo, simplemente los pasamos a la plantilla

    return render_template('view_stock.html', products=all_products)

@app.route('/generate_barcode/<barcode>')
def generate_barcode(barcode):
    # Genera el código de barras y devuelve la imagen
    ean = generate('EAN13', barcode, writer=ImageWriter(), output='./static/barcodes')
    filename = ean.save(barcode)
    return "Barcode generated successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
