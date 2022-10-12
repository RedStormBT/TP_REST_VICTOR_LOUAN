import requests
from flask import Flask, render_template, request, jsonify, make_response, url_for
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), "r") as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service! Try /apidiscover endpoint to discover all endpoints available !</h1>",200)

@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

"""
DESCRIPTION : Retourne tous les films
SORTIE : Une liste d'objet MovieItem
"""
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

"""
DESCRIPTION : Retourne le film qui a pour id celui passé en paramètre de cette fonction
ENTRÉE : Un id de film
SORTIE : Un objet MovieItem
"""
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)


"""
DESCRIPTION : Retourne le film qui a pour id celui passé en paramètre de cette fonction en exploitant l'API Imdb 
ENTRÉE : Un id de film
SORTIE : Un objet MovieItem
"""
@app.route("/movies/imdb/<movieid>", methods=['GET'])
def get_movie_byid_imdb(movieid):
    req = requests.get("https://imdb-api.com/en/API/Title/k_jm7ykvhe/" + movieid).json()
    rep = {"title": req["originalTitle"], "rating": req["imDbRating"], "director": req["directors"], "id": movieid}
    return make_response(jsonify(rep))

"""
DESCRIPTION : Retourne le film qui a pour titre celui passé en paramètre de cette fonction
ENTRÉE : Un titre de film en string
SORTIE : Un objet MovieItem
"""
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(json),200)
    return res

"""
DESCRIPTION : Retourne le film qui a pour titre celui passé en paramètre de cette fonction avec l'api Imdb
ENTRÉE : Un titre de film en string
SORTIE : Un objet MovieItem
"""
@app.route("/moviesbytitle/imdb", methods=['GET'])
def get_movie_bytitle_imdb():
    if request.args:
        req = request.args
        reqImdb = requests.get("https://imdb-api.com/en/API/SearchTitle/k_jm7ykvhe/" + req["title"]).json()
        reqImdb = reqImdb["results"][0]
        rep = {"title": reqImdb["title"], "id": reqImdb["id"]}
    else:
        return make_response({"error": "movie title not found"}, 400)
    return make_response(jsonify(rep), 200)


"""
DESCRIPTION : Ajoute un film à la liste
ENTRÉE : Un id en paramètre et un objet MovieItem dans le body de la requête
SORTIE : Un message de validation ou d'erreur
"""
@app.route("/movies/<movieid>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

"""
DESCRIPTION : Modifie la note d'un film
ENTRÉE : L'id du film en string et la nouvelle note en float
SORTIE : L'objet MovieItem modifié
"""
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res


"""
DESCRIPTION : Supprime un film
ENTRÉE : L'id du film en string
SORTIE : L'objet supprimé 
"""
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response({"error":"item deleted"}, 200)

    res = make_response(jsonify({"error":"movie ID not found"}), 400)
    return res

"""
DESCRIPTION : Retourne tous les films programmés pour une date donnée
ENTRÉE : Date en string
SORTIE : L'objet Schedule
"""
@app.route("/moviesbydirector", methods=['GET'])
def get_movies_bydirector():
    moviesByDirector = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                moviesByDirector.append(movie)

    if not json:
        res = make_response(jsonify({"error":"director not found"}),400)
    else:
        res = make_response(jsonify(moviesByDirector),200)
    return res


"""
DESCRIPTION : Retourne une liste de tous les endpoint existants
SORTIE : Un json avec tous les endpoints
"""
@app.route("/apidiscover", methods=['GET'])
def get_all_endpoints():
    routes = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        routes.append({"%s" % rule: methods})
    print(routes)
    return make_response(jsonify({"routes": routes}),200)


if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)

