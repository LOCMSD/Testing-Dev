from flask import Flask, request, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from my_package.calculator import add, subtract

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '326a5dfacad845a78f7d83325f375276'  # Thay bằng key bí mật của bạn
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Khởi tạo Flask-Admin với template tùy chỉnh
admin = Admin(app, name='Calculator Admin', template_mode='bootstrap4', base_template='custom_admin.html')

# Định nghĩa model cho bảng Calculation
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, nullable=False)
    b = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    operation = db.Column(db.String(50), nullable=False)

# Tùy chỉnh giao diện quản trị cho Calculation
class CalculationView(ModelView):
    column_list = ('id', 'a', 'b', 'result', 'operation')
    form_columns = ('a', 'b', 'result', 'operation')
    column_searchable_list = ('operation',)
    column_filters = ('operation',)

# Thêm model vào Flask-Admin
admin.add_view(CalculationView(Calculation, db.session))

# Route trang chính
@app.route('/')
def index():
    return render_template('index.html')

# Route để thực hiện phép cộng
@app.route('/add', methods=['GET', 'POST'])
def add_numbers():
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            result = add(a, b)
            calc = Calculation(a=a, b=b, result=result, operation="add")
            db.session.add(calc)
            db.session.commit()
            return render_template('result.html', result=result, operation="Add")
        except (ValueError, KeyError):
            return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    return render_template('add.html')

# Route để thực hiện phép trừ
@app.route('/subtract', methods=['GET', 'POST'])
def subtract_numbers():
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            result = subtract(a, b)
            calc = Calculation(a=a, b=b, result=result, operation="subtract")
            db.session.add(calc)
            db.session.commit()
            return render_template('result.html', result=result, operation="Subtract")
        except (ValueError, KeyError):
            return render_template('error.html', message="Invalid input. Please enter valid numbers.")
    return render_template('subtract.html')

# Khởi tạo database và chạy ứng dụng
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
