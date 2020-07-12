from flask import Flask, render_template
import joblib
from flask import Flask, render_template, request, redirect, url_for
from models.user import Db, User
from modules.dataForms import UserForm, passwordConfirmation, ChangeForm, GenerateForm
import sqlalchemy.dialects.postgresql.psycopg2
import hashlib
import random
import string
from flask_heroku import Heroku
app = Flask(__name__)
heroku = Heroku(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
Db.init_app(app)

@app.route('/')
def index():
    # Query all
    users = User.query.all()

    # Iterate and print
    for user in users:
        User.toString(user)

    return render_template("index.html", users=users)

# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            password = request.form['password']
            passhash = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
            new_user = User(first_name=first_name, age=age, passhash=passhash)
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)
# @route /adduser/<first_name>/<age>

@app.route('/adduser/<first_name>/<age>/<password>')
def addUserFromUrl(first_name, age, password):
    passhash = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
    Db.session.add(User(first_name=first_name, age=age, passhash=passhash))
    Db.session.commit()
    return redirect(url_for('index'))

@app.route('/viewuser/<userId>')
def viewUser(userId):
    users = User.query.all()
    for user in users:
        if (int(user.user_id) == int(userId)):
            return render_template("singleuser.html", user=user)

@app.route('/delete/<userId>', methods=['GET', 'POST'])
def deleteUser(userId):
    correctUser = User()
    users = User.query.all()
    for user in users:  # gets user object from all users based on user id
        if (int(user.user_id) == int(userId)):
            correctUser = user
            break
    passwordForm = passwordConfirmation()
    # If GET
    if request.method == 'GET':
        if correctUser.user_id:  # Makes sure there is a user with the url's id
            return render_template("delete.html", user=correctUser, form=passwordForm)
        else:
            return redirect(url_for('index'))
    # If POST
    else:
        if passwordForm.validate_on_submit():
            password = request.form['password']
            passhash = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
            if str(passhash) == str(correctUser.passhash):
                Db.session.delete(correctUser)
                Db.session.commit()
                return redirect(url_for('index'))
            return render_template('delete.html', user=correctUser, form=passwordForm, error=True)
        else:
            return render_template('delete.html', form=passwordForm)

@app.route('/changeInfo/<userId>',  methods=['GET', 'POST'])
def changeUserInfo(userId):
    correctUser = User()
    users = User.query.all()
    for user in users:  # gets user object from all users based on user id
        if (int(user.user_id) == int(userId)):
            correctUser = user
            break
    changeForm = ChangeForm()
    # If GET
    if request.method == 'GET':
        changeForm.age.default = correctUser.age
        changeForm.first_name.default = correctUser.first_name
        if correctUser.user_id:  # Makes sure there is a user with the url's id
            return render_template("change.html", user=correctUser, form=changeForm)
        else:
            return redirect(url_for('index'))
    # If POST
    else:
        if changeForm.validate_on_submit():
            
            password = request.form['password']
            passhash = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
            if str(passhash) == str(correctUser.passhash):
                if request.form.get('first_name'): correctUser.first_name = request.form['first_name']
                if request.form.get('age'): correctUser.age = int(request.form['age'])
                Db.session.commit()
                return redirect(url_for('index'))
            return render_template('change.html', user=correctUser, form=changeForm, error=True)
        else:
            return render_template('change.html', user=correctUser, form=changeForm)

@app.route('/generate',  methods=['GET', 'POST'])
def generate():
    form = GenerateForm()
    if request.method == 'GET':
        return render_template('generate.html', form=form)
    else:
        if form.validate_on_submit():
            password = 'TEST'
            passhash = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
            for i in range(int(request.form['numOfUsers'])):
                Db.session.add(User(first_name='TEST - '+ ''.join(random.choice(string.ascii_letters) for _ in range(4)), age=int(random.random()*10+13), passhash=passhash))
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('generate.html', form=form)
