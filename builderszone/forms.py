from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from builderszone.models import  Materials, Feedback, Gallery, Login, Project
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address')
    contact = StringField('Contact No')

        
    lincense = StringField('license No')

        
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),Length(min=8, max=8) ,EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Login.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')   


class Imageadd(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=40)])
    pic = FileField('Upload Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')

class Imageupdate(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=5, max=40)])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[ EqualTo('password')])
    submit = SubmitField('Reset Password')

class Accountform(FlaskForm):
    username = StringField('Username',
                           validators=[ Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



class Material(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=40)])
    brand = StringField('Brand',validators=[Length(min=1, max=20)])
    price = StringField('Price',validators=[Length(min=1,max=15)])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')



class Projects(FlaskForm):
    name = StringField('Project Name',render_kw={"placeholder": "project name"})
    desc = StringField('Description', render_kw={"placeholder": "description"})
    mat1 = StringField('Materials', render_kw={"placeholder": "materials"})
    mat1q = StringField('Materials')
    mat2 = StringField('Materials', render_kw={"placeholder": "materials"})
    mat2q = StringField('Materials')
    mat3 = StringField('Materials', render_kw={"placeholder": "materials"})
    mat3q = StringField('Materials')
    mat4 = StringField('Materials', render_kw={"placeholder": "materials"})
    mat4q = StringField('Materials')
    mat5 = StringField('Materials', render_kw={"placeholder": "materials"})
    mat5q = StringField('Materials')
    
    numemp = StringField('No of Employees', render_kw={"placeholder": "no"})
    days = StringField('Working Days', render_kw={"placeholder": "Days"})
    empcost = StringField('Employees cost per head', render_kw={"placeholder": "cost"})
    matcost = StringField('Estimate Material cost', render_kw={"placeholder": "cost"})
    addcost = StringField('Additional cost', render_kw={"placeholder": "cost"})
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')