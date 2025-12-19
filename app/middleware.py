# app/middleware.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(allowed_roles):
    """
    Decorator to check if user has required role
    
    Usage:
        @dashboard.route('/doctor')
        @login_required
        @role_required(['doctor'])
        def doctor_dashboard():
            return render_template('doctor_dashboard.html')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please login first', 'danger')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in allowed_roles:
                flash('Access denied. You do not have permission to access this page.', 'danger')
                
                # Redirect based on user role
                if current_user.role == 'doctor':
                    return redirect(url_for('dashboard.doctor'))
                else:
                    return redirect(url_for('dashboard.patient'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def patient_only(f):
    """Shorthand for patient-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))
        
        if current_user.role != 'patient':
            flash('This page is for patients only', 'danger')
            return redirect(url_for('dashboard.doctor'))
        
        return f(*args, **kwargs)
    return decorated_function

def doctor_only(f):
    """Shorthand for doctor-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))
        
        if current_user.role != 'doctor':
            flash('This page is for doctors only', 'danger')
            return redirect(url_for('dashboard.patient'))
        
        return f(*args, **kwargs)
    return decorated_function