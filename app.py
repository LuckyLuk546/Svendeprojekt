from flask import Flask, render_template, url_for
from datetime import date, datetime, timedelta
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import dataconnection

app = Flask(__name__)
Mobility(app)

@app.route("/")
@app.route("/index")
@app.route("/forside")
@mobile_template('{mobile/}index.html')
def index(template):

    today = date.today()
    yesterday = today - timedelta(days=1)
    weekday = date.today().weekday()
    info_table = dataconnection.get_info_table().fillna(-1)

    table = dataconnection.get_newest_cars().fillna(-1)
    table[['car_price']] = table[['car_price']].astype(int) # Fjerner .0

    return render_template("index.html", info_table=info_table, today=today, yesterday=yesterday, weekday=weekday, table=table, title='Svend-Leasing')


@app.route("/biler")
@mobile_template('{mobile/}biler.html')
def biler(template):

    info_table = dataconnection.get_info_table().fillna(-1)

    table = dataconnection.get_newest_cars().fillna(-1)
    table[['car_price']] = table[['car_price']].astype(int) # Fjerner .0

    return render_template("biler.html", info_table=info_table, table=table, title='Biler på lager')

@app.route("/qrtest")
@mobile_template('{mobile/}qrtest.html')
def qrtest(template):

    info_table = dataconnection.get_info_table().fillna(-1)

    return render_template("qrtest.html", info_table=info_table, title='Qrtest')