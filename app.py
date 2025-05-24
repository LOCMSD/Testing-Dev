from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

# Định nghĩa model (ví dụ: lưu kết quả phép tính từ calculator)
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.Float, nullable=False)
    b = db.Column(db.Float, nullable=False)
    result = db.Column(db.Float, nullable=False)
    operation = db.Column(db.String(50), nullable=False)

# Thêm model vào Flask-Admin
admin.add_view(ModelView(Calculation, db.session))

# Tạo route cơ bản
@app.route('/')
def index():
    return "Welcome to Flask-Admin Demo!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tạo database
    app.run(debug=True)