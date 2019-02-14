"""Billboard Top 100 Artist Web Scraper

This script allows the user to specify a year in which to find the list of top 100 artists
and save a json file with the current top 10 tracks as returned by Spotify. The information
stored includes the artists' unique ids and the tracks unique ids to be used for further
exploration using the Spotify API.

Running this script requires three arguments to be passed:
    2 access tokens for using different endpoints in Spotify's API and
    a year starting from 2002 to determine which top 100 artists to find.

This script requires that BeautifulSoup be installed in the environment that it is run in.

This file can also be imported as a module and contains the following functions:
    * top_artists - given a year, find the top 100 Billboard artists for that year
    * find_artist - given an artist name and an access_token, find the artist's Spotify id
    * find_trop_tracks - given an artist's Spotify id, find the ids for their top 10 tracks

"""

# import necessary libraries
import sys
import requests
from bs4 import BeautifulSoup
import json

# running script takes three arguments:
# spotify access token for finding artists, 
#     found at https://developer.spotify.com/console/get-artist/
# spotify access token for finding tracks 
#     found at https://developer.spotify.com/console/get-artist-top-tracks/
# and year of top artists starting from 2002

artist_token=sys.argv[1]
track_token=sys.argv[2]
year=sys.argv[3]


def top_artists(year):
    """ 
    Finds the top 100 artists for a given year from Billboard's rankings
    and returns as a list of artist names.
    """
    
    artist_list = []
    artist_list_clean = []
    
    # Sets the url to scrape with the passed year parameter and the requests library
    url = f'https://www.billboard.com/charts/year-end/{year}/top-artists'
    html = requests.get(url)
    # Parses the html from the request with BeautifulSoup to find the specific div 
    # containing the artist name
    html_content = BeautifulSoup(html.content, 'html.parser')
    artist_div = html_content.findAll('div', class_="ye-chart-item__title")
    
    # Goes div by div and finds the text in the link containing the artist name
    # which is appended to a list which is returned
    for item in artist_div:
        artist_list.append(item.a.text)
    for item in artist_list:
        artist_list_clean.append(item.strip())
    return artist_list_clean


def find_artist(name,token):
    """Takes an artist name and access token and returns the unique Spotify artist id"""
    
    # Sets the Spotify endpoint to use and the necessary scraping parameters
    url='https://api.spotify.com/v1/search?'
    url_params=f'q={name}'+'&type=artist'
    
    access_token=token
    headers= {
        'Authorization': 'Bearer '+access_token
    }
    response=requests.get(url+url_params,headers=headers)
    
    # Turns the request into a json and then indexes the dictionaries and lists within
    # to return the 22 character long artist id.
    return response.json()['artists']['items'][0]['uri'][-22:]

def find_top_tracks(artist_id,token):
    """Takes an artist id and access token and returns a list of their Spotify top ten track ids"""
    
    # Sets the Spotify endpoint to use and the necessary scraping parameters
    url=f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    access_token=token
    headers= {
        'Authorization': 'Bearer '+access_token
    }
    url_params='?country=US'
    songs_data=requests.get(url+url_params,headers=headers).json()
    song_ids=[]
    # Turns the request into a json and then loops through the ten song list
    # to return a list of song ids.
    for song in songs_data['tracks']:
        song_ids.append(song['id'])
    return song_ids

# loops through the top 100 arists of a year and saves their artist id
# and top ten track ids into a json dictionary for further analysis
artists=top_artists(year)
artists_ids=[]
songs_ids=[]
top_artist_tracks={}
for artist in artists:
    artist_id=find_artist(artist,artist_token)
    top_artist_tracks[artist]={}
    top_artist_tracks[artist]['id']=artist_id
    song_id=find_top_tracks(artist_id,track_token)
    top_artist_tracks[artist]['tracks']=song_id

with open(f'tracks{year}.txt','w') as outfile:
    json.dump(top_artist_tracks,outfile)
