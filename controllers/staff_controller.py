from flask import render_template,session,redirect,url_for,flash,request
from models.models import db,Trek,Booking,StaffProfile
from utils.decorators import login_required,role_required

def register_staff_routes(app):
    #====================================== Dashboard =================================================================
    @app.route('/staff/dashboard')
    @login_required
    @role_required('staff')
    def staff_dashboard():
        staff_id = session['user_id']
        assigned_treks = Trek.query.filter_by(assigned_staff_id=staff_id).all()
        total_treks = len(assigned_treks)
        total_trekkers = 0
        for trek in assigned_treks:
            total_trekkers += len(trek.bookings)
        open_treks = Trek.query.filter_by(assigned_staff_id=staff_id,
                                          status='Open'
                                          ).count()
        completed_treks = Trek.query.filter_by(assigned_staff_id=staff_id,
                                               status='Completed'
                                               ).count()
        return render_template('staff/dashboard.html',
                               total_treks=total_treks,
                               total_trekkers=total_trekkers,
                               open_treks=open_treks,
                               completed_treks=completed_treks,
                               assigned_treks=assigned_treks
                               )
    
    #====================================== Assigned Treks =====================================================================
    @app.route('/staff/treks')
    @login_required
    @role_required('staff')
    def assigned_treks():
        treks = Trek.query.filter_by(assigned_staff_id=session['user_id']).all()
        return render_template('staff/assigned_treks.html',
                               treks=treks
                               )
    
        
    #====================================== Trek Details ==================================================================
    @app.route('/staff/trek/<int:trek_id>')
    @login_required
    @role_required('staff')
    def trek_details(trek_id):
        trek = Trek.query.get_or_404(trek_id)
        if trek.assigned_staff_id != session['user_id']:
            flash('You are not authorized to manage this trek')
            return redirect(url_for('assigned_treks'))
        participant_count = Booking.query.filter_by(trek_id=trek.id).count()
        return render_template('staff/trek_details.html',
                               trek=trek,
                               participant_count=participant_count
                               )
    
    #====================================== Update Available Slots ==============================================
    @app.route('/staff/trek/<int:trek_id>/slots',methods=['GET','POST'])
    @login_required
    @role_required('staff')
    def update_slots(trek_id):
        trek = Trek.query.get_or_404(trek_id)
        if trek.assigned_staff_id != session['user_id']:
            flash('Unauthorized Access')
            return redirect(url_for('assigned_treks'))
        if request.method == 'POST':
            trek.available_slots = int(request.form['available_slots'])
            db.session.commit()
            flash('Available slots updated successfully')
            return redirect(url_for('trek_details',
                                    trek_id=trek.id)
                                    )
        return render_template('staff/update_slots.html',
                               trek=trek
                               )
    
    #====================================== Update Trek Status =======================================
    @app.route('/staff/trek/<int:trek_id>/status',methods=['GET','POST'])
    @login_required
    @role_required('staff')
    def update_trek_status(trek_id):
        trek = Trek.query.get_or_404(trek_id)
        if trek.assigned_staff_id != session['user_id']:
            flash('Unauthorized Access')
            return redirect(url_for('assigned_treks'))
        if request.method == 'POST':
            trek.status = request.form['status']
            db.session.commit()
            flash('Trek status updated successfully')
            return redirect(url_for('trek_details',
                                    trek_id=trek.id)
                                    )
        return render_template('staff/update_status.html',
                               trek=trek
                               )  
    
    #====================================== View Participants ==============================================
    @app.route('/staff/trek/<int:trek_id>/participants')
    @login_required
    @role_required('staff')
    def view_participants(trek_id):
        trek = Trek.query.get_or_404(trek_id)
        if trek.assigned_staff_id != session['user_id']:
            flash('Unauthorized Access')
            return redirect(url_for('assigned_treks'))
        bookings = Booking.query.filter_by(
            trek_id=trek.id
        ).all()
        return render_template('staff/participants.html',
                               trek=trek,
                               bookings=bookings
                               )
    
    #=============================================Update Staff Profile ===================================================
    @app.route('/staff/profile',methods=['GET','POST'])
    @login_required
    @role_required('staff')
    def staff_profile():
        profile = StaffProfile.query.filter_by( user_id=session['user_id']).first()
        if request.method == 'POST':
            profile.bio = request.form['bio']
            profile.experience_years = int(
                request.form['experience_years']
            )
            db.session.commit()
            flash('Profile updated successfully')
            return redirect(url_for('staff_profile'))
        return render_template('staff/profile.html',
                               profile=profile
                               )
        

    