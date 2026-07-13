from flask import app, Flask, render_template,request,redirect,url_for,flash
from models.models import db,User,Trek,Booking,StaffProfile
from utils.decorators import login_required,role_required
from datetime import datetime

def register_admin_routes(app):
    #=======================================Dashboard ===========================================
    @app.route('/admin/dashboard')
    @login_required
    @role_required('admin')
    def admin_dashboard():
        total_treks=Trek.query.count()
        total_users=User.query.filter_by(role='user').count()
        total_staff=User.query.filter_by(role='staff').count()
        total_bookings=Booking.query.count()
        recent_bookings=Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
        return render_template('admin/dashboard.html',
                               total_treks=total_treks,
                               total_users=total_users,
                               total_staff=total_staff,
                               total_bookings=total_bookings,
                               recent_bookings=recent_bookings
                               )
    
    #==================================View All Treks===============================================
    @app.route('/admin/treks')
    @login_required
    @role_required('admin')
    def admin_view_treks():
        treks=Trek.query.all()
        return render_template('admin/treks.html',
                               treks=treks
                               )
    
    #=======================================Add Trek=====================================================
    @app.route('/admin/trek/add',methods=['GET','POST'])
    @login_required
    @role_required('admin')
    def add_trek():
        if request.method=='POST':
            trek = Trek(
                name=request.form['name'],
                location=request.form['location'],
                difficulty=request.form['difficulty'],
                duration_days=int(request.form['duration_days']),
                total_slots=int(request.form['total_slots']),
                available_slots=int(request.form['total_slots']),
                start_date = datetime.strptime( request.form['start_date'], "%Y-%m-%d").date(),
                end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date(),
                description=request.form['description'],
                price=float(request.form['price'])
                )
            db.session.add(trek)
            db.session.commit()
            flash('Trek added successfully','success')
            return redirect(url_for('admin_view_treks'))
        return render_template('admin/add_trek.html')


    #==========================================Edit Trek===================================================
    @app.route('/admin/trek/edit/<int:trek_id>',methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def edit_trek(trek_id):
        trek=Trek.query.get_or_404(trek_id)
        if request.method == 'POST':
            trek.name = request.form['name']
            trek.location = request.form['location']
            trek.difficulty = request.form['difficulty']
            trek.duration_days = int(request.form['duration_days'])
            trek.total_slots = int(request.form['total_slots'])
            trek.available_slots = int(request.form['available_slots'])
            trek.start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
            trek.end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()
            trek.description = request.form['description']
            trek.price = float(request.form['price'])
            db.session.commit()

            flash('Trek updated successfully', 'success')
            return redirect(url_for('admin_view_treks'))
        return render_template('admin/edit_trek.html',trek=trek)
        

    #==========================================Delete Trek===================================================
    @app.route('/admin/trek/delete/<int:trek_id>')
    @login_required
    @role_required('admin')
    def delete_trek(trek_id):
        trek = Trek.query.get_or_404(trek_id)
        db.session.delete(trek)
        db.session.commit()
        flash('Trek deleted successfully','success')
        return redirect(url_for('admin_view_treks'))
    
    #==========================================View All Users===================================================
    @app.route('/admin/users')
    @login_required
    @role_required('admin')
    def view_users():
        users=User.query.filter_by(role='user').all()
        return render_template('admin/users.html',
                               users=users
                               )
    
    #=========================================View All Staff===================================================
    @app.route('/admin/staff')
    @login_required
    @role_required('admin')
    def view_staff():
        approved_staff = User.query.join(StaffProfile).filter(
            User.role == 'staff',
            StaffProfile.approval_status == 'approved'
        ).all()

        pending_staff = User.query.join(StaffProfile).filter(
            User.role == 'staff',
            StaffProfile.approval_status == 'pending'
        ).all()

        return render_template('admin/staffs.html',
                               approved_staff=approved_staff,
                               pending_staff=pending_staff
                               )
       
    
    #========================================View Staff Details===================================================
    @app.route('/admin/staff/<int:staff_id>')
    @login_required
    @role_required('admin')
    def view_staff_details(staff_id):
        staff = User.query.get_or_404(staff_id)
        if staff.role != 'staff':
            flash("Invalid staff member.",'error')
            return redirect(url_for('view_staff'))
        profile = StaffProfile.query.filter_by(user_id=staff.id).first()
        return render_template('admin/staff_details.html',
                               staff=staff,
                               profile=profile
                               )
        
        
    #========================================Delete Staff===================================================
    @app.route('/admin/staff/delete/<int:staff_id>')
    @login_required
    @role_required('admin')
    def delete_staff(staff_id):
        staff = User.query.get_or_404(staff_id)
        if staff.role!='staff':
            flash('Invalid staff member','error')
            return redirect(url_for('view_staff'))
        profile = StaffProfile.query.filter_by(user_id=staff.id).first()
        if profile:
            db.session.delete(profile)
        db.session.delete(staff)
        db.session.commit()
        flash('Staff removed successfully','success')
        return redirect(url_for('view_staff'))
    
    #======================================== Approve Staff ===========================================

    @app.route('/admin/staff/approve/<int:staff_id>')
    @login_required
    @role_required('admin')
    def approve_staff(staff_id):
        profile = StaffProfile.query.filter_by(
            user_id=staff_id
        ).first_or_404()
        profile.approval_status ='approved'
        profile.user.status ='active'
        db.session.commit()
        flash('Staff approved successfully.','success')
        return redirect(url_for('view_staff'))
        
    #========================================Trekking History===================================================
    @app.route('/admin/history')
    @login_required
    @role_required('admin')
    def trekking_history():
        history = Booking.query.filter_by(status='Completed').all()
        return render_template('admin/history.html',
                               history=history
                               )
    
    #========================================Assign Staff for Trek===================================================
    @app.route('/admin/trek/assign_staff/<int:trek_id>',methods=['GET','POST'])
    @login_required
    @role_required('admin')
    def assign_staff(trek_id):
        trek=Trek.query.get_or_404(trek_id)
        staffs=User.query.filter_by(role='staff').all()
        if request.method=='POST':
            trek.assigned_staff_id=request.form['staff_id']
            db.session.commit()
            flash('Staff assigned successfully','success')
            return redirect(url_for('admin_view_treks'))
        return render_template('admin/assign_staff.html',
                               trek=trek,
                               staffs=staffs
                               )
    
    #========================================Blacklist User=================================================================
    @app.route('/admin/blacklist/<int:user_id>')
    @login_required
    @role_required('admin')
    def blacklist_user(user_id):
        user=User.query.get_or_404(user_id)
        user.status='blacklisted'
        db.session.commit()
        flash('User blacklisted','warning')
        return redirect(request.referrer)
    
    #========================================Activate User================================================================
    @app.route('/admin/activate/<int:user_id>')
    @login_required
    @role_required('admin')
    def activate_user(user_id):
        user = User.query.get_or_404(user_id)
        user.status = 'active'
        db.session.commit()
        flash('User activated','success')
        return redirect(request.referrer)
    
    #=======================================View All Bookings====================================================================
    @app.route('/admin/bookings')
    @login_required
    @role_required('admin')
    def view_bookings():
        bookings = Booking.query.all()
        return render_template('admin/bookings.html',
                               bookings=bookings
                               )
    
    #=======================================Search============================================================================
    @app.route('/admin/search')
    @login_required
    @role_required('admin')
    def search():
        keyword = request.args.get('keyword','')
        treks = Trek.query.filter(db.or_(
            Trek.name.ilike(f'%{keyword}%'),
            Trek.id.cast(db.String).ilike(f'%{keyword}%'))
            ).all()
        
        users = User.query.filter(User.role == 'user',db.or_(
            User.name.ilike(f'%{keyword}%'),
            User.id.cast(db.String).ilike(f'%{keyword}%'))
            ).all()
        
        staffs = User.query.filter(User.role == 'staff',db.or_(
            User.name.ilike(f'%{keyword}%'),
            User.id.cast(db.String).ilike(f'%{keyword}%'))
            ).all()
        
        return render_template('admin/search_results.html',
                            treks=treks,
                            users=users,
                            staffs=staffs,
                            keyword=keyword
                            )
