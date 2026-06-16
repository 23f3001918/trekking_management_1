from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    role=db.Column(db.String(30),nullable=False,default='user')                #admin/staff/user
    status=db.Column(db.String(20),nullable=False,default='active')    #active/blacklisted
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    bookings=db.relationship('Booking',backref='user',lazy=True)


class StaffProfile(db.Model):
    __tablename__='staff_profiles'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    bio=db.Column(db.Text,default='')
    experience_years=db.Column(db.Integer,default=0)
    approval_status=db.Column(db.String(20),default='pending')              #pending/approved/rejected
    user=db.relationship('User',backref=db.backref('staff_profile',uselist=False))


class Trek(db.Model):
    __tablename__='treks'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(150),nullable=False)
    difficulty=db.Column(db.String(20),nullable=False)         #easy/moderate/hard
    duration_days=db.Column(db.Integer,nullable=False)
    total_slots=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    assigned_staff_id=db.Column(db.Integer,db.ForeignKey('users.id'), nullable=True)
    status=db.Column(db.String(20),default='Pending')              #Pending/Approved/Open/Closed/Completed
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date,nullable=False)
    description=db.Column(db.Text,default='')
    price=db.Column(db.Float,default=0.0)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    assigned_staff=db.relationship('User',foreign_keys=[assigned_staff_id],backref='assigned_treks')
    bookings=db.relationship('Booking',backref='trek',lazy=True)



class Booking(db.Model):
    __tablename__ ='bookings'

    id= db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey('treks.id'),nullable=False)
    booking_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(20),default='Booked')                #Booked/Cancelled/Completed
    participants=db.Column(db.Integer,default=1)
    total_amount=db.Column(db.Float,default=0.0)






