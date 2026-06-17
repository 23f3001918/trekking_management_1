from flask import render_template
from utils.decorators import (login_required,role_required)

def register_admin_routes(app):
    @app.route('/admin/dashboard')
    @login_required
    @role_required('admin')

    def admin_dashboard():
        return render_template('admin/dashboard.html')