from flask import Blueprint, render_template
from app.models import Vehicle
from flask_login import current_user

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    vehicles = Vehicle.query.all()
    user_first_name = current_user.first_name if current_user.is_authenticated else None
    return render_template('index.html', vehicles=vehicles, user_first_name=user_first_name)

@site.route('/profile')
def profile():
    return render_template('profile.html')
