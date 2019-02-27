from flask import render_template, url_for, flash, redirect, request #add import for : request

from blog_app import app, db, bcrypt #added import for : db, bcrypt
from blog_app.forms  import RegistrationForm, LoginForm

#import the database models here
from blog_app.models import User, Post

from flask_login import login_user, current_user, logout_user, login_required # add import for: current_user and logout_user, and login_required


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        #hash and verify p/w
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        #create and adding a  new user after p/w hashing and verification
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # flash(f'Account created for {form.username.data}!', 'success')
        flash('Your account has been created! you are now able to log in' , 'success')

        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        #     flash('You have been logged in!', 'success')
        #     return redirect(url_for('home'))
        # else:
        #     flash('Login Unsuccessful. Please check username and password', 'danger')

       
        #check if user exist first
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # don't undst this

            # return redirect(url_for('home'))
            return redirect(next_page) if next_page  else redirect(url_for('home')) # don't undst this

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)



# logout route to log out our user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# account route for only the logged in users
@app.route("/account")
@login_required #restrict this page to only logged in users
def account():
    return render_template('account.html', title='Account')