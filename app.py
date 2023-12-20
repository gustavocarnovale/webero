import time
from flask import Flask, render_template, request, redirect, url_for,jsonify
import firebase_admin
from firebase_admin import credentials, db

# Inicializa Firebase
cred = credentials.Certificate('stockero-40e02-firebase-adminsdk-zi40z-5de78aa07f.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://stockero-40e02-default-rtdb.firebaseio.com/'})
ref = db.reference('/')

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product_form')
def product_form():
    return render_template('product_form.html')
    
@app.route('/save_product', methods=['POST'])
def save_product():
    barcode = request.form.get('barcode').lower() 
    category = request.form.get('category').lower() 
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))

    # Utiliza la categoría como nombre del nodo en Realtime Database
    category_ref = ref.child('products').child(category)

    # Verifica si ya existe un producto con el mismo código de barras en esa categoría
    existe = category_ref.order_by_child('barcode').equal_to(barcode).get()

    if existe:
        # Si el producto ya existe, actualiza la cantidad y el precio
        product_id = list(existe.keys())[0]
        category_ref.child(product_id).update({
            'quantity': existe[product_id]['quantity'] + quantity,
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

    return render_template('index.html')

@app.route('/view_stock')
def view_stock():
    # Obtener todos los productos desde la base de datos
    all_products = ref.child('products').get()

    # Puedes procesar la lista de productos según tus necesidades
    # En este ejemplo, simplemente los pasamos a la plantilla

    return render_template('view_stock.html', products=all_products)

@app.route('/sales')
def sales():
    # Lógica para obtener categorías y productos desde Firebase
    categories = ref.child('categories').get()
    products = ref.child('products').get()

    return render_template('sales.html', categories=categories, products=products)

@app.route('/get_product_info/<barcode>')
def get_product_info(barcode):
    # Lógica para obtener la información de un producto por su código de barras desde Firebase
    product_info = {}  # Asume que obtienes la información del producto desde Firebase según el código de barras

    return jsonify(product_info)


@app.route('/process_sale', methods=['POST'])
def process_sale():
    product_key = request.form.get('barcode')
    quantity = int(request.form.get('quantity'))

    # Lógica para restar del stock en Firebase
    # ...

    # Lógica para guardar la venta en Firebase
    sale_ref = ref.child('sales')
    sale_ref.push({
        'product_key': product_key,
        'quantity': quantity,
        'timestamp': time.time()  # Puedes usar la marca de tiempo para realizar un seguimiento de cuándo se realizó la venta
    })

    return redirect(url_for('sales'))

@app.route('/view_sales')
def view_sales():
    # Obtener datos de ventas desde Firebase
    sales_data = ref.child('sales').get()

    return render_template('view_sales.html', sales=sales_data)

@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.form.get('name')
    phone = request.form.get('phone')

    # Crea un nuevo cliente en la base de datos
    new_client_ref = ref.child('clients').push({
        'name': name,
        'phone': phone,
        'purchase_history': {}
    })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
