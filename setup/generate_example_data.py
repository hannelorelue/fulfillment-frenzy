import json
import overpass

from dataclasses import dataclass
from iso3166 import countries
from pprint import pprint
from typing import List, Dict, Optional, Tuple


@dataclass
class Country:
    name: str
    iso3166_1: str


@dataclass
class City:
    node_id: int
    name: str
    coordinates: Tuple[float, float]
    zipcode: Optional[str] = None


def get_countries() -> List[Country]:
    return [Country(country.name, country.alpha2) for country in countries]


def get_zipcode_of_city(city: City) -> Optional[str]:
    api = overpass.API() 

    around = 100
    response = None

    while around < 1000:
        query = f"""
node(around:{around}, {city.coordinates[0]}, {city.coordinates[1]})["addr:postcode"];
out;
"""
        response = api.get(query)

        if len(response['features']) == 0:
            around += 100
        else:
            break

    try:
        zipcode = response['features'][0]['properties']['addr:postcode']
    except:
        zipcode = None

    return zipcode


def get_cities_of_country(country: Country) -> List[City]:
    api = overpass.API() 
    response = api.get(f"""
area['ISO3166-1'='{country.iso3166_1}'][admin_level=2];
node['place'='city'](area);
out;
    """)

    cities = [City(feature['id'], 
                   feature['properties']['name'], 
                   (feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0])
                   ) for feature in response['features']]

    cities_with_zipcode = list()

    for city in cities:
        zipcode = get_zipcode_of_city(city)
        if zipcode is not None:
            city.zipcode = zipcode 
            cities_with_zipcode.append(city)

    return cities_with_zipcode
        

def get_overpass_id_of_city(city: City) -> Optional[int]:
    api = overpass.API() 
    response = api.get(f"node[name='{city.name}'][place=city]")

    # check if response was empty
    if len(response['features']) == 0:
        return None

    # if the response wasn't empty select the first feature 
    feature = response['features'][0]
    if 'id' not in feature.keys():
        return None

    return int(feature['id'])


def get_street_names_of_city(city: City, do_check: bool = True) -> Optional[List[str]]:

    # first check that city has an id 
    if do_check and (get_overpass_id_of_city(city) is None):
        return None

    api = overpass.API() 
    response = api.get(f"area [name='{city.name}']; way(area)[highway][name];")

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
    pprint(get_countries())
    pprint(get_cities_of_country(Country("Germany", "DE")))
    pprint(get_street_names_of_city(City(node_id=0, name="Rottenburg am Neckar", coordinates=(0,0)), do_check=False))

