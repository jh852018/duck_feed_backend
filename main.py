from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)

@app.route('/duck-feed-entry', methods=['POST'])
@cross_origin()
def entry():
    if request.method == 'POST':
        try:
            data = request.json
            dfTime = data['dfTime']
            dfFood = data['dfFood']
            dfLocation = data['dfLocation']
            dfCount = data['dfCount']
            dfFoodType = data['dfFoodType']
            dfFoodQty = data['dfFoodQty']
            return json.dumps({'error': False, 'message': 'Successfully added'})
        except Exception as e:
            print(f"Exception while processing request: {e}")
            return json.dumps({'error': True, 'message': 'Failed to add record', 'description': str(e) })

@app.route('/duck-feed-admin', methods=['GET'])
def admin():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)