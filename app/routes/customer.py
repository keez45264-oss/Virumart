"""
Customer-facing routes: browse products, cart, checkout.
"""
import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, current_app, session, redirect, url_for, request

customer_bp = Blueprint('customer', __name__)

DELIVERY_CHARGE_PERCENT = 8  # 8% of order subtotal
MIN_DELIVERY_CHARGE = 10
MAX_DELIVERY_CHARGE = 50
FREE_DELIVERY_THRESHOLD = 300


def get_delivery_charge(subtotal):
    if subtotal >= FREE_DELIVERY_THRESHOLD:
        return 0
    charge = round(subtotal * DELIVERY_CHARGE_PERCENT / 100, 2)
    charge = max(MIN_DELIVERY_CHARGE, min(charge, MAX_DELIVERY_CHARGE))
    return charge


def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@customer_bp.route('/')
def home():
    conn = get_db_connection()

    search_query = request.args.get('q', '').strip()
    selected_category = request.args.get('category', '').strip()

    sql = 'SELECT * FROM products WHERE quantity_in_stock > 0'
    params = []

    if search_query:
        sql += ' AND name LIKE ?'
        params.append(f'%{search_query}%')

    if selected_category:
        sql += ' AND category = ?'
        params.append(selected_category)

    sql += ' ORDER BY name'
    products = conn.execute(sql, params).fetchall()

    categories = conn.execute(
        'SELECT DISTINCT category FROM products ORDER BY category'
    ).fetchall()

    conn.close()
    return render_template(
        'index.html', products=products, categories=categories,
        search_query=search_query, selected_category=selected_category
    )


@customer_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart
    return redirect(request.referrer or url_for('customer.home'))


@customer_bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('customer.cart'))


@customer_bp.route('/update-cart/<int:product_id>/<action>', methods=['POST'])
def update_cart(product_id, action):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        if action == 'increase':
            cart[product_id_str] += 1
        elif action == 'decrease':
            cart[product_id_str] -= 1
            if cart[product_id_str] <= 0:
                cart.pop(product_id_str)
    session['cart'] = cart
    return redirect(url_for('customer.cart'))


def get_cart_items_and_total(conn, cart_data):
    cart_items = []
    total = 0
    for product_id_str, quantity in cart_data.items():
        product = conn.execute(
            'SELECT * FROM products WHERE product_id = ?', (product_id_str,)
        ).fetchone()
        if product:
            subtotal = product['selling_price'] * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
    return cart_items, total


@customer_bp.route('/cart')
def cart():
    cart_data = session.get('cart', {})
    conn = get_db_connection()
    cart_items, total = get_cart_items_and_total(conn, cart_data)
    conn.close()
    delivery_charge = get_delivery_charge(total)
    grand_total = total + delivery_charge
    return render_template(
        'cart.html', cart_items=cart_items, total=total,
        delivery_charge=delivery_charge, grand_total=grand_total,
    )


@customer_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_data = session.get('cart', {})

    if not cart_data:
        return redirect(url_for('customer.home'))

    conn = get_db_connection()

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        delivery_address = request.form['delivery_address']

        cart_items, total = get_cart_items_and_total(conn, cart_data)
        delivery_charge = get_delivery_charge(total)
        grand_total = total + delivery_charge

        # Create the order (total_amount stored is the grand total, including delivery)
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.execute(
            '''INSERT INTO orders
               (customer_name, customer_phone, delivery_address, order_status, order_date, total_amount)
               VALUES (?, ?, ?, 'pending', ?, ?)''',
            (customer_name, customer_phone, delivery_address, order_date, grand_total)
        )
        order_id = cursor.lastrowid

        # Add order items + deduct stock + log as an online sale
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']

            conn.execute(
                '''INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
                   VALUES (?, ?, ?, ?)''',
                (order_id, product['product_id'], quantity, product['selling_price'])
            )

            conn.execute(
                'UPDATE products SET quantity_in_stock = quantity_in_stock - ? WHERE product_id = ?',
                (quantity, product['product_id'])
            )

            conn.execute(
                '''INSERT INTO sales (product_id, quantity_sold, sale_date, total_amount, source)
                   VALUES (?, ?, ?, ?, 'online')''',
                (product['product_id'], quantity, order_date, item['subtotal'])
            )

        conn.commit()
        conn.close()

        session['cart'] = {}  # empty the cart
        return redirect(url_for('customer.order_confirmation', order_id=order_id))

    cart_items, total = get_cart_items_and_total(conn, cart_data)
    conn.close()
    delivery_charge = get_delivery_charge(total)
    grand_total = total + delivery_charge
    return render_template(
        'checkout.html', cart_items=cart_items, total=total,
        delivery_charge=delivery_charge, grand_total=grand_total,
    )


@customer_bp.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    conn = get_db_connection()
    order = conn.execute(
        'SELECT * FROM orders WHERE order_id = ?', (order_id,)
    ).fetchone()
    conn.close()
    return render_template('order_confirmation.html', order=order)