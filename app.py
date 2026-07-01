from flask import Flask,render_template,request,url_for,redirect
from models.models import db,User,Trek,Booking,StaffProfile
from controllers.auth_controller import register_routes
from controllers.admin_controller import register_admin_routes
from controllers.staff_controller import register_staff_routes
from controllers.user_controller import register_user_routes

app= Flask(__name__)
app.config['SECRET_KEY']='trek-secret-key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trekking.db'

db.init_app(app)
register_routes(app)
register_admin_routes(app)
register_staff_routes(app)      
register_user_routes(app)

with app.app_context():
    db.create_all()
    admin=User.query.filter_by(role='admin').first()

    if not admin:
        admin=User(name='admin',
                   email='admin@gmail.com',
                   password='admin123',
                   phone='1234567890',
                   role='admin'
                   )
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)