from flask import Flask, render_template, url_for
from datetime import date, datetime, timedelta
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

app = Flask(__name__)
Mobility(app)

@app.route("/")
@mobile_template('{mobile/}index.html')
def index(template):
    today = date.today()
    yesterday = today - timedelta(days=1)
    weekday = date.today().weekday()
    return render_template("index.html", today=today, yesterday=yesterday, weekday=weekday, title='Forside')