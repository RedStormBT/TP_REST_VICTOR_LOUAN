# UE-AD-A1-REST

## Auteurs :
- Victor Barreteau
- Louan Bélicaud

## Avancement TP
- Vert ✅

Pour la question 1 du TP Vert, nous avons choisi comme point d'entrée /moviesbydirector , 
qui rassemble les films réalisés par le réalisateur passé en paramètre.

- Bleu ✅
- Rouge ✅

On a ajouté des fonctions de recherche par titre et par id en exploitant la BDD de Imdb.

## APIs
1. API Rest Movie : 
	```
    - /
    - /template
    - /json
    - /moviesbytitle
    - /movies/<movieid> [GET / POST / DELETE]
    - /movies/<movieid>/<rate>
    - /movies/imdb/<movieid>
    - /movies/imdb (ex: /movies/imdb?title=Lost)
    - /moviesbydirector
    - /apidiscover
	```
2. API Rest Showtime :
   ```
   - /
   - /showtimes
   - /showmovies/<date>
   ```
3. API Rest Booking :
   ```
   - /bookings/\<userid> [GET / POST]
   ```

## Comment démarrer ?  

Si des dépendances sont manquantes, elles sont listées dans le fichier requirements.txt
Pour les installer, lancer la commande suivante : 
```bash 
pip install -r requirements.txt
```