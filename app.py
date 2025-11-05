from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'minimart_secret_key'

# ✅ Sample products (use your real ones if needed)
products = [
    {'id': 1, 'name': 'Apple', 'price': 50, 'image': 'Apple.png'},
    {'id': 2, 'name': 'Banana', 'price': 20, 'image': 'Banana.jpg'},
    {'id': 3, 'name': 'Orange', 'price': 30, 'image': 'Orange.jpg'},
    {'id': 4, 'name': 'Mango', 'price': 80, 'image': 'Mango.jpg'}
]

@app.route('/')
def home():
    cart = session.get('cart', [])
    cart_count = sum(item['quantity'] for item in cart)
    return render_template('index.html', products=products, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', [])
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        existing_item = next((item for item in cart if item['id'] == product_id), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product['image'],
                'quantity': 1
            })
    session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    # Get cart items from session
    cart = session.get('cart', [])

    # Calculate total price safely (handles empty cart)
    total_price = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart)

    # Pass cart and total to template
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = max(1, quantity)
            break
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart'))



@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('home'))

# ✅ NEW: Place order route (restores missing functionality)
@app.route('/place_order', methods=['POST'])
def place_order():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('home'))

    total_price = sum(item['price'] * item['quantity'] for item in cart)
    session['order_summary'] = {
        'items': cart,
        'total_price': total_price
    }
    session['cart'] = []  # clear cart after order
    return redirect(url_for('order_summary'))

@app.route('/order_summary')
def order_summary():
    order = session.get('order_summary', {})
    items = order.get('items', [])
    total_price = order.get('total_price', 0)
    return render_template('order_summary.html', order=items, total_price=total_price)


if __name__ == '__main__':
    app.run(debug=True)
