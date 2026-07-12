from flask import render_template,request,redirect,url_for,flash,session
from models.models import StaffProfile, db,User

def register_routes(app):
    #=================================User Registration==============================================
    @app.route('/register',methods=['GET','POST'])
    def register():
        if request.method=='POST':
            email=request.form['email']
            existing_user=User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered.','error')
                return redirect(url_for('register'))
            
            user=User(
                name=request.form['name'],
                email=email,
                password=request.form['password'],
                phone=request.form['phone'],
                role='user'
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration Successful! please login.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')
    
    #========================================================Staff Registration =======================================

    @app.route('/staff/register', methods=['GET', 'POST'])
    def staff_register():
        if request.method == 'POST':
            email = request.form['email']
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered.', 'error')
                return redirect(url_for('staff_register'))
            staff = User(
                name=request.form['name'],
                email=email,
                password=request.form['password'],
                phone=request.form['phone'],
                role='staff'
            )
            db.session.add(staff)
            db.session.commit()
            profile = StaffProfile(
            user_id=staff.id,
            bio='',
            experience_years=int(request.form['experience_years']),
            approval_status='pending'
        )
            db.session.add(profile)
            db.session.commit()
            flash('Registration successful. Wait for Admin approval.', 'success')
            return redirect(url_for('login'))
        return render_template('staff_register.html')
    
        
    #=================================Login===================================================
    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method=='POST':
            email=request.form['email']
            password=request.form['password']
            user=User.query.filter_by(email=email,password=password).first()
            if user:
                if user.status=='blacklisted':
                    flash('Your account is blacklisted.', 'warning')
                    return redirect (url_for('login'))
                session['user_id']=user.id
                session['user_role']=user.role
                session['name']=user.name

                if user.role=='admin':
                    return redirect(url_for('admin_dashboard'))
                    
                elif user.role == 'staff':
                    profile = StaffProfile.query.filter_by(user_id=user.id).first()
                    if not profile or profile.approval_status != 'approved':
                        flash('Your staff account is waiting for Admin approval.', 'error')
                        session.clear()
                        return redirect(url_for('login'))
                    return redirect(url_for('staff_dashboard'))   
                
                elif user.role=='user':
                    return redirect(url_for('user_dashboard'))
                    
            flash ('Invalid Credentials', 'error')
            return redirect(url_for('login'))
        return render_template('login.html')

    #===================================Logout=================================================================

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged Out Successfully.', 'success')
        return redirect(url_for('login'))       
                    

