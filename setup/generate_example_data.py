import json

from geosky import geo_plug

if __name__ == "__main__":
    country_names = geo_plug.all_CountryNames()
    state_names = json.loads(geo_plug.all_Country_StateNames())
    for state_name in state_names:
        print(state_name)
