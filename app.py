from flask import Flask, render_template, request, jsonify, redirect, url_for
from models.user import User
from models.attendance import Attendance
from models.database import connect_to_database
from models.order import Order

app = Flask(__name__)


try:
    db_connection = connect_to_database()
    app.config['DB_CONNECTION'] = db_connection
except Exception as error:
    db_connection = None
    app.config['DB_CONNECTION_ERROR'] = str(error)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/customer_login')
def customer_login():
    return render_template('customer_login.html')


@app.route('/customer_register')
def customer_register():
    return render_template('customer_register.html')


@app.route('/admin_login')
def admin_login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        User.register(
            username=username,
            email=email,
            phone=phone,
            password=password,
            confirm_password=confirm_password
        )

    return render_template('register.html')


@app.route('/menu')
def menu():
    conn = connect_to_database()
    if conn is None:
        items = []
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ItemID, ItemName, Description, Price, ImageURL, Status FROM MenuItems ORDER BY ItemID")
            rows = cursor.fetchall()
            items = [
                {
                    'item_id': row[0],
                    'item_name': row[1],
                    'description': row[2],
                    'price': float(row[3]) if row[3] is not None else 0.0,
                    'image_url': row[4],
                    'status': row[5],
                }
                for row in rows
            ]
        finally:
            conn.close()
    return render_template('menu.html', items=items)


@app.route('/api/menu')
def api_menu():
    conn = connect_to_database()
    if conn is None:
        return jsonify([])
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ItemID, ItemName, Description, Price, ImageURL, Status FROM MenuItems ORDER BY ItemID")
        rows = cursor.fetchall()
        return jsonify([
            {
                'item_id': row[0],
                'item_name': row[1],
                'description': row[2],
                'price': float(row[3]) if row[3] is not None else 0.0,
                'image_url': row[4],
                'status': row[5],
            }
            for row in rows
        ])
    finally:
        conn.close()


@app.route('/api/orders', methods=['POST'])
def create_order_api():
    payload = request.get_json(silent=True) or {}
    items = payload.get('items', [])
    customer_id = payload.get('customer_id')
    table_id = payload.get('table_id')
    employee_id = payload.get('employee_id')
    reservation_id = payload.get('reservation_id')
    discount_percent = payload.get('discount_percent', 0)

    if not customer_id or not table_id:
        return jsonify({'success': False, 'message': 'Thiếu customer_id hoặc table_id'}), 400

    try:
        order = Order.create_order(
            customer_id=customer_id,
            table_id=table_id,
            employee_id=employee_id,
            reservation_id=reservation_id,
            items=items,
            discount_percent=discount_percent,
            status='Pending'
        )
        return jsonify({'success': True, 'order': order.to_dict()})
    except Exception as exc:
        return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/orders')
def list_orders_api():
    try:
        orders = Order.get_all_orders()
        return jsonify({'success': True, 'orders': [o.to_dict() for o in orders]})
    except Exception as exc:
        return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/api/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status_api(order_id):
    payload = request.get_json(silent=True) or {}
    status = payload.get('status')
    try:
        success = Order.update_status(order_id, status)
        if success:
            return jsonify({'success': True, 'order_id': order_id, 'status': status})
        return jsonify({'success': False, 'message': 'Cập nhật thất bại'}), 400
    except Exception as exc:
        return jsonify({'success': False, 'message': str(exc)}), 500


@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/attendance')
def attendance():
    attendance = Attendance(employee_id=1)
    attendance.check_in(time=None)
    return "Attendance checked", 200



if __name__ == '__main__':
    app.run(debug=True)