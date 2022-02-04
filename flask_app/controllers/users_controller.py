
from flask import render_template,redirect,session,request, flash
from flask_app import app
from tkinter import messagebox
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/contact',methods=['POST'])
def register():

    if not User.validate_contact(request.form):
        return redirect("/error")
    data ={ 
        "name": request.form['name'],
        "email": request.form['email'],
        "message": request.form['message']
    }
    id = User.save(data)
    session['user_id'] = id
    # messagebox.showinfo("Title", "a Tk MessageBox")
    return redirect("/submited")

@app.route('/login',methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_by_email(request.form)
    session['user_id'] = user.id
    # ['user_id'] user_id just a var you make , make sure to use the same var name 
    return redirect('/dashboard')

@app.route('/submited')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id':session['user_id']
        # ['user_id'] user_id just a var you make , make sure to use the same var name 
    }
    return render_template("submited.html",user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/contact/<id>')
def show_contact(id):
    # if 'user_id' not in session:
    #     return redirect('/logout')
    data ={
        'id':session['user_id']
        # ['user_id'] user_id just a var you make , make sure to use the same var name 
    }
    return render_template("submited.html",user=User.get_by_id(data))

@app.route('/error')
def error():
    return render_template('error.html')