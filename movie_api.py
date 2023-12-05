import json

import requests
import json

api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZmEwODJiODljNzRkMDgyODAwMWU1ZWQxODZhNWY5ZCIsInN1YiI6IjY1NmRkNDliNTY4NDYzMDBlZTEzYjAzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dMxyOKJik0SjKV2DNtvU8Xo_1B4UcamtAE3D2SHLuZQ'

headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

def search_all_movies(name):
    url = f"https://api.themoviedb.org/3/search/movie?query={name}&include_adult=false&language=en-US&page=1"
    response = requests.get(url, headers=headers)

    data = response.json()

    with open('movies.json', 'w') as file:
        json.dump(data, file, indent=4)




def search_data():
    with open('movies.json', 'r')as file:
        data = json.load(file)
        print(data['results'])


if __name__ == '__main__':
    search_data()