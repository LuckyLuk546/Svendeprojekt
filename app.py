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
from datetime import date, datetime
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
    car_date_added = db.Column(db.DateTime)
    car_price = db.Column(db.Integer)
    car_thumbnail = db.Column(db.String)
    car_image_2 = db.Column(db.String)
    car_image_3 = db.Column(db.String)
    car_image_4 = db.Column(db.String)

    def __init__(self, car_brand, car_model, car_sub_model, car_mileage, car_model_year, car_horsepower, car_sold, car_date_added, car_price, car_thumbnail, car_image_2, car_image_3, car_image_4):
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_sub_model = car_sub_model
        self.car_mileage = car_mileage
        self.car_model_year = car_model_year
        self.car_horsepower = car_horsepower
        self.car_sold = car_sold
        self.car_date_added = car_date_added
        self.car_price = car_price
        self.car_thumbnail = car_thumbnail
        self.car_image_2 = car_image_2
        self.car_image_3 = car_image_3
        self.car_image_4 = car_image_4

class AddCar(FlaskForm):
    # id used only by update/edit
    car_ID = HiddenField()
    car_brand = StringField('Mærke', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid brand name"),
        Length(min=1, max=25, message="Invalid brand name length")
        ])
    car_model = StringField('Model', [ InputRequired(),
        Length(min=1, max=25, message="Invalid model name length")
        ])
    car_sub_model = StringField('Under model')
    car_mileage = IntegerField('Car mileage', [ InputRequired(),
        NumberRange(min=1, max=999999, message="Invalid mileage")
        ])
    car_model_year = IntegerField('Model år', [ InputRequired(),
        NumberRange(min=1.00, max=2022, message="Invalid model year")
        ])
    car_horsepower = IntegerField('Hestekræfter', [ InputRequired(),
        NumberRange(min=1.00, max=9999, message="Invalid horsepower")
        ])
    car_sold = SelectField('Solgt', [ InputRequired()],
        choices=[ ('', ''), ('false', 'False'), ('true', 'True')])
    car_price = IntegerField('Totalomkostning', [ InputRequired(),
        NumberRange(min=1.00, max=9999999, message="Invalid price")
        ])
    car_thumbnail = StringField('Billede 1 (imgbb url)', [ InputRequired(),
        Length(min=1, max=250, message="Invalid url length")
        ])
    car_image_2 = StringField('Billede 2 (imgbb url)', [ InputRequired(),
        Length(min=1, max=250, message="Invalid url length")
        ])
    car_image_3 = StringField('Billede 3 (imgbb url)', [ InputRequired(),
        Length(min=1, max=250, message="Invalid url length")
        ])
    car_image_4 = StringField('Billede 4 (imgbb url)', [ InputRequired(),
        Length(min=1, max=250, message="Invalid url length")
        ])
    submit = SubmitField('Bekræft')

class DeleteCar(FlaskForm):
    car_ID = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Delete This Car')
    
# add a new car to the database
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    now = datetime.now()
    form1 = AddCar()
    if form1.validate_on_submit():
        car_brand = request.form['car_brand']
        car_model = request.form['car_model']
        car_sub_model = request.form['car_sub_model']
        car_mileage = request.form['car_mileage']
        car_model_year = request.form['car_model_year']
        car_horsepower = request.form['car_horsepower']
        car_sold = request.form['car_sold']
        car_date_added = now
        car_price = request.form['car_price']
        car_thumbnail = request.form['car_thumbnail']
        car_image_2 = request.form['car_image_2']
        car_image_3 = request.form['car_image_3']
        car_image_4 = request.form['car_image_4']
        # the data to be inserted into the cars table
        car = cars(car_brand, car_model, car_sub_model, car_mileage, car_model_year, car_horsepower, car_sold, car_date_added, car_price, car_thumbnail, car_image_2, car_image_3, car_image_4)
        # Flask-SQLAlchemy magic adds car to database
        db.session.add(car)
        db.session.commit()
        # create a message to send to the template
        message = f"{car_brand} {car_model} {car_sub_model} er tilføjet til databasen."
        return render_template('add_car.html', message=message)
    else:
        # show validaton errors
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_car.html', form1=form1, title='Tilføj ny bil')

# view cars from the database
@app.route('/view_car', methods=['GET', 'POST'])
def view_car():
    cars_view = cars.query.filter_by().order_by(cars.car_brand).all()
    return render_template('view_car.html', cars_view=cars_view)

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    car = cars.query.filter(cars.car_ID == id).first()
    # two forms in this template
    form1 = AddCar()
    form2 = DeleteCar()
    return render_template('edit_or_delete.html', car=car, form1=form1, form2=form2, choice=choice)

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['POST'])
def delete_result():
    id = request.form['car_ID']
    purpose = request.form['purpose']
    car = cars.query.filter(cars.car_ID == id).first()
    if purpose == 'delete':
        db.session.delete(car)
        db.session.commit()
        message = f"Bilen {car.car_brand} {car.car_model} er blevet slettet fra databasen"
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)

# result of edit - this function updates the record
@app.route('/edit_result', methods=['POST'])
def edit_result():
    id = request.form['car_ID']
    # call up the record from the database
    car = cars.query.filter(cars.car_ID == id).first()
    # update all values
    car.car_brand = request.form['car_brand']
    car.car_model = request.form['car_model']
    car.car_sub_model = request.form['car_sub_model']
    car.car_mileage = request.form['car_mileage']
    car.car_model_year = request.form['car_model_year']
    car.car_horsepower = request.form['car_horsepower']
    car.car_sold = request.form['car_sold']
    car.car_price = request.form['car_price']
    car.car_thumbnail = request.form['car_thumbnail']
    car.car_image_2 = request.form['car_image_2']
    car.car_image_3 = request.form['car_image_3']
    car.car_image_4 = request.form['car_image_4']

    form1 = AddCar()
    if form1.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"Bil med id: {car.car_ID} er blevet opdateret."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        car.car_ID = id
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, car=car, choice='edit')

# view cars from the database
@app.route('/view_car_first', methods=['GET', 'POST'])
def view_car_first():
    try:
        cars_view = cars.query.filter_by().order_by(cars.car_brand).all()
        car_text = '<ul>'
        for car in cars_view:
            car_text += '<li>' + car.car_brand + ', ' + car.car_model + '</li>'
        car_text += '</ul>'
        return car_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


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

    return render_template("bil.html", info_table=info_table, table=table, title='Bil')


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