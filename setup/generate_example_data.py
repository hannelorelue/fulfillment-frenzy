import json
import overpass
import random

from dataclasses import dataclass
from iso3166 import countries
from pprint import pprint
from typing import List, Dict, Optional, Tuple

random.seed(42)


@dataclass
class Country:
    name: str
    iso3166_1: str

    def __hash__(self):
        return hash(self.name)


@dataclass
class City:
    node_id: int
    name: str
    coordinates: Tuple[float, float]
    zipcode: Optional[str] = None

    def __hash__(self):
        return hash(self.node_id)


@dataclass
class Address:
    street: str
    house_number: str
    city: str
    zipcode: str
    country: str
    coordinate_latitude: float
    coordinate_longitude: float

    def __hash__(self):
        return hash(self.street) ^ hash(self.house_number) ^ hash(self.city) ^ hash(self.zipcode)


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

    cities = list()

    for feature in response['features']:
        try:
            city = City(feature['id'], 
                        feature['properties']['name'], 
                        (feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0]))
            cities.append(city)
        except:
            continue

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


def generate_addresses(countries: Optional[List[Country]] = None, number_of_countries: int = 20, number_of_cities: int = 100, number_of_addresses: int = 1000) -> List[Address]:
    all_countries = get_countries()
    
    if countries is None:
        selected_countries = random.sample(all_countries, number_of_countries)
    else:
        selected_countries = random.sample(all_countries, number_of_countries-len(countries))
        selected_countries.extend(countries)


    # sample number of cities from selected countries
    min_number_of_cities_from_country = number_of_cities // number_of_countries // 3
    max_number_of_cities_from_country = int(number_of_cities // number_of_countries * 1.1)

    country_to_cities_map = dict()

    sum_of_selected_cities = 0

    # select cities from countries
    for index, country in enumerate(selected_countries):
        if index % 2 == 0:
            number_of_cities_to_select_from_country = random.randint(min_number_of_cities_from_country, max_number_of_cities_from_country) 
        else:
            number_of_cities_to_select_from_country = (index+1) * (number_of_cities // number_of_countries) - sum_of_selected_cities

        cities = get_cities_of_country(country)

        # make sure not to select more cities than the country has
        number_of_cities_to_select_from_country = min(number_of_cities_to_select_from_country, len(cities))

        sum_of_selected_cities += number_of_cities_to_select_from_country

        selected_cities = random.sample(cities, number_of_cities_to_select_from_country)
        country_to_cities_map[country] = selected_cities 

        print(f" * {index}: selected {len(country_to_cities_map[country])}/{len(cities)} cities for {country.name}")

    for country, cities in country_to_cities_map.items():
        # get streets of city
        for city in cities:
            ...            

if __name__ == "__main__":
    generate_addresses(countries=[Country("Germany", "DE"), 
                                  Country("Croatia", "HR"), 
                                  Country("United Kingdom", "UK")])

