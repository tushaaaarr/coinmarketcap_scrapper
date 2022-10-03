import json
from urllib import response
from flask import Flask, render_template, request,make_response
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from bson import json_util
import datetime
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

#initialize the Flask app
app = Flask("myapp")

app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()

db.init_app(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/get_data")
def hello():
   json_data ={'name':'tushar'}
   return json_data

class ScraperTable(db.Document):
    custom_id =db.IntField()
    name = db.StringField()
    price = db.StringField()
    h_1 = db.StringField()
    h_24 = db.StringField()
    d_7 = db.StringField()
    market_cap = db.StringField()
    volume = db.StringField()
    circulating_Supply = db.StringField()
    meta = {'strict': False}

@app.route('/fetch-data', methods=['GET'])
def query_records():
    user = ScraperTable.objects.all()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user)

@app.route('/update-record', methods=['POST'])
def update_record():
    post_data = request.json
    for d_list in post_data:
        user_id = ScraperTable.objects.filter(custom_id=d_list['id']).first()
        if not user_id:
            if not ScraperTable.objects.filter(name=d_list['name']).first():
                new_instance = ScraperTable(
                    custom_id=d_list['id'],
                    name=d_list['name'],
                    price=d_list['price'],
                    h_1=d_list['h_1'],
                    h_24=d_list['h_24'],
                    d_7=d_list['d_7'],
                    market_cap=d_list['market_cap'],
                    volume=d_list['volume'],
                    circulating_Supply=d_list['circulating_Supply'])
                new_instance.save()
        else:
            user_id.update(name=d_list['name'],
                price=d_list['price'],
                h_1=d_list['h_1'],
                h_24=d_list['h_24'],
                d_7=d_list['d_7'],
                market_cap=d_list['market_cap'],
                volume=d_list['volume'],
                circulating_Supply=d_list['circulating_Supply'])
    return jsonify({'status': 'succes'})


if __name__ == "__main__":
    app.run(debug=True) 

