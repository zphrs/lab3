## Lab 3

Welcome! This week we will be connecting to a Postgres database using models to for CRUD operations.

1. [PostgreSQL](https://www.postgresql.org/): The World's Most Advanced Open Source Relational Database
    + Follow the tutorials: [installation](https://www.postgresqltutorial.com/install-postgresql/) and [connection](https://www.postgresqltutorial.com/connect-to-postgresql-database/)
    + Download the latest version of Postgres from [EDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads), which includes: PostgresSQL Server, pgAdmin 4, Stack Builder, Command Line Tools
        + OR, Mac users may want to use [Homebrew](https://wiki.postgresql.org/wiki/Homebrew) for installation.
        + OR, Another Mac alternative is to dowload [Postgres App](https://postgresapp.com/)
    + Confirm success: 
        + For EDB, by opening SQL Shell (psql), and entering: `SELECT version();`
        + For homebrew, in terminal: `psql postgres`
        + For Postgres App, open application.
    + PSQl commands:
        + List all databases: `\d`
        + List all schemas: `\dn`
        + List all tables: `\dt`
        + List all users: `\du`
        + Connect: `\c`
        + Quit: `\q`
    + Create usersdb database:
        + Create: `CREATE DATABASE usersdb;`
        + Connect: `\c usersdb;`
        + Type `CREATE TABLE users(user_id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, age INT NOT NULL);`
        + Confirm table creation: `SELECT * FROM users;`
        + Insert user: `INSERT INTO users(first_name, age) VALUES ('Zona', 35);`
      
2. Build a model for your usersdb
    + Create a directory 'models' and add a new file 'user.py'.
    + Import [Flask SqlAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/): ` pip install flask-sqlalchemy`
    + Install [Psycopg2](https://www.psycopg.org/docs/): `pip install psycopg2`
        + If error, add to PATH (or equivalent for configuration): `export PATH="/Library/PostgreSQL/12/bin/:$PATH"`
        + If another error, `pip install psycopg2-binary`
    + Add imports, db init and User class to user.py
        ```
        from flask_sqlalchemy import SQLAlchemy
        
        # Create DB instance
        db = SQLAlchemy()
        
        
        class User(db.model):
            # Fields
            __tablename__ = 'users'
            user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            first_name = db.Column(db.String(64), nullable=False)
            age = db.Column(db.Integer, nullable=False)
        
            # toString
            def toString(self):
                print(f"{self.user_id}: {self.first_name} ({self.age})")
        ```
    + Create an html template form 'adduser.html':
        ```
        <h1>Add user:</h1>
        <form class="user-form" method="POST" action="/adduser">
            {{ form.hidden_tag() }}
            <div class="user-form-group">
                {{ form.first_name.label }}:
                {{ form.first_name }}
                {% if form.first_name.errors %}
                    {% for error in form.first_name.errors %}
                        <p class="user-error-message">{{ error }}</p>
                    {% endfor %}
                {% endif %}
            </div>
            <div class="user-form-group">
                {{ form.age.label }}:
                {{ form.age }}
                {% if form.age.errors %}
                    {% for error in form.age.errors %}
                        <p class="user-error-message">{{ error }}</p>
                    {% endfor %}
                {% endif %}
            </div>
            <div class="user-form-submit">
                {{ form.submit }}
            </div>
        </form>
        ```
    
3. Build a user form
    + Create a directory 'modules' and add a new file 'userform.py'.
    + Install [Flask WTF](https://flask-wtf.readthedocs.io/en/stable/): `pip install flask-wtf;`
    + Add imports and UserForm class to userform.py
        ```
        from flask_wtf import FlaskForm
        from wtforms import StringField, IntegerField, SubmitField
        from wtforms.validators import DataRequired
        
        
        class UserForm(FlaskForm):
        first_name = StringField('First Name', validators=[DataRequired()])
        age = IntegerField('Age', validators=[DataRequired()])
        submit = SubmitField('Enter')
        
        ```

4. Connect the database with your Flask app.
    + In 'app.py' add/update import statements for your user model:
        ```
        from flask import Flask, render_template, request, redirect, url_for
        from models.user import Db, User
        from modules.userform import UserForm
        ```
    + Also after you initialize your app, configure and connect the db: 
        ```
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/usersdb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.secret_key = "s14a-key"
        Db.init_app(app)
        ```
      
6. Implementing CRUD
    + Create a '/' route with some logic (READ):
        ```
        @app.route('/')
        def index():
        # Query all
        users = User.query.all()
        
        # Iterate and print
        for user in users:
        User.tostring(user)
        
        return render_template("index.html")
        ```
    + Create a '/adduser' route with GET and POST methods (CREATE):
        ```
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
                new_user = User(first_name=first_name, age=age)
                Db.session.add(new_user)
                Db.session.commit()
                return redirect(url_for('index'))
            else:
                return render_template('adduser.html', form=form)
        ```
    + Expand route, '/adduser/<first_name>/<age>', to add users based on url parameters":
        ```
        # @route /adduser/<first_name>/<age>
        @app.route('/adduser/<first_name>/<age>')
        def addUserFromUrl(first_name, age):
            Db.session.add(User(first_name=first_name, age=age))
            Db.session.commit()
            return redirect(url_for('index'))
        ```
    
7. TASKS / TODOS / HW
    1. At route '/', show (read) all users in browser.
    2. Create a read route for an individual user.
    3. Create a route to delete a user by id.
    4. Create a route to update a user's name or age
    5. Create a route that can generate mock data of any amount (names can be nonsense).
    6. Improve the styling of your site.
    7. (EC). Introduce validation features that require user confirmation for deleting/updating.
   