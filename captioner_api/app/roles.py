from flask import Blueprint, redirect, render_template, url_for
from flask_login import AnonymousUserMixin, current_user

from app.models import Role

roles = Blueprint('roles', __name__)

@roles.route('/roles')
def roles_list():

    user = current_user

    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for('auth.login'))  
    elif current_user.role.name == "USER":
        return redirect(url_for('main.index'))  

    roles = Role.query.all()

    return render_template('roles.html', user=user, roles=roles)