import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from  dateutil.parser import parse
from datetime import timezone
from utils import createResponse
from config.constants import ENV, TABLENAME, DF_TIME_T
from config.constants import SQLALCHEMY_TRACK_MODIFICATIONS, SQLALCHEMY_DATABASE_URI
from config.constants import SQLALCHEMY_DATABASE_URI_DEV, SQLALCHEMY_DATABASE_URI_PROD
from config.constants import DF_TIME_J, DF_FOOD_J, DF_FOOD_LOCATION_J
from config.constants import DF_FOOD_COUNT_J, DF_FOOD_TYPE_J, DF_FOOD_QTY_J


app = Flask(__name__)
cors = CORS(app)


if ENV == 'dev':
    app.debug = True
    app.config[SQLALCHEMY_DATABASE_URI] = SQLALCHEMY_DATABASE_URI_DEV
else:
    app.debug = False
    app.config[SQLALCHEMY_DATABASE_URI] = SQLALCHEMY_DATABASE_URI_PROD

app.config[SQLALCHEMY_TRACK_MODIFICATIONS] = False
db = SQLAlchemy(app)

class DuckFeedEntry(db.Model):
    __tablename__ = TABLENAME
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
            # print(f"Received->{data}<-")
            dfTime = parse(data[DF_TIME_J]).replace(tzinfo=None)
            dfFood = data[DF_FOOD_J]
            dfLocation = data[DF_FOOD_LOCATION_J]
            dfCount = data[DF_FOOD_COUNT_J]
            dfFoodType = data[DF_FOOD_TYPE_J]
            dfFoodQty = data[DF_FOOD_QTY_J]
            # print(f"Adding data ->", dfTime, dfFood, dfLocation, dfCount, dfFoodType, dfFoodQty)
            dfEntry = DuckFeedEntry(dfTime, dfFood, dfLocation, dfCount, dfFoodType, dfFoodQty)
            db.session.add(dfEntry)
            db.session.commit()
            return json.dumps(createResponse(False, 'Successfully added'))
        except Exception as e:
            print(f"Exception while processing request: {e}")
            return json.dumps(createResponse(True, 'Failed to add record', str(e)))

@app.route('/duck-feed-admin', methods=['GET'])
def admin():
    try:
        data = []
        for item in DuckFeedEntry.query.all():
            item = item.__dict__
            item = {column: item[column] for column in COLUMNS}
            item[DF_TIME_T] = item[DF_TIME_T].replace(tzinfo=timezone.utc).isoformat()
            data.append(item)
        return json.dumps(createResponse(False, data), default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>")
    except Exception as e:
        return json.dumps(True, 'Exception while querying data', str(e))

if __name__ == '__main__':
    app.run()