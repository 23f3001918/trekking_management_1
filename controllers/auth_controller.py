from flask import render_template,request,redirect,url_for,flash,session
from models.models import db,User

def register_routes(app):
    #=================================User Registration==============================================
    @app.route('/register',methods=['GET','POST'])
    def register():
        if request.method=='POST':
            email=request.form['email']
            existing_user=User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered.')
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
            flash('Registration Successful! please login.')
            return redirect(url_for('login'))
        return render_template('register.html')
        
    #=================================Login===================================================
    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method=='POST':
            email=request.form['email']
            password=request.form['password']
            user=User.query.filter_by(email=email,password=password).first()
            if user:
                if user.status=='blacklisted':
                    flash('Your account is blacklisted.')
                    return redirect (url_for('login'))
                session['user_id']=user.id
                session['user_role']=user.role
                session['name']=user.name

                if user.role=='admin':
                    return redirect(url_for('admin_dashboard'))
                    
                elif user.role=='staff':
                    return redirect(url_for('staff_dashboard'))
                    
                elif user.role=='user':
                    return redirect(url_for('user_dashboard'))
                    
            flash ('Invalid Credentials')
            return redirect(url_for('login'))
        return render_template('login.html')

    #===================================Logout=================================================================

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged Out Successfully.') 
        return redirect(url_for('login'))       
                    

