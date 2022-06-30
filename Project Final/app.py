import email
from flask import flash, Flask, render_template, session, redirect, url_for, request
from flask_wtf import *
from wtforms import *
from flask_sqlalchemy import SQLAlchemy
import os
from mijnproject import app,db
from flask_login import login_user, login_required, logout_user, current_user

from mijnproject.models import *
from mijnproject.forms import *


alle_opmerkingen = Contact.query.all()

for contact in alle_opmerkingen:
    print(contact)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/welkom')
@login_required
def welkom():
    return render_template('welkom.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('home'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Succesvol ingelogd.')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welkom')
                return redirect(next)

    return render_template('login.html', form=form)  

@app.route('/register', methods=['GET', 'POST'])
    
def register():
        
    form = RegistrationForm()        

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ')     

        return redirect(url_for('login'))
    
    
    return render_template('register.html', form=form) 

@app.route("/boeken/")
def boeken():
    alle_huisjes = Huisjes.query.all()
    return render_template("boeken.html", alle_huisjes = alle_huisjes)

@app.route("/overons/")
def overons():
    return render_template("overons.html")

@app.route("/ervaringen/delete/<id>")
def del_opmerking(id):
    if id:
        contact = Contact.query.get(id)

        db.session.delete(contact)
        db.session.commit()
        
        flash("Opmerking verwijderd","success")

    return redirect("/ervaringen/")



@app.route("/uwmening/", methods=['GET', 'POST'])
def form():

    form = InfoForm()

    if form.validate_on_submit():

        contact = Contact(form.naam.data,form.email.data,form.opmerking.data)

        db.session.add(contact)
        db.session.commit()
        print(contact)
        flash("Opmerking opgeslagen","success")

        return redirect("/ervaringen/")
        
    return render_template('uwmening.html', form=form)

@app.route("/ervaringen/")
def ervaringen():

    alle_opmerkingen = Contact.query.all()

    return render_template("ervaringen.html", alle_opmerkingen = alle_opmerkingen)


@app.route("/uwmening/update/<id>/", methods=['GET', 'POST'])

def update_opmerking(id):

    form = InfoForm()
    
    contact = Contact.query.get(id)
    
    if form.validate_on_submit():
        if form.id.data != "" and form.id.data==id:
            contact.naam = form.naam.data
            contact.email = form.email.data
            contact.opmerking = form.opmerking.data

            db.session.add(contact)
            db.session.commit()
        
            flash("Ervaring opgeslagen","success")

            return redirect("/ervaringen/")

    form.id.data=contact.id
    form.opmerking.data=contact.opmerking
    form.naam.data=contact.naam
    form.email.data=contact.email

    return render_template('uwmening.html', form=form)    

@app.route("/boeken/formulier/<id>/", methods=['GET', 'POST'])

def boeking(id):

    form = BoekenForm()

    huisje = Huisjes.query.get(id)
    
    form.huisje.data = id

    if form.validate_on_submit() and current_user.is_authenticated:

        boeking = Boeken(id, current_user.username, form.week.data)
        db.session.add(boeking)
        db.session.commit()
        
        flash("Boeking opgeslagen!","success")

        return redirect("/")

    elif current_user.is_authenticated == False:
        flash("Log eerst in a.u.b.")


    return render_template('boekformulier.html', form=form, huisje=huisje)   


@app.route("/admin/", methods=['GET', 'POST'])
def adminform():

    form = HuisjeForm()

    if form.validate_on_submit():

        huisje = Huisjes(form.naam.data,form.prijs.data,form.foto.data,form.omschrijving.data)

        db.session.add(huisje)
        db.session.commit()
        print(huisje)
        flash("huisje succesvol opgeslagen")

        return redirect("/huisjes")

    return render_template('admin.html', form=form)

@app.route("/huisjes/")
def huisjes():

    alle_huisjes = Huisjes.query.all()

    return render_template("huisjes.html", alle_huisjes = alle_huisjes)

@app.route("/huisjes/delete/<id>")
def del_huisje(id):
    if id:
        huisjes = Huisjes.query.get(id)

        db.session.delete(huisjes)
        db.session.commit()
        
        flash("Huisje verwijderd","success")

    return redirect("/huisjes/")

@app.route("/mijnboekingen/<id>")
def mijn_boekingen(id):

    alle_boekingen = Boeken.query.all()
    

    return render_template("mijnboekingen.html", alle_boekingen = alle_boekingen)
    


@app.route("/mijnboekingen/delete/<id>")
def del_boeking(id):
    if id:
        boekingVerwijderen = Boeken.query.get(id)

        db.session.delete(boekingVerwijderen)
        db.session.commit()
        
        flash("Boeking succesvol geannuleerd")

    return redirect("/")

@app.route("/boekformulier/update/<id>/", methods=['GET', 'POST'])

def update_boeking(id):

    form = BoekenForm()
    
    boeking = Boeken.query.get(id)

    
    if form.validate_on_submit() and current_user.is_authenticated:
        if form.id.data != "" and form.id.data==id:
            boeking.Huisjesid = form.huisje.data
            boeking.Klantid = boeking.Klantid
            boeking.Weekid = form.week.data

            db.session.add(boeking)
            db.session.commit()
        
            flash("Boeking bijgewerkt","success")

            return redirect("/mijnboekingen/<current_user>")

    form.huisje.data = boeking.Huisjesid
    form.id.data = boeking.id
    form.week.data = boeking.Weekid

    return render_template('boekingupdate.html', form=form, boeking=boeking)    



if __name__ == "__main__":
    app.run(debug = True)