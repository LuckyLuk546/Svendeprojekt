from flask_mobility.decorators import mobile_template
from flask import Flask, render_template, url_for, request, flash
from datetime import date, datetime, timedelta
from flask_mobility import Mobility

from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, DateTimeField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy.sql import text
from flask_wtf import FlaskForm
from datetime import date
import wtforms
import pyodbc

import dataconnection


app = Flask(__name__)
Mobility(app)

app.config['SECRET_KEY'] = '2J6SmC3c67XTnbK2xaQrDdt2RkdIKUjh'

Bootstrap(app)

server = 'svenddata.database.windows.net'
database = 'svenddata'
username = 'Lukas546'
password = 'Idiot546'   
driver= '{ODBC Driver 17 for SQL Server}'   

db_name = 'svenddata.db'
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://Lukas546:Idiot546@svenddata.database.windows.net/svenddata?driver=SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class cars(db.Model):
    __tablename__ = 'cars'
    car_ID = db.Column(db.Integer, primary_key=True)
    car_brand = db.Column(db.String)
    car_model = db.Column(db.String)
    car_sub_model = db.Column(db.String)
    car_mileage = db.Column(db.Integer)
    car_model_year = db.Column(db.Integer)
    car_horsepower = db.Column(db.Integer)
    car_sold = db.Column(db.String)
    car_date_added = db.Column(db.DateTime)
    car_price = db.Column(db.Integer)
    car_thumbnail = db.Column(db.String)

    def __init__(self, car_brand, car_model, car_sub_model, car_mileage, car_model_year, car_horsepower, car_sold, car_price, car_thumbnail):
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_sub_model = car_sub_model
        self.car_mileage = car_mileage
        self.car_model_year = car_model_year
        self.car_horsepower = car_horsepower
        self.car_sold = car_sold
        self.car_price = car_price
        self.car_thumbnail = car_thumbnail

class AddRecord(FlaskForm):
    # id used only by update/edit
    car_ID = HiddenField()
    car_brand = StringField('Car brand', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid brand name"),
        Length(min=1, max=25, message="Invalid brand name length")
        ])
    car_model = StringField('Car model', [ InputRequired(),
        Length(min=1, max=25, message="Invalid model name length")
        ])
    car_sub_model = StringField('Car sub model', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\'\/]+$', message="Invalid sub model name"),
        Length(min=1, max=25, message="Invalid sub model name length")
        ])
    car_mileage = IntegerField('Car mileage', [ InputRequired(),
        NumberRange(min=1, max=999999, message="Invalid mileage")
        ])
    car_model_year = IntegerField('Car model year', [ InputRequired(),
        NumberRange(min=1.00, max=2022, message="Invalid model year")
        ])
    car_horsepower = IntegerField('Car horsepower', [ InputRequired(),
        NumberRange(min=1.00, max=9999, message="Invalid horsepower")
        ])
    car_sold = SelectField('Sold', [ InputRequired()],
        choices=[ ('', ''), ('false', 'False'), ('true', 'True')])
    car_price = IntegerField('Total price', [ InputRequired(),
        NumberRange(min=1.00, max=9999999, message="Invalid price")
        ])
    car_thumbnail = StringField('Car thumbnail', [ InputRequired(),
        Length(min=1, max=250, message="Invalid thumbnail length")
        ])
    submit = SubmitField('Add car')

# add a new sock to the database
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        car_brand = request.form['car_brand']
        car_model = request.form['car_model']
        car_sub_model = request.form['car_sub_model']
        car_mileage = request.form['car_mileage']
        car_model_year = request.form['car_model_year']
        car_horsepower = request.form['car_horsepower']
        car_sold = request.form['car_sold']
        car_price = request.form['car_price']
        car_thumbnail = request.form['car_thumbnail']
        # the data to be inserted into Sock model - the table, socks
        record = cars(car_brand, car_model, car_sub_model, car_mileage, car_model_year, car_horsepower, car_sold, car_price, car_thumbnail)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"{car_brand} {car_model} {car_sub_model} er tilføjet til databasen."
        return render_template('add_record.html', message=message)
    else:
        # show validaton errors
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form1=form1)


@app.route('/testconnection')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route("/login")
@mobile_template('{mobile/}login.html')
def login(template):

    info_table = dataconnection.get_info_table().fillna(-1)

    table = dataconnection.get_newest_cars().fillna(-1)
    table[['car_price']] = table[['car_price']].astype(int) # Fjerner .0

    return render_template("login.html", info_table=info_table, table=table, title='Login')


@app.route("/")
@app.route("/index")
@app.route("/forside")
@mobile_template('{mobile/}index.html')
def index(template):

    today = date.today()
    yesterday = today - timedelta(days=1)
    weekday = date.today().weekday()
    info_table = dataconnection.get_info_table().fillna(-1)

    newest_car = dataconnection.get_newest_car().fillna(-1)
    newest_car[['car_price']] = newest_car[['car_price']].astype(int) # Fjerner .0

    table = dataconnection.get_newest_cars().fillna(-1)
    table[['car_price']] = table[['car_price']].astype(int) # Fjerner .0

    return render_template("index.html", info_table=info_table, today=today, yesterday=yesterday, weekday=weekday, table=table, newest_car=newest_car, title='Svend-Leasing')


@app.route("/biler")
@mobile_template('{mobile/}biler.html')
def biler(template):

    info_table = dataconnection.get_info_table().fillna(-1)

    table = dataconnection.get_newest_cars().fillna(-1)
    table[['car_price']] = table[['car_price']].astype(int) # Fjerner .0

    return render_template("biler.html", info_table=info_table, table=table, title='Biler på lager')


@app.route("/bil/<int:car_ID>")
@mobile_template('{mobile/}bil.html')
def bil(template, car_ID):

    info_table = dataconnection.get_info_table().fillna(-1)

    table = dataconnection.get_specific_car(car_ID).fillna(-1)
    table[['car_price']] = table[['car_price']].astype(int) # Fjerner .0
    car_images = dataconnection.get_specific_car_image(car_ID).fillna(-1)

    return render_template("bil.html", info_table=info_table, table=table, car_images=car_images, title='Bil')


@app.route("/kontakt_os")
@mobile_template('{mobile/}kontakt_os.html')
def kontakt_os(template):
    info_table = dataconnection.get_info_table().fillna(-1)
    
    return render_template("kontakt_os.html", info_table=info_table, title='Kontakt os')


@app.route("/om_os")
@mobile_template('{mobile/}om_os.html')
def om_os(template):
    info_table = dataconnection.get_info_table().fillna(-1)
    
    return render_template("om_os.html", info_table=info_table, title='Om os')


@app.route("/qrtest")
@mobile_template('{mobile/}qrtest.html')
def qrtest(template):

    info_table = dataconnection.get_info_table().fillna(-1)
    newest_car = dataconnection.get_newest_car().fillna(-1)
    newest_car[['car_price']] = newest_car[['car_price']].astype(int) # Fjerner .0

    return render_template("qrtest.html", info_table=info_table, newest_car=newest_car, title='Qrtest')


@app.route("/form")
@mobile_template('{mobile/}form.html')
def form(template):
    info_table = dataconnection.get_info_table().fillna(-1)
    
    return render_template("form.html", info_table=info_table, title='Form')