import requests
from bs4 import BeautifulSoup

client_id='e5ef323e5b0a415795db7dd2755f1865'
client_secret='0120442d103140e38d9370756217e5b5'

def find_artist_id(name,token):
    url='https://api.spotify.com/v1/search?'
    url_params=f'q={name}'+'&type=artist'

    access_token=token
    headers= {
        'Authorization': 'Bearer '+access_token
    }
    response=requests.get(url+url_params,headers=headers)
    return response.json()['artists']['items'][0]['uri'][-22:]
