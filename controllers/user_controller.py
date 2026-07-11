from flask import render_template, session, redirect, url_for, flash, request
from models.models import db, User, Trek, Booking
from utils.decorators import login_required, role_required

def register_user_routes(app):

    #============================================== User Dashboard =================================================

    @app.route('/user/dashboard')
    @login_required
    @role_required('user')
    def user_dashboard():
        open_treks=Trek.query.filter_by(status='Open').all()
        bookings=Booking.query.filter_by(user_id=session['user_id']).all()
        return render_template('user/dashboard.html',
                           open_treks=open_treks,
                           bookings=bookings
                           )

    #============================================View Available Treks ========================================
    
    @app.route('/user/treks')
    @login_required
    @role_required('user')
    def view_treks():
        difficulty=request.args.get('difficulty')
        location=request.args.get('location')
        query=Trek.query.filter_by(status='Open')
        if difficulty:
            query=query.filter(Trek.difficulty == difficulty)
        if location:
            query=query.filter(Trek.location.ilike(f'%{location}%'))
        treks=query.all()
        return render_template('user/treks.html',
                               treks=treks
                               )
    
    #========================================Book Trek===========================================

    @app.route('/user/book/<int:trek_id>')
    @login_required
    @role_required('user')
    def book_trek(trek_id):
        user_id=session['user_id']
        trek=Trek.query.get_or_404(trek_id)
        if trek.status!='Open':
            flash('Trek is not open for booking')
            return redirect(url_for('view_treks'))
        if trek.available_slots <= 0:
            flash('No slots available')
            return redirect(url_for('view_treks'))
        existing_booking = Booking.query.filter(
            Booking.user_id == user_id,
            Booking.trek_id == trek_id,
            Booking.status != 'Cancelled'
            ).first()
        
        if existing_booking:
            flash('You have already booked this trek')
            return redirect(url_for('view_treks'))
        booking=Booking(user_id=user_id,
                          trek_id=trek_id,
                          total_amount=trek.price,
                          payment_status='pending'
                          )
        trek.available_slots-=1
        db.session.add(booking)
        db.session.commit()
        flash('Trek booked successfully')
        return redirect(url_for('user_bookings'))
    
     #=========================== My Bookings ========================================

    @app.route('/user/bookings')
    @login_required
    @role_required('user')
    def user_bookings():
        bookings=Booking.query.filter_by(user_id=session['user_id']).all()
        return render_template('user/bookings.html',
                               bookings=bookings
                               )
    
    #============================Cancel Booking============================================================

    @app.route('/user/booking/cancel/<int:booking_id>')
    @login_required
    @role_required('user')
    def cancel_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if booking.user_id != session['user_id']:
            flash('Unauthorized access')
            return redirect(url_for('user_bookings'))
        if booking.status != 'Booked':
            flash('Only booked treks can be cancelled')
            return redirect(url_for('user_bookings'))
        booking.status = 'Cancelled'
        booking.trek.available_slots += 1
        db.session.commit()
        flash('Booking cancelled successfully')
        return redirect(url_for('user_bookings'))
    
    
    #=========================== Trek History =======================================

    @app.route('/user/history')
    @login_required
    @role_required('user')
    def trek_history():
        history=Booking.query.filter_by(user_id=session['user_id'],status='Completed').all()
        return render_template('user/history.html',
                               history=history
                               )

    #=========================== User Profile =======================================

    @app.route('/user/profile')
    @login_required
    @role_required('user')
    def user_profile():
        user=User.query.get_or_404(session['user_id'])
        return render_template('user/profile.html',
                               user=user
                               )

    #=========================== Update Profile =====================================

    @app.route('/user/profile/update', methods=['POST'])
    @login_required
    @role_required('user')
    def update_profile():
        user=User.query.get_or_404(session['user_id'])
        name = request.form.get('name')
        phone = request.form.get('phone')
        if not name or not phone:
            flash('All fields are required')
            return redirect(url_for('user_profile'))
        user.name = name
        user.phone = phone
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('user_profile'))
    