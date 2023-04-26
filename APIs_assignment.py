import requests, json
import numpy as np

################################################################################

######################## get_pokemon_types #####################################

################################################################################

def get_pokemon_types(from_type):

    url = f'https://pokeapi.co/api/v2/type/{from_type}'
    try:
        response = requests.get(url)
        if not response.json()['damage_relations']:
            print(f"get_pokemon_types Error1: Error getting info.  Check spelling of URL: {url}")
            return None
    except:
        print(f"get_pokemon_types Error1: Error getting info.  Check spelling of URL: {url}")
        return None
    
    poke_data = response.json()
    poke_types = []

    for relation in poke_data['damage_relations']:
        i = 0
        while i < len(poke_data['damage_relations'][relation]):
            poke_types.append(poke_data['damage_relations'][relation][i]['name'])
            i += 1
    poke_types = set(poke_types)

    return poke_types

# print(get_pokemon_types('bug'))  ## Ran several times to get all types.

# type_list = ['ground', 'ice', 'fairy', 'water', 'fire', 'dragon', 'steel', 'bug', 'rock', 'grass','fighting', 'dark', 'poison', 'fire', 'bug', 'dragon', 'steel','fairy', 'bug', 'poison', 'steel', 'ghost', 'rock', 'psychic', 'normal', 'ice', 'flying', 'dark','ghost', 'poison', 'bug', 'dark', 'normal', 'psychic', 'fighting','steel', 'bug', 'ice', 'flying', 'poison', 'rock', 'fire', 'water', 'grass', 'electric','ice', 'dragon', 'water', 'steel', 'flying', 'fire', 'fighting', 'grass', 'rock', 'ground','water', 'grass', 'rock', 'dragon', 'fire', 'ground', 'ice', 'electric', 'steel','fighting', 'rock', 'bug', 'dragon', 'fire', 'poison', 'flying', 'grass', 'steel', 'ice', 'ground', 'fairy', 'normal', 'water', 'psychic', 'electric','poison', 'grass', 'dark', 'steel', 'rock', 'ghost', 'psychic', 'fire', 'ground', 'flying', 'fighting', 'fairy']
# type_set = set(type_list)
# print(type_set)

# type_set = {'normal', 'psychic', 'ice', 'bug', 'grass', 'fighting', 'fire', 'dark', 'steel', 'fairy', 'poison', 'ground', 'flying', 'electric', 'ghost', 'water', 'dragon', 'rock'}
# print(len(type_set)) # 18

################################################################################

######################## get_pokemon_info ######################################

################################################################################

def get_pokemon_info(pocket_monster, attribute):
    url = f'https://pokeapi.co/api/v2/pokemon/{pocket_monster.lower()}'
    
    try:
        response = requests.get(url)
        if not response.json()['abilities'][0]['ability']['name']:
            print("get_pokemon_info Error1: Error getting info.  Check spelling of url: {url}.")
            return None
    except:
        print("get_pokemon_info Error1: Error getting info.  Check spelling of url: {url}.")
        return None
    
    poke_data = response.json()
    
    ability_list = []
        
    ability = 0
    while ability < len(poke_data['abilities']):
        ability_list.append(poke_data['abilities'][ability]['ability']['name'])
        ability += 1


    pokemon_info = {
        'Name': pocket_monster.title(),
        'Abilities': ability_list,
        'Weight': poke_data['weight'],
        'Base_exp': poke_data['base_experience'],
        'front_shiny_sprite': poke_data['sprites']['front_shiny'],
        'attack_base_state': poke_data['stats'][1]['base_stat'],
        'HP_base_stat': poke_data['stats'][0]['base_stat'],
        'Defense_base_stat': poke_data['stats'][2]['base_stat']
    }
    if attribute.lower() == "abilities":
        return ability_list
    elif attribute.lower() == "weight":
        return poke_data['weight']
    elif attribute.lower() == 'info':
        return pokemon_info


################################################################################

######################## pokemon_by_type (not used) ############################

################################################################################

def pokemon_by_type(type):
    
    url = f'https://pokeapi.co/api/v2/type/{type}'
    try:
        response = requests.get(url)
        if not response.json()['damage_relations']:
            print(f"pokemon_by_type Error1: Error getting info.  Check spelling of url: {url}")
            return None
    except:
        print(f"pokemon_by_type Error1: Error getting info.  Check spelling of url: {url}")
        return None
    
    poke_data = response.json()
    pokemon_by_type = {}

    
    select_poke = np.random.randint(0, len(poke_data['pokemon']))
    pokemon_name = poke_data['pokemon'][select_poke]['pokemon']['name'].lower()
    abilities = get_pokemon_info(pokemon_name, 'abilities')
    weight = get_pokemon_info(pokemon_name, 'weight')
    
    # print(f'\ntype: {type}, url = {url}')
    # print(f'select_poke: {select_poke}, len(poke_data["pokemon"] =  {len(poke_data["pokemon"])}, pokemon_name = "{pokemon_name}"')

      
    pokemon_by_type = {
        type: {
            pokemon_name: {
                'abilities': abilities,
                'weight': weight
            }
        }
    }

    return pokemon_by_type[type]

################################################################################

######################## build_deck (not used) #################################
#                 Interesting, but not structure asked for
################################################################################

def build_deck(num_cards):  
    '''
        Builds a random deck with given number of cards.
        Input MUST be an integer
    '''
    type_list = ['normal', 'psychic', 'ice', 'bug', 'grass', 'fighting', 'fire', 'dark', 'steel', 'fairy', 'poison', 'ground', 'flying', 'electric', 'ghost', 'water', 'dragon', 'rock']

    deck = {}

    i = 1
    while i <= num_cards:
        deck[i] = pokemon_by_type(type_list[np.random.randint(0,len(type_list))])
        i += 1

    return deck

# print('\n', build_deck(5), '\n')


################################################################################

######################## build_pokemon_dict ####################################

################################################################################

def build_pokemon_dict(num):
    type_list = ['normal', 'psychic', 'ice', 'bug', 'grass', 'fighting', 'fire', 'dark', 'steel', 'fairy', 'poison', 'ground', 'flying', 'electric', 'ghost', 'water', 'dragon', 'rock']
    pokemon = []
    my_pokemon_dict = {}
    for type in type_list:
        my_pokemon_dict[type] = {}

    
    while num > 0:
        url = "https://pokeapi.co/api/v2/pokemon"
        
        try:
            response = requests.get(url)
            if not response.json()['results']: ## crashes out if URL is wrong
                print(f"build_pokemon_dict Error_1: Error getting info.  Check spelling of url: {url}")
                return None
        except:
            print(f"build_pokemon_dict Error_1: Error getting info.  Check spelling of url: {url}")
            return None
        
        poke_data = response.json()
        select_poke = np.random.randint(0, len(poke_data['results']))
        pokemon_name = poke_data['results'][select_poke]['name']
        
        # print(f'num = {num}, pokemon_name = {pokemon_name}')
        if pokemon_name in pokemon:
            continue
        
        pokemon.append(pokemon_name)
        
        url_2 = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        try:
            response_2 = requests.get(url_2)    ## crashes out if URL is wrong
            if not response_2.json()['abilities']:
                print(f"Error_3: Error getting info.  Check spelling of url: {url_2}")
                return None
        except:
            print(f"Error_4: Error getting info.  Check spelling of url: {url_2}")
            return None
        
        poke_data_2 = response_2.json()
        type = poke_data_2['types'][0]['type']['name']

        my_pokemon_dict[type][pokemon_name] = {'abilities':[],'weight':''}
        my_pokemon_dict[type][pokemon_name]['abilities'] = get_pokemon_info(pokemon_name, 'abilities' )
        my_pokemon_dict[type][pokemon_name]['weight'] = get_pokemon_info(pokemon_name, 'weight' )
        
        num -= 1

    
    return my_pokemon_dict

print('\n',json.dumps(build_pokemon_dict(20), sort_keys=False, indent=4),'\n')

# confirmed 20 pokemon by manual count of below
output = {
    "normal": {
        "pidgeot": {
            "abilities": [
                "keen-eye",
                "tangled-feet",
                "big-pecks"
            ],
            "weight": 395
        },
        "rattata": {
            "abilities": [
                "run-away",
                "guts",
                "hustle"
            ],
            "weight": 35
        },
        "pidgeotto": {
            "abilities": [
                "keen-eye",
                "tangled-feet",
                "big-pecks"
            ],
            "weight": 300
        },
        "pidgey": {
            "abilities": [
                "keen-eye",
                "tangled-feet",
                "big-pecks"
            ],
            "weight": 18
        },
        "raticate": {
            "abilities": [
                "run-away",
                "guts",
                "hustle"
            ],
            "weight": 185
        }
    },
    "psychic": {},
    "ice": {},
    "bug": {
        "metapod": {
            "abilities": [
                "shed-skin"
            ],
            "weight": 99
        },
        "kakuna": {
            "abilities": [
                "shed-skin"
            ],
            "weight": 100
        },
        "beedrill": {
            "abilities": [
                "swarm",
                "sniper"
            ],
            "weight": 295
        },
        "weedle": {
            "abilities": [
                "shield-dust",
                "run-away"
            ],
            "weight": 32
        },
        "butterfree": {
            "abilities": [
                "compound-eyes",
                "tinted-lens"
            ],
            "weight": 320
        },
        "caterpie": {
            "abilities": [
                "shield-dust",
                "run-away"
            ],
            "weight": 29
        }
    },
    "grass": {
        "venusaur": {
            "abilities": [
                "overgrow",
                "chlorophyll"
            ],
            "weight": 1000
        },
        "ivysaur": {
            "abilities": [
                "overgrow",
                "chlorophyll"
            ],
            "weight": 130
        },
        "bulbasaur": {
            "abilities": [
                "overgrow",
                "chlorophyll"
            ],
            "weight": 69
        }
    },
    "fighting": {},
    "fire": {
        "charmeleon": {
            "abilities": [
                "blaze",
                "solar-power"
            ],
            "weight": 190
        },
        "charmander": {
            "abilities": [
                "blaze",
                "solar-power"
            ],
            "weight": 85
        },
        "charizard": {
            "abilities": [
                "blaze",
                "solar-power"
            ],
            "weight": 905
        }
    },
    "dark": {},
    "steel": {},
    "fairy": {},
    "poison": {},
    "ground": {},
    "flying": {},
    "electric": {},
    "ghost": {},
    "water": {
        "wartortle": {
            "abilities": [
                "torrent",
                "rain-dish"
            ],
            "weight": 225
        },
        "blastoise": {
            "abilities": [
                "torrent",
                "rain-dish"
            ],
            "weight": 855
        },
        "squirtle": {
            "abilities": [
                "torrent",
                "rain-dish"
            ],
            "weight": 90
        }
    },
    "dragon": {},
    "rock": {}
}