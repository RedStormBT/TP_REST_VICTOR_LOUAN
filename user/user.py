from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

"""
DESCRIPTION : Retourne les réservations d'un utilisateur
ENTRÉE : Un username ou userid en argument de la requête
SORTIE : Une liste de type Bookings
"""
@app.route("/user/bookings", methods=['GET'])
def get_booking_from_username_or_userid():
    bookings = ""
    if request.args:
        req = request.args
        found = False
        for user in users:
            print(str(user["id"]))
            if ("id" in req and str(user["id"]) == str(req["id"])) or ("name" in req and str(user["name"]) == str(req["name"])):
                # cette condition permet de rechercher l'utilisateur en fonction de son nom et de son id
                # on peut passer le nom ou l'id en argument de la requête
                found = True
                bookings = requests.get("http://localhost:3201/bookings/" + str(user["id"]))
        if not found:
            res = make_response(jsonify({"error": "User not found"}), 400)
        elif bookings.status_code == 400:
            res = make_response(jsonify({"error": "User has no reservation"}), 400)
        else:
            res = bookings.json()
    else:
        res = make_response(jsonify({"error": "No argument passed"}), 400)
    return res

"""
DESCRIPTION : Retourne le détail des films réservés par un utilisateur
ENTRÉE : Un userid 
SORTIE : Une liste de type Bookings
"""
@app.route("/user/booking/details/<userid>", methods=['GET'])
def get_user_bookings_infos(userid):
    for user in users:
        if str(user["id"]) == str(userid):  # On récupère le bon utilisateur
            if requests.get('http://localhost:3201/bookings/' + userid).status_code == 400 :
                return make_response(jsonify({"error": "user has no reservations"}), 400)
            else:
                bookingsUser = requests.get('http://localhost:3201/bookings/' + userid).json()[
                    "dates"]  # On récupère les séances auxquelles il est inscrit dans un tableau
                allMovieList = []
                for date in bookingsUser:
                    # pour chaque date dans lequel l'utilisateur à au moins une réservation, on récupère le détail de ces films
                    movieListDetailed = []
                    tmpDate = date
                    for movie in date["movies"]:
                        movieDetailed = requests.get("http://localhost:3200/movies/" + str(movie)).json()
                        print(movieDetailed)
                        movieListDetailed.append(movieDetailed)
                    tmpDate["movies"] = movieListDetailed # On remplace la liste d'id par toutes les informations de chaque film
                    allMovieList.append(tmpDate)
                bookingsUser = allMovieList # une fois tout le parcours effectué, on remplace la liste des dates par la
                # version actualisée contenant le détail de chaque film
                return make_response(jsonify(bookingsUser), 200)
    return make_response(jsonify({"error": "incorrect userid"}), 400)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
