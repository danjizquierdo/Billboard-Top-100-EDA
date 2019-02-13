# import necessary libraries
import sys
import requests
from bs4 import BeautifulSoup
import json

# running script takes two arguments, year of top artists and
# spotify access token
year=arg1
token=arg2


# finds top 100 artists for a given year from Billboard's rankings
# returns as a list of artist names
def top_artists(year):
    artist_list = []
    artist_list_clean = []
    url = f'https://www.billboard.com/charts/year-end/{}/top-artists'
    html = requests.get(url)
    html_content = BeautifulSoup(html.content, 'html.parser')
    artist_div = html_content.findAll('div', class_="ye-chart-item__title")
    for item in artist_div:
        artist_list.append(item.a.text)
    for item in artist_list:
        artist_list_clean.append(item.strip())
    return artist_list_clean

# takes an artist name and returns the unique Spotify artist id
def find_artist(name,token):
    url='https://api.spotify.com/v1/search?'
    url_params=f'q={name}'+'&type=artist'
    
    access_token=token
    headers= {
        'Authorization': 'Bearer '+access_token
    }
    response=requests.get(url+url_params,headers=headers)
    return response.json()['artists']['items'][0]['uri'][-22:]

# takes an artist id and returns a list of their top ten track ids
def find_top_tracks(artist_id,token):
    url=f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    access_token=token
    headers= {
        'Authorization': 'Bearer '+access_token
    }
    url_params='?country=US'
    songs_data=requests.get(url+url_params,headers=headers).json()
    song_ids=[]
    for song in songs_data['tracks']:
        song_ids.append(song['id'])
    return song_ids

# loops through the top 100 albums of a year and saves their:
# artist id and top ten track ids into a json dictionary for analysis
artists=top_artists(year)
artists_ids=[]
songs_ids=[]
top_artist_tracks={}
for artist in artists:
    artist_id=find_artist(artist,token)
    top_artist_tracks[artist]={}
    top_artist_tracks[artist]['id']=artist_id
    song_id=find_top_tracks(artist_id,token)
    top_artist_tracks[artist]['tracks']=song_id

with open(f'tracks{year}.txt','w') as outfile:
    json.dump(top_artist_tracks,outfile)
