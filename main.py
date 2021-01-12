import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from  dateutil.parser import parse

##TODO refactor constants

ENV = 'prod'
app = Flask(__name__)
cors = CORS(app)


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toor@localhost/duck_feed'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fcvsmlzuwlmubg:196a52b2d0b1510bb66d321f812e1fab6c337e61fc38be0c4d4b441f76bd795c@ec2-54-144-196-35.compute-1.amazonaws.com:5432/d6kgqfsk0i1tls'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#TODO refactor to model.py
class DuckFeedEntry(db.Model):
    __tablename__ = 'duckfeedentry'
    id = db.Column(db.Integer, primary_key=True)
    df_time = db.Column(db.DateTime, nullable=False)
    df_food = db.Column(db.String(100))
    df_location = db.Column(db.String(100))
    df_count = db.Column(db.Integer)
    df_food_type = db.Column(db.String(100))
    df_food_qty = db.Column(db.Integer)

    def __init__(self, df_time, df_food, df_location, df_count, df_food_type, df_food_qty):
        self.df_time = df_time
        self.df_food = df_food
        self.df_location = df_location
        self.df_count = df_count
        self.df_food_type = df_food_type
        self.df_food_qty = df_food_qty

COLUMNS = set(DuckFeedEntry.__table__.columns.keys())

@app.route('/duck-feed-entry', methods=['POST', 'OPTIONS'])
@cross_origin()
def entry():
    if request.method == 'POST':
        try:
            data = request.json
            print(f"Received->{data}<-")
            dfTime = parse(data['dfTime']).replace(tzinfo=None)
            dfFood = data['dfFood']
            dfLocation = data['dfLocation']
            dfCount = data['dfCount']
            dfFoodType = data['dfFoodType']
            dfFoodQty = data['dfFoodQty']
            print(f"Adding data ->", dfTime, dfFood, dfLocation, dfCount, dfFoodType, dfFoodQty)
            dfEntry = DuckFeedEntry(dfTime, dfFood, dfLocation, dfCount, dfFoodType, dfFoodQty)
            db.session.add(dfEntry)
            db.session.commit()
            return json.dumps({'error': False, 'message': 'Successfully added'})
        except Exception as e:
            print(f"Exception while processing request: {e}")
            return json.dumps({'error': True, 'message': 'Failed to add record', 'description': str(e) })

@app.route('/duck-feed-admin', methods=['GET'])
def admin():
    try:
        data = []
        for item in DuckFeedEntry.query.all():
            item = item.__dict__
            item = {column: item[column] for column in COLUMNS}
            item['df_time'] = str(item['df_time'])
            data.append(item)

        return {'error': False, 'message': json.dumps(data, default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>")}
    except Exception as e:
        return {'error': True, 'message': 'Exception while querying data', 'description': str(e)}

if __name__ == '__main__':
    app.run()