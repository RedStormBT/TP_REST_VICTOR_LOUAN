from flask import Flask, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedules = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

"""
DESCRIPTION : Retourne toutes la programmation
SORTIE : Une liste d'objet Schedule
"""
@app.route("/showtimes", methods=['GET'])
def get_json():
    res = make_response(jsonify(schedules), 200)
    return res

"""
DESCRIPTION : Retourne tous les films programmés pour une date donnée
ENTRÉE : Date en string
SORTIE : L'objet Schedule
"""
@app.route("/showmovies/<date>", methods=['GET'])
def get_schedule_per_date(date):
    for schedule in schedules:
        if str(schedule["date"]) == str(date):
            res = make_response(jsonify(schedule),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
