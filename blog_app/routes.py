import os

import secrets #to generate random names

from PIL import Image

from flask import render_template, url_for, flash, redirect, request #add import for : request

from blog_app import app, db, bcrypt #added import for : db, bcrypt
from blog_app.forms  import RegistrationForm, LoginForm, UpdateAccountForm #added import for :UpdateAccountForm

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


#save user uploaded image
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext #picture file name
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    # #automatically resize images before being saved
    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    form_picture.save(picture_path)

    return picture_fn




# account route for only the logged in users
@app.route("/account", methods=['GET', 'POST'])
@login_required #restrict this page to only logged in users
def account():
    form = UpdateAccountForm()

    # # #update form username and email if our form is valid
    if form.validate_on_submit():

        #check if picture exist
        if form.picture.data:
            #save picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file #update profile picture

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()



    #     #flash message
        flash('Your account has been updated !', 'success')
        return redirect(url_for('account'))

    # # # # populate the form with current user data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #set up user profile pic
    return render_template('account.html', title='Account', 
                            image_file=image_file, form=form) #add code to :pass the image_file, and the form