from flask import app, Flask, render_template,request,redirect,url_for,flash
from models.models import db,User,Trek,Booking,StaffProfile
from utils.decorators import login_required,role_required

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
        return render_template('admin/dashboard.html',
                               total_treks=total_treks,
                               total_users=total_users,
                               total_staff=total_staff,
                               total_bookings=total_bookings
                               )
    
    #==================================View All Treks===============================================
    @app.route('/admin/treks')
    @login_required
    @role_required('admin')
    def view_treks():
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
                duration_days=request.form['duration_days'],
                total_slots=request.form['total_slots'],
                available_slots=request.form['total_slots'],
                start_date=request.form['start_date'],
                end_date=request.form['end_date'],
                description=request.form['description'],
                price=request.form['price']
                )
            db.session.add(trek)
            db.session.commit()
            flash('Trek added successfully')
            return redirect(url_for('view_treks'))
        return render_template('admin/add_trek.html')


    #==========================================Edit Trek===================================================
    @app.route('/admin/trek/edit/<int:trek_id>',methods=['GET', 'POST'])
    @login_required
    @role_required('admin')
    def edit_trek(trek_id):
        trek=Trek.query.get_or_404(trek_id)
        if request.method=='POST':
            trek.name=request.form['name']
            trek.location=request.form['location']
            trek.difficulty=request.form['difficulty']
            trek.duration_days=request.form['duration_days']
            trek.total_slots=request.form['total_slots']
            trek.available_slots=request.form['available_slots']
            trek.start_date=request.form['start_date']
            trek.end_date=request.form['end_date']
            trek.description=request.form['description']
            trek.price=request.form['price']
            db.session.commit()
            flash('Trek updated successfully')
            return redirect(url_for('view_treks'))
        return render_template('admin/edit_trek.html',
                               trek=trek
                               )
    
    #==========================================Delete Trek===================================================
    @app.route('/admin/trek/delete/<int:trek_id>')
    @login_required
    @role_required('admin')
    def delete_trek(trek_id):
        trek = Trek.query.get_or_404(trek_id)
        db.session.delete(trek)
        db.session.commit()
        flash('Trek deleted successfully')
        return redirect(url_for('view_treks'))
    
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
        staffs=User.query.filter_by(role='staff').all()
        return render_template('admin/staffs.html',
                               staffs=staffs
                               )
    

    #========================================Add Staff===================================================
    @app.route('/admin/staff/add',methods=['GET','POST'])
    @login_required
    @role_required('admin')
    def add_staff():
        if request.method == 'POST':
            user = User(
                name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'],
                phone=request.form['phone'],
                role='staff'
            )
            db.session.add(user)
            db.session.commit()
            profile = StaffProfile(user_id=user.id,
                                   bio=request.form['bio'],
                                   experience_years=request.form['experience_years'],
                                   approval_status='approved'
                                   )
            db.session.add(profile)
            db.session.commit()
            flash('Staff added successfully')
            return redirect(url_for('view_staff'))
        return render_template('admin/add_staff.html')
    
    #========================================Delete Staff===================================================
    @app.route('/admin/staff/delete/<int:staff_id>')
    @login_required
    @role_required('admin')
    def delete_staff(staff_id):
        staff = User.query.get_or_404(staff_id)
        if staff.role!='staff':
            flash('Invalid staff member')
            return redirect(url_for('view_staff'))
        profile = StaffProfile.query.filter_by(user_id=staff.id).first()
        if profile:
            db.session.delete(profile)
        db.session.delete(staff)
        db.session.commit()
        flash('Staff removed successfully')
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
            flash('Staff assigned successfully')
            return redirect(url_for('view_treks'))
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
        flash('User blacklisted')
        return redirect(request.referrer)
    
    #========================================Activate User================================================================
    @app.route('/admin/activate/<int:user_id>')
    @login_required
    @role_required('admin')
    def activate_user(user_id):
        user = User.query.get_or_404(user_id)
        user.status = 'active'
        db.session.commit()
        flash('User activated')
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
    
    #=======================================Search=========================================================
    @app.route('/admin/search')
    @login_required
    @role_required('admin')
    def search():
        keyword = request.args.get('keyword','')
        treks = Trek.query.filter(db.or_(
            Trek.name.ilike(f'%{keyword}%'),
            Trek.id.cast(db.String).ilike(f'%{keyword}%'))
            ).all()
        users = User.query.filter(db.or_(
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
