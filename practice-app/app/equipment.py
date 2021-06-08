import requests
from flask import Flask, Blueprint, jsonify, abort, request
import urllib
from datetime import datetime, timedelta
from math import cos, asin, sqrt, pi
from sqlalchemy.orm import sessionmaker
from .dbinit import db, User, Equipmentpost

equipment_api = Blueprint('equipment_api', __name__)
API_KEY = "Google API Key"

events = [
    {
        "eventId": 1,
        "owner": "emre_gundogu",
        "title":  "Tennis Game for Everyone",
        "content": "People who are looking for a tennis court can apply this event. Our court is for you if you are seeking for a clean and well-lit court.",
        "location": "Etiler Tennis Club",
        "coordinates": (41.0869173, 29.0321301),
        "date": "01.05.2021",
        "hours": "15.00",
        "sport": "Tennis",
        "ageGroup": "Any age",
        "skillLevel": "Any level",
        "playerCapacity": "2",
        "spectatorCapacity": "8",
        "spectators": [{"username":"zulfikar_tunc"}],
        "players": [{"username":"zulfikar_tunc"}]
    }
]

users = [
    {
        "userId": 1,
        "nickname": "emre_gundogu",
        "first_name": "Emre",
        "last_name": "Gundogu",
        "biography": "Hello, I am a 28 year-old football fan",
        "birth_year": "28",
        "avatar": "url_to_image",
        "location": "Istanbul",
        "fav_sports": ["football", "basketball"],
        "badges": ["good_player", "serious"],
        "privacy": "public",
    }
]

equipmentPost = [
	{
		"postId": 1,
		"ownerId": 1,
		"content": "A nice ball",
		"title": "Well-conditioned ball",
		"creationDate": "29.05.2021",
		"lastUpdateDate": "29.05.2021",
		"numberOfClicks": 1,
		"location": "İstanbul",
		"equipmentType": "Ball",
		"websiteName": "ismycomputeron",
		"link": "www.ismycomputeron.com"
	}
]
equipments2 = [
    {
        "equipmentId": 1,
        "ownerId": 1,
        "title" : "Tennis shoes for sale!",
        "content" : "I have a pair of shoes in good condition that i want to sell.",
        "website name" : "letgo",
        "link" : "letgo.com/245323",
        "equipmentType": "shoes",
        "location": "Istanbul",
        "sportType": "Tennis"

    },
    {
        "equipmentId": 2,
        "ownerId": 1,
        "title" : "Tennis rackets for sale!",
        "content" : "I have a pair of shoes in good condition that i want to sell.",
        "website name" : "letgo",
        "link" : "letgo.com/245323",
        "equipmentType": "racket",
        "location": "Ankara",
        "sportType": "Tennis"
    }
]
headers = {
    "x-rapidapi-key": "c4ab16012amsh73b5a257264eb3dp11ade4jsnb69ec0b79098",
    "x-rapidapi-host" :"google-search3.p.rapidapi.com"
}

@equipment_api.route('/api/v1.0/equipments/<int:equipmentId>/results', methods=['GET'])
def results(equipmentId):
    equipment = [equipment for equipment in equipments2 if equipment['equipmentId'] == equipmentId]
    if len(equipment) == 0:
        abort(404)
    title=equipment[0]['title']
    query = {
    "q": equipment[0]['title'],
}

    response=requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query), headers=headers)
    mapped=[{"description": j["description"],"link": j["link"], "title":j["title"]} for j in response.json()["results"]]
    return jsonify(mapped), 200
@equipment_api.route('/api/v1.0/equipments/<int:equipmentId>', methods=['GET'])
def getEquipment(equipmentId):
   equipment = [equipment for equipment in equipments2 if equipment['equipmentId'] == equipmentId]
   if len(equipment) == 0:
        abort(404)
   return jsonify({'equipments': equipment[0]})

@equipment_api.route('/api/v1.0/equipments', methods=['POST'])
def create_equipment_post():

    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")

    if "title" not in request.json:
        abort(400)
    if "creationDate" not in request.json:
        abort(400)
    if "equipmentType" not in request.json:
        abort(400)
    if "websiteName" not in request.json:
        abort(400)
    if "link" not in request.json:
        abort(400)

    new_equipment = Equipmentpost(content=request.json["content"],
                                  title=request.json["title"],
                                  creationDate=d1,
                                  location=request.json["location"],
                                  equipmentType=request.json["equipmentType"],
                                  websiteName=request.json["websiteName"],
                                  link=request.json["link"])

    session.add(new_equipment)
    session.commit()

    return jsonify(new_equipment), 201


@equipment_api.route('/api/v1.0/search-equipment-type/<string:equipmentType>', methods=['GET'])
def search_equipments_by_type(equipmentType):
    equipment = [equipment for equipment in equipments2 if equipment['equipmentType'] == equipmentType]
    if len(equipment) == 0:
        abort(404)
    return jsonify(equipment), 200


@equipment_api.route('/api/v1.0/search-equipment-location/<string:location>', methods=['GET'])
def search_equipments_by_location(location):
    equipment = [equipment for equipment in equipments2 if equipment['location'] == location]
    if len(equipment) == 0:
        abort(404)
    return jsonify(equipment), 200

