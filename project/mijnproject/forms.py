from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from mijnproject.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm',    message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Leg vast!')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            flash('Email al in gebruik')
            raise ValidationError('Email al in gebruik')
        

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            flash('Gebruikersnaam al in gebruik')
            raise ValidationError('Gebruikersnaam al in gebruik')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Inloggen')