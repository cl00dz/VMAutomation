from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page."""
    return render_template('dashboard.html')

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')
