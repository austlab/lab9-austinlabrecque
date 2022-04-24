import requests

def get_pokemon_info(name):

    print("Fetching info...", end='')
    
    if name is None:
        print('Error: Missing name parameter')
        return
    name=name.strip().lower()
    if name == '':
        print('Error: Empty name parameter')
        return

    url = "https://pokeapi.co/api/v2/pokemon/" + name
    resp = requests.get(url)

    if resp.status_code == 200:
        print('success')
        return resp.json()

    else:
        print('failed. Code:', resp.status_code)
        return

def get_pokemon_list(limit=100, offset=0):
    url = "https://pokeapi.co/api/v2/pokemon"
    
    params = {'limit': limit,
              'offset': offset
    }
    
    resp = requests.get(url, data=params)
    
    if resp.status_code == 200:
        dict = resp.json()
        return [p['name']for p in dict['results']]
    else:
        print('Failed to get Pokemon, response code:', resp.status_code)
        
def get_poke_image(name):
    pokemon_dict = get_pokemon_info(name)
    if pokemon_dict:
        return pokemon_dict['sprites']['other']['official-artwork']['front_default']
    
            