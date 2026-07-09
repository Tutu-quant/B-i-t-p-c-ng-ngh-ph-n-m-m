from flask import Flask, render_template, request
from models.user import User
from models.attendance import Attendance
from models.database import connect_to_database

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
    return render_template('menu.html')


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