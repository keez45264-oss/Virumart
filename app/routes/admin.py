"""
Admin routes: manage products, stock, view orders, view sales.
"""
import sqlite3
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, current_app, request, redirect, url_for

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = os.path.join('app', 'static', 'images', 'products')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_product_image(file, product_name):
    if file and file.filename and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        safe_name = secure_filename(product_name).lower().replace(' ', '_')
        filename = f"{safe_name}_{os.urandom(4).hex()}.{ext}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filename
    return None


def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@admin_bp.route('/')
def dashboard():
    conn = get_db_connection()
    low_stock = conn.execute(
        'SELECT * FROM products WHERE quantity_in_stock <= reorder_threshold'
    ).fetchall()
    total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    conn.close()
    return render_template('admin/dashboard.html', low_stock=low_stock, total_products=total_products)


@admin_bp.route('/products')
def products():
    conn = get_db_connection()
    all_products = conn.execute('SELECT * FROM products ORDER BY name').fetchall()
    conn.close()
    return render_template('admin/products.html', products=all_products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        cost_price = float(request.form['cost_price'])
        selling_price = float(request.form['selling_price'])
        quantity_in_stock = int(request.form['quantity_in_stock'])
        reorder_threshold = int(request.form['reorder_threshold'])

        image_file = request.files.get('image')
        image_filename = save_product_image(image_file, name)

        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO products
               (name, category, cost_price, selling_price, quantity_in_stock, reorder_threshold, image_path)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (name, category, cost_price, selling_price, quantity_in_stock, reorder_threshold, image_filename)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('admin.products'))

    return render_template('admin/add_product.html')


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        cost_price = float(request.form['cost_price'])
        selling_price = float(request.form['selling_price'])
        quantity_in_stock = int(request.form['quantity_in_stock'])
        reorder_threshold = int(request.form['reorder_threshold'])

        image_file = request.files.get('image')
        new_image_filename = save_product_image(image_file, name)

        if new_image_filename:
            conn.execute(
                '''UPDATE products SET name=?, category=?, cost_price=?, selling_price=?,
                   quantity_in_stock=?, reorder_threshold=?, image_path=? WHERE product_id=?''',
                (name, category, cost_price, selling_price, quantity_in_stock,
                 reorder_threshold, new_image_filename, product_id)
            )
        else:
            conn.execute(
                '''UPDATE products SET name=?, category=?, cost_price=?, selling_price=?,
                   quantity_in_stock=?, reorder_threshold=? WHERE product_id=?''',
                (name, category, cost_price, selling_price, quantity_in_stock, reorder_threshold, product_id)
            )
        conn.commit()
        conn.close()
        return redirect(url_for('admin.products'))

    product = conn.execute(
        'SELECT * FROM products WHERE product_id = ?', (product_id,)
    ).fetchone()
    conn.close()
    return render_template('admin/edit_product.html', product=product)


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
def orders():
    conn = get_db_connection()
    all_orders = conn.execute(
        'SELECT * FROM orders ORDER BY order_id DESC'
    ).fetchall()

    orders_with_items = []
    for order in all_orders:
        items = conn.execute(
            '''SELECT order_items.quantity, order_items.price_at_order, products.name
               FROM order_items
               JOIN products ON order_items.product_id = products.product_id
               WHERE order_items.order_id = ?''',
            (order['order_id'],)
        ).fetchall()
        orders_with_items.append({'order': order, 'line_items': items})

    conn.close()
    return render_template('admin/orders.html', orders_with_items=orders_with_items)


@admin_bp.route('/orders/update-status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    new_status = request.form['status']
    conn = get_db_connection()
    conn.execute(
        'UPDATE orders SET order_status = ? WHERE order_id = ?',
        (new_status, order_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('admin.orders'))
