from flask import flash
from flask_wtf import FlaskForm
from mijnproject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from wtforms import *
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class InfoForm(FlaskForm):

    id = HiddenField()
    naam = StringField('Wat is je naam?')
    email = StringField('Wat is je email?')
    opmerking = StringField('Wat vond je van je verblijf?')
    submit = SubmitField('Verzend')

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer,primary_key=True)
    naam = db.Column(db.Text)
    email = db.Column(db.Text)
    opmerking = db.Column(db.Text)
    
    def __init__(self,naam,email,opmerking):
        self.naam = naam
        self.email = email
        self.opmerking = opmerking

    def __repr__(self):
        return f"Contact {self.naam}: {self.opmerking} ."


class HuisjeForm(FlaskForm):

    id = HiddenField()
    naam = StringField('Wat is de naam van het huisje?')
    prijs = StringField('Wat is de prijs?')
    foto = StringField('Voeg een foto toe!')
    omschrijving = StringField('Voeg een omschrijving toe!')
    submit = SubmitField('opslaan')

class Huisjes(db.Model):
    __tablename__ = "Huisjes"

    id = db.Column(db.Integer,primary_key=True)
    naam = db.Column(db.Text)
    prijs = db.Column(db.Text)
    foto = db.Column(db.Text)
    omschrijving = db.Column(db.Text)

    def __init__(self,naam,prijs,foto,omschrijving):
        self.naam = naam
        self.prijs = prijs
        self.foto = foto
        self.omschrijving = omschrijving

    def __repr__(self):
        return f"Huisjes {self.naam}: {self.prijs}: {self.foto}: {self.omschrijving} ."



class KlantForm(FlaskForm):

    id = HiddenField()
    naam = StringField('Wat is uw naam?')
    mailadres = StringField('Wat is uw mailadres?')
    submit = SubmitField('Opslaan')

class Boeken(db.Model):
    __tablename__ = "Boeken"

    id = db.Column(db.Integer,primary_key=True)
    Huisjesid = db.Column(db.Integer)
    Klantid = db.Column(db.Text)
    Weekid = db.Column(db.Integer)

    def __init__(self,Huisjesid,Klantid,Weekid):
        self.Huisjesid = Huisjesid
        self.Klantid = Klantid
        self.Weekid = Weekid
    

    def __repr__(self):
        return f"Boeken {self.Huisjesid}: {self.Klantid}: {self.Weekid} ."

class BoekenForm(FlaskForm):

    id = HiddenField()
    week = SelectField(u'Voor welke week wilt u boeken?',
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'),('51', '51'), ('52', '52')]) 
    huisje = SelectField(u'Welke type huisje wenst u?',
        choices=[('1', 'Bungalow Comfort 4-persoons'), ('2', 'Bungalow Luxe 4-persoons'), ('3', 'Bungalow Luxe 6-persoons')]) 
    submit = SubmitField('Opslaan')

class HuisjeSelect(FlaskForm):

    id = HiddenField()
    huisje = SelectField(u'Welke type huisje wenst u?',
        choices=[('1', 'Bungalow Comfort 4-persoons'), ('2', 'Bungalow Luxe 4-persoons'), ('3', 'Bungalow Luxe 6-persoons')]) 
    submit = SubmitField('Opslaan')


db.create_all()