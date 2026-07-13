from functools import wraps
from flask import flash, session,redirect,url_for

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'user_id' not in session:
            flash('Please login to access.')
            return redirect(url_for('login'))
        return func(*args,**kwargs)
    return wrapper

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if session.get('user_role') !=role:
                flash('Unauthorised Access.')
                return redirect(url_for('login'))
            return func(*args,**kwargs)
        return wrapper
    return decorator


