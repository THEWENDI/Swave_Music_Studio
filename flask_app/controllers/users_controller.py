
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/contact',methods=['POST'])
def contact():

    if not User.validate_contact(request.form):
        return redirect("/error")
    data ={ 
        "name": request.form['name'],
        "email": request.form['email'],
        "message": request.form['message']
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect("/submited")

@app.route('/edit/<int:id>')
def edit_contact(id):
    data = {
        "id":id
    }
    return render_template("edit.html",edit=User.get_by_id(data))

@app.route('/update/contact',methods=['POST'])
def update_contact():
    if not User.validate_contact(request.form):
        return redirect(f"/edit/{request.form['id']}")
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "message": request.form['message'],
        "id": request.form['id']
        # make sure to add the id for update
    }
    User.update(data)
    return redirect('/submited')

@app.route('/destroy/<int:id>')
def destroy_contact(id):
    data = {
        "id":id
    }
    User.destroy(data)
    return redirect('/')

@app.route('/submited')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id':session['user_id']
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
    }
    return render_template("submited.html",user=User.get_by_id(data))

@app.route('/error')
def error():
    return render_template('error.html')