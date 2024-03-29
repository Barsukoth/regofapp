# Файл отвечает за структуру баз данных

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Таблица пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # cook, carp и print отвечают за направление образовательной программы: Повар, Столяр и Маляр соответственно
    cook = db.Column(db.Boolean, index=True)
    carp = db.Column(db.Boolean, index=True)
    paint = db.Column(db.Boolean, index=True)
    id_reg = db.Column(db.String(32), index=True)
    gpa = db.Column(db.Float, index=True)
    docs = db.Column(db.Boolean, index=True)
    phone = db.Column(db.Integer, index=True)
    # Значение используеся для определения сотрудника приёмной коммиссии
    admin = db.Column(db.Boolean, index=True)

    # Функция по созданию хэша пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Функция по расшифровке хэша пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# функция для Flask-login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))