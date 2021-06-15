# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
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
    car_price = db.Column(db.Integer)

    def __init__(self, car_ID, style, color, quantity, price, updated):
        self.car_ID = car_ID
        self.style = style
        self.color = color
        self.quantity = quantity
        self.price = price
        self.updated = updated