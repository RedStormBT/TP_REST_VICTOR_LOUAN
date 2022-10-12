from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

"""
DESCRIPTION : Retourne toutes les réservations
SORTIE : Un objet AllBookings
"""
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

"""
DESCRIPTION : Retourne toutes les réservations d'un utilisateur
ENTRÉE : Un id d'utilisateur en string
SORTIE : Un objet BookingsUser
"""
@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"Booking ID not found"}),400)

"""
DESCRIPTION : Ajoute une réservation à un utilisateur
ENTRÉE : Un id d'utilisateur en string et l'objet NewMovie
SORTIE : Un objet BookingsUser
"""
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_for_user(userid):
    req = request.get_json()
    # 1. On regarde si le film souhaité est bien programmé ce jour là
    scheduledMovie = requests.get('http://localhost:3202/showmovies/' + req["date"]).json()
    found = False
    for schedule in scheduledMovie["movies"]:
        if str(schedule) == req["movieid"]:
            found = True
    if not found:
        return make_response(jsonify({"error": "The movie you try to book is not available for this date"}), 408)

    # 2. On regarde si l'utilisateur n'a pas déjà réservé ce film pour la date souhaitée
    res = make_response(jsonify({"message": "booking added"}), 200)
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            for userBooking in booking["dates"]:
                if userBooking["date"] == req["date"]:
                    for movieBooked in userBooking["movies"]:
                        if str(movieBooked) == str(req["movieid"]):
                            return make_response(jsonify({"error": "an existing item already exists"}), 409)
                    # si le film n'est pas déjà booké pour la date demandé, on l'ajoute
                    userBooking["movies"].append(req["movieid"])
                    return res

        # si le film n'est pas déjà booké et que l'utilisateur n'a rien réservé sur cette date,
        # on ajoute un item à "dates"
        jsonToAdd = {"date": req["date"], "movies": [req["movieid"]]}
        booking["dates"].append(jsonToAdd)
    return res

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
