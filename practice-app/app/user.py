import requests
from flask import Flask, jsonify, abort, request
import urllib
from datetime import datetime, timedelta
from math import cos, asin, sqrt, pi
from dbinit import User


app = Flask(__name__)
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



@app.route('/api/v1.0/users', methods=['POST'])
def post_user(user_id):
    body = request.json
    user_id = body["userId"]
    user = [user for user in users if user["userId"] == user_id]
    if len(user) == 0:
        response = requests.get("https://randomapi.com/api/9fekfc0v?key=2UX0-XIT1-7DYM-WDBC")
        json_data = response.json()["results"]
        new_user = User(user_id=user_id,
                        nickname=json_data[0]["nickname"],
                        first_name=json_data[0]["firstName"],
                        last_name=json_data[0]["lastName"],
                        biography=json_data[0]["biography"],
                        birth_year=json_data[0]["birth_year"],
                        avatar=json_data[0]["avatar"],
                        location=json_data[0]["location"],
                        privacy=False if json_data[0]["privacy"] == 'private' else True)
        users.append(new_user)
        return jsonify({"applicantId": user_id,
                    "applicantNickname": user[0]["nickname"],
                    "applicationServerTime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}), 201


@user_api.route('/api/v1.0/users', methods=['GET'])
def get_user(nickname):
    users_ = session.query(User).filter(nickname == User.nickname)
    if len(users_) == 0:
        abort(404)
    return jsonify(users_), 200


if __name__ == '__main__':
    app.run(debug=True)
