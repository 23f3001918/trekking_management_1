from flask import render_template
from utils.decorators import(login_required,role_required)

def register_user_routes(app):
    @app.route('/user/dashboard')
    @login_required
    @role_required('user')

    def user_dashboard():
        return render_template('user/dashboard.html')