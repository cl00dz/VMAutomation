from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import User
from app import db, login_manager
import pyotp

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        mfa_code = request.form.get('mfa_code')
        
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            # Check MFA if enabled
            if user.mfa_secret:
                totp = pyotp.TOTP(user.mfa_secret)
                if not mfa_code or not totp.verify(mfa_code):
                    flash('Invalid MFA code.', 'danger')
                    return render_template('auth/login.html', mfa_required=True, username=username)
            
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')
        
        user = User(username=username, email=email)
        user.password = password
        
        # Generate MFA secret
        user.mfa_secret = pyotp.random_base32()
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please set up MFA.', 'success')
        return redirect(url_for('auth.setup_mfa', user_id=user.id))
    
    return render_template('auth/register.html')

@auth_bp.route('/setup-mfa/<int:user_id>', methods=['GET', 'POST'])
def setup_mfa(user_id):
    """Set up MFA for a user."""
    user = User.query.get_or_404(user_id)
    
    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        db.session.commit()
    
    totp = pyotp.TOTP(user.mfa_secret)
    provisioning_url = totp.provisioning_uri(name=user.email, issuer_name="Proxmox VM Automation")
    
    if request.method == 'POST':
        mfa_code = request.form.get('mfa_code')
        
        if totp.verify(mfa_code):
            flash('MFA setup successful. You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid MFA code. Please try again.', 'danger')
    
    return render_template('auth/setup_mfa.html', provisioning_url=provisioning_url)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile."""
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if email and email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
            else:
                current_user.email = email
                db.session.commit()
                flash('Email updated.', 'success')
        
        if current_password and new_password:
            if not current_user.verify_password(current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
            else:
                current_user.password = new_password
                db.session.commit()
                flash('Password updated.', 'success')
    
    return render_template('auth/profile.html')

@auth_bp.route('/reset-mfa', methods=['GET', 'POST'])
@login_required
def reset_mfa():
    """Reset MFA for a user."""
    if request.method == 'POST':
        password = request.form.get('password')
        
        if current_user.verify_password(password):
            current_user.mfa_secret = pyotp.random_base32()
            db.session.commit()
            flash('MFA reset. Please set up your new MFA device.', 'success')
            return redirect(url_for('auth.setup_mfa', user_id=current_user.id))
        else:
            flash('Incorrect password.', 'danger')
    
    return render_template('auth/reset_mfa.html')
