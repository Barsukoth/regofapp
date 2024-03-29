# Файл отвечает за формы в проекте

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    id_reg = StringField('Идентификатор абитуриента/логин сотрудника', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить вход')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    fullname = StringField('Фамилия, имя, отчество', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    is_cooker = BooleanField('Повар')
    is_carper = BooleanField('Столяр')
    is_painter = BooleanField('Маляр строительный')
    id_reg = StringField('Идентификатор абитуриента/логин сотрудника', validators=[DataRequired()])
    gpa = FloatField('Средний балл аттестата', )
    phone = IntegerField('Контактный телефон')
    docs = BooleanField('Документы оригинал')
    admin = BooleanField('Сотрудник приёмной компании')
    submit = SubmitField('Зарегистрировать')

    # проверка уникальности почты
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Почта уже зарегистрирована.')

    # проверка уникальности логина/идентификатора абитуриента
    def validate_login(self, id_reg):
        user = User.query.filter_by(id_reg=id_reg.data).first()
        if user is not None:
            raise ValidationError('Абитуриент или сотрудник с таким идентификатором уже существует. Введите другой.')


class EditForm(FlaskForm):
    fullname = StringField('Фамилия, имя, отчество', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    gpa = FloatField('Средний балл аттестата')
    phone = IntegerField('Контактный телефон')
    id_reg = StringField('Идентификатор абитуриента/логин сотрудника', validators=[DataRequired()])
    submit = SubmitField('Изменить')