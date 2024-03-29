# -*- coding: utf-8 -*-

# Файл отвечает за отображение HTML файлов, за передачу данных из формы в БД и другую логику

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditForm
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('info_college.html', title='Информация об КГБ ПОУ «Приморский колледж»')

@app.route('/regofapp')
def regofapp():
    return render_template('regofapp.html', title='Подать документы')

@app.route('/confidentiality')
def confidentiality():
    return render_template('confidentiality.html', title='Политика конфиденциальности')

@app.route('/cookie')
def cookie():
    return render_template('cookie.html', title='Условия обработки файлов cookie')

@app.route('/vacancy')
def vacancy():
    return render_template('vacancy.html', title='Вакансии')

@app.route('/admin')
@login_required
def admin():
    if current_user.admin == True:
        users = User.query.all()
        return render_template('admin.html', title='Список поступающих', users=users)
    else:
        flash('Ошибка! У Вас нет доступа к странице')
        return redirect(url_for('index'))

@app.route('/admin_analog')
@login_required
def admin_analog():
    if current_user.admin == True:
        users = User.query.all()
        return render_template('admin_analog.html', title='Карточка поступающих поступающих', users=users)
    else:
        flash('Ошибка! У Вас нет доступа к странице')
        return redirect(url_for('index'))

@app.route('/rating_cook')
@login_required
def rating_cook():
    users = User.query.order_by(User.gpa.desc()).all()
    return render_template('rating_cook.html', title='Списки поступающих | Повар', users=users)

@app.route('/rating_carp')
@login_required
def rating_carp():
    users = User.query.order_by(User.gpa.desc()).all()
    return render_template('rating_carp.html', title='Списки поступающих | Столяр', users=users)

@app.route('/rating_painter')
@login_required
def rating_painter():
    users = User.query.order_by(User.gpa.desc()).all()
    return render_template('rating_painter.html', title='Списки поступающих | Штукатур; Маляр строительный', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже вошли, зачем опять открываете страницу входа?')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id_reg=form.id_reg.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный идентификатор или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.')
    return redirect(url_for('index'))

@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    if current_user.admin == True:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(fullname=form.fullname.data, email=form.email.data, cook=form.is_cooker.data,
                        carp=form.is_carper.data, paint=form.is_painter.data, id_reg=form.id_reg.data,
                        gpa=form.gpa.data, phone=form.phone.data, docs=form.docs.data, admin=form.admin.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация прошла успешно')
            return redirect(url_for('admin'))
        return render_template('register.html', title='Регистрация абитуриента', form=form)
    else:
        flash('Ошибка! У Вас нет доступа к странице')
        return redirect(url_for('index'))

@app.route('/user/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.admin == True:
        user = User.query.filter_by(id=id).first()
        return render_template('delete_user.html', title='Удалить данные', user=user)
    flash('Удалить не получилось, нет доступа')
    return redirect(url_for('index'))

@app.route('/user/delete_yes/<int:id>')
@login_required
def delete_user_yes(id):
    if current_user.admin == True:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Пользователь удалён')
        return redirect(url_for('admin'))
    flash('Удалить не получилось, нет доступа')
    return redirect(url_for('index'))

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
  if current_user.admin:
    user = User.query.filter_by(id=id).first()
    form = EditForm(fullname=user.fullname,
            email=user.email, gpa=user.gpa, phone=user.phone, id_reg=user.id_reg)
    if form.validate_on_submit():
      user.fullname = form.fullname.data
      user.email = form.email.data
      user.gpa = form.gpa.data
      user.phone = form.phone.data
      user.id_reg = form.id_reg.data
      db.session.commit()
      flash('Данные изменены')
      return redirect(url_for('admin'))
    return render_template('edit_user.html', title='Изменить данные', form=form, user=user)
  flash('У Вас нет доступа к странице')
  return redirect(url_for('index'))