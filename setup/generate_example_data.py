import json
import overpass

from pprint import pprint
from typing import List, Dict, Optional
from geosky import geo_plug

def get_countries() -> List[str]:
    return geo_plug.all_CountryNames()

def get_country_to_states_map() -> Dict[str, List[str]]:
    country_to_states_map = dict()
    data = json.loads(geo_plug.all_Country_StateNames())
    for country_states_dict in data:
        country = list(country_states_dict.keys())[0]
        states = country_states_dict[country]
        country_to_states_map[country] = states

    return country_to_states_map

def get_state_to_cities_map() -> Dict[str, List[str]]:
    state_to_cities_map = dict()
    data = json.loads(geo_plug.all_State_CityNames())
    for state_cities_dict in data:
        state = list(state_cities_dict.keys())[0]
        cities = state_cities_dict[state]
        state_to_cities_map[state] = cities

    return state_to_cities_map

def get_overpass_id_of_city(city: str) -> Optional[int]:
    api = overpass.API() 
    response = api.get(f"node[name={city}][place=city]")

    # check if response was empty
    if len(response['features']) == 0:
        return None

    # if the response wasn't empty select the first feature 
    feature = response['features'][0]
    if 'id' not in feature.keys():
        return None

    return int(feature['id'])

def get_street_names_of_city(city: str, do_check: bool = True) -> Optional[List[str]]:

    # first check that city has an id 
    if do_check and (get_overpass_id_of_city("Dresden") is None):
        return None

    api = overpass.API() 
    response = api.get(f"area [name={city}]; way(area)[highway][name];")

    if len(response['features']) == 0:
        return None

    # collect street names in a set to remove duplicates
    street_names = set()

    # collect street names
    for feature in response['features']:
        if 'name' in feature['properties']:
            street_names.add(feature['properties']['name'])

    return list(street_names)

if __name__ == "__main__":
    country_to_states_map = get_country_to_states_map()
    state_to_cities_map = get_state_to_cities_map()

    #print(country_to_states_map['Germany'])
    #print(state_to_cities_map['Baden-Württemberg'])
    
    #city_id = get_overpass_id_of_city("Dresden")
    street_names = get_street_names_of_city("Zagreb", do_check=False)
    pprint(street_names)
