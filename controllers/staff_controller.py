from flask import render_template
from utils.decorators import(login_required,role_required)

def register_staff_routes(app):
    @app.route('/staff/dashboard')
    @login_required
    @role_required('staff')

    def staff_required():
        return render_template('staff/dashboard.html')