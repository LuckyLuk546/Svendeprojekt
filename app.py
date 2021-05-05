from flask import Flask, render_template, url_for
from datetime import date, datetime, timedelta
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import dataconnection

app = Flask(__name__)
Mobility(app)

@app.route("/")
@mobile_template('{mobile/}index.html')
def index(template):
    today = date.today()
    yesterday = today - timedelta(days=1)
    weekday = date.today().weekday()
    table = dataconnection.get_newest_cars().fillna(-1)
    table[['Car_price']] = table[['Car_price']].astype(int) # Fjerner .0
    return render_template("index.html", today=today, yesterday=yesterday, weekday=weekday, table=table, title='Forside')