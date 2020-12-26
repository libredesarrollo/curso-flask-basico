#from my_app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from werkzeug.exceptions import abort
from sqlalchemy.sql.expression import not_,or_

from flask_login import login_required
from flask_user import roles_required
from flask_user.forms import RegisterForm,ChangeUsernameForm

from flask_mail import Message
from flask_babel import gettext

from my_app import db, rol_admin_need,mail, app, get_locale
from my_app.auth.model.user import User, Role, UserRoles
from my_app import user_manager
from my_app.product.models import CustomChangeUsernameForm
from my_app.product import root

from collections import namedtuple

import flask_login

userBp = Blueprint('usercrud',__name__, url_prefix=root)
global rol


@userBp.before_request
@login_required
#@rol_admin_need
@roles_required('Admin')
def constructor():
   global rol

   if flask_login.current_user.has_roles('Superadmin'):
      rol = 'Admin'
   else:
      rol = 'Regular'


@userBp.route('/user')
@userBp.route('/user/<int:page>')
def index(page=1):
   global rol
   """users = User.query\
   .join(UserRoles, UserRoles.user_id==User.id)\
   .join(Role,UserRoles.role_id==Role.id)\
   .filter(Role.name=='Admin')\
   .paginate(page,5)"""


   #print(User.roles.any(Role.name=='Admin'))
   users = User.query.filter(User.roles.any(Role.name==rol)).paginate(page,5)

   return render_template('dashboard/user/index.html', users=users)


@userBp.route('user/create', methods=('GET', 'POST'))
def create():
   global rol
   form = RegisterForm() #meta={'csrf':False}
   if form.validate_on_submit():
      
      #crear usuario
      username = request.form['username']
      password = user_manager.hash_password(request.form['password'])
      email = request.form['email']

      # crear usuario
      user = User(username=username, password=password, email=email)

      # asignar el rol
      rol = Role.query.filter_by(name=rol).one()
      user.roles.append(rol)

      db.session.add(user)
      db.session.commit()
      flash("Usuario creado con éxito")
      return redirect(url_for('usercrud.create'))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('dashboard/user/create.html',form=form)

@userBp.route('user/update-username/<int:id>', methods=('GET', 'POST'))
def update(id):
   user = User.query.get_or_404(id)

   form = CustomChangeUsernameForm() #meta={'csrf':False}

   if request.method == 'GET':
      form.new_username.data = user.username

   if form.validate_on_submit():
      
      #actualizar usuario
      user.username = request.form['new_username']

      db.session.add(user)
      db.session.commit()
      flash("Usuario actualizado con éxito")
      return redirect(url_for('usercrud.update',id=user.id))

   if form.errors:
      flash(form.errors,'danger')

   return render_template('dashboard/user/update.html',form=form,user=user)

@userBp.route('user/delete/<int:id>')
def delete(id):
   user = User.query.get_or_404(id)   

   db.session.delete(user)
   db.session.commit()
   flash("Usuario eliminado con éxito")

   return redirect(url_for('usercrud.index'))