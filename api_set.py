"""This module is an API set up"""
import os
import random
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


API_KEY = os.getenv("TMDB_KEY")

movies_lst = [634649, 315635, 429617, 24428, 299534, 299536, 99861]

base_url1= f"https://api.themoviedb.org/3/configuration?api_key={API_KEY}"


def get_data():

    """ This function will get data about
    randomly selected movie from TMDB"""

    movie_id = random.choice(movies_lst)# select random element from list
    base_url= f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get( # response from TMDB API
    base_url,
    )
    movie = response.json() # take info that you need from json file

    #print(movie)
    name = movie["original_title"]
    base_url2=f"""https://en.wikipedia.org/w/api.php?action=query&\
    format=json&prop=info&gapfrom={name}&gaplimit=5&inprop=url&generator=allpages"""
    response_wiki = requests.get( # response from TMDB API
    base_url2,
    )
    movie_url = response_wiki.json()
    page_id = list(movie_url["query"]["pages"].keys())[0]
    tagline = movie["tagline"]
    poster_path = movie["poster_path"]
    genre = []
    for i in range(len(movie["genres"])):
        genre.append(movie["genres"][i]["name"])
    genres =", ".join(genre)
    return name, tagline, genres, poster_path, movie_url["query"]["pages"][page_id]["fullurl"],movie_id

def get_config():
    """This function will get configuration data
    to construct a url for a movie image later"""
    response1 = requests.get(base_url1,)
    config_info = response1.json()
    base_url=config_info["images"]["base_url"]
    poster_sizes=config_info["images"]["poster_sizes"][3]
    return base_url, poster_sizes
