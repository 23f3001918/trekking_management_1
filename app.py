from flask import Flask 
from models.models import db,User,Trek,Booking,StaffProfile

app= Flask(__name__)
app.config['SECRET_KEY']='secretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trekking.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to Trekking Management System"

if __name__=='__main__':
    app.run(debug=True)