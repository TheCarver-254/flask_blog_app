from flask_wtf import FlaskForm
#add import for : FileField
from flask_wtf.file import FileField, FileAllowed 
#add import for : current_user
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField #add import for :BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from blog_app.models import User #add User model


class RegistrationForm(FlaskForm):
    username = StringField('Username',
       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    #create a custom form validation

    #check if username exist in the database 
    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(' That username already exist. Please choose another username')



     #check if email exist in the database 
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(' That email already exist. Please choose another email')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit   = SubmitField('Login')



# update user profile
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')


    #create a custom form validation

    #check if username exist in the database 
    def validate_username(self, username):

        #run custom validation only if the username is not equal to their current username
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(' That username already exist. Please choose another username')



     #check if email exist in the database 
    def validate_email(self, email):

        #run custom validation only if the email is not equal to their current email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(' That email already exist. Please choose another email')





#create post form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


        
