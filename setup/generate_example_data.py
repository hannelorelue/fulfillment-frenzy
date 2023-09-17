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

    def __repr__(self) -> str:
        return f'"{self.street}","{self.house_number}","{self.city}","{self.zipcode}","{self.country}",{self.coordinate_latitude},{self.coordinate_longitude}'

    def __str__(self) -> str:
        return self.__repr__() 


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


def generate_house_number():
    house_number = str(random.randint(1,200))
    
    if random.randint(0,10) > 8: 
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] 
        letter = random.choice(letters)

        house_number = f"{house_number}{letter}"

    return house_number


def generate_addresses(countries: Optional[List[Country]] = None, number_of_countries: int = 20, number_of_cities: int = 100, number_of_addresses: int = 1000) -> List[Address]:
    all_countries = get_countries()

    final_number_of_addresses = number_of_addresses
    number_of_addresses= int(number_of_addresses*1.2)

    addresses = list()
    
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

    number_of_selected_cities = len([item for sublist in country_to_cities_map.values() for item in sublist])
    min_number_of_streets_from_city = number_of_addresses // number_of_selected_cities // 3
    max_number_of_streets_from_city = int(number_of_addresses // number_of_selected_cities * 1.1)

    index = 0
    sum_of_selected_streets = 0

    for country, cities in country_to_cities_map.items():
        # get streets of city
        for city in cities:

            if index % 2 == 0:
                number_of_streets_to_select_from_city = random.randint(min_number_of_streets_from_city, max_number_of_streets_from_city)
            else:
                number_of_streets_to_select_from_city = (index+1)* (number_of_addresses // number_of_selected_cities) - sum_of_selected_streets

            streets = get_street_names_of_city(city)

            if streets is not None:
                # make sure not to select more streets than the city has
                number_of_streets_to_select_from_city = min(number_of_streets_to_select_from_city, len(streets))

                sum_of_selected_streets += number_of_streets_to_select_from_city

                selected_streets = random.sample(streets, number_of_streets_to_select_from_city)

                print(f" * {index}: selected {len(selected_streets)}/{len(streets)} steets from {city.name}")

                # generate addresses
                for street in selected_streets:

                    address = Address(street=street,
                                      house_number=generate_house_number(),
                                      city=city.name,
                                      zipcode=city.zipcode,
                                      country=country.name,
                                      coordinate_latitude=city.coordinates[0],
                                      coordinate_longitude=city.coordinates[1])

                    addresses.append(address)

            index += 1
    
    final_number_of_addresses = min(len(addresses), final_number_of_addresses)
    addresses = random.sample(addresses, final_number_of_addresses)

    return addresses
        

if __name__ == "__main__":
    addresses = generate_addresses(countries=[Country("Germany", "DE"), 
                                              Country("Croatia", "HR"), 
                                              Country("United Kingdom", "GB")], 
                                   number_of_countries=3, 
                                   number_of_addresses=1000)

    print(f" * generated {len(addresses)} addresses")

    address_id = 1

    with open("setup/addresses.csv", "w") as addresses_csv:
        addresses_csv.write("AddressId,Street,HouseNumber,City,ZipCode,Country,CoordinateLatitude,CoordinateLongitude\n")

        for address in addresses:
            addresses_csv.write(f"{address_id},{address}\n")
            address_id += 1

