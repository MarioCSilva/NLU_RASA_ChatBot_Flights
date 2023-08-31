import json
from numpy import random
import requests
import aux.constants as Constants
import json
import logging
# Logger
logging.basicConfig(
    format="%(module)-20s:%(levelname)-15s| %(message)s",
    level=logging.INFO
)
class AviationStackHandler:
    def __init__(self) -> None:
        self.flights_endpoint = '/flights'
        self.cities = None
        self.loadCities()

    def loadCities(self):
        logging.info("Reading cities data..")
        f = open("./static/cities.json",'r')
        data = f.read()
        self.cities = json.loads(data)['data']
        f.close()
        logging.info("Data loaded")
    
    def getCityByName(self,city_name):
        for city in self.cities:
            if city['city_name'] == city_name:
                return True, city
        return False, f"Could not get City by city name {city_name}"
    
    def getFlightsByIATACode(self, dep_iata=None, arr_iata=None):
        url = f'{Constants.AVIATIONSTACK_HOST}{self.flights_endpoint}?access_key={Constants.ACCESS_KEY}'
        if dep_iata:
            url+=f'&dep_iata={dep_iata}'
        if arr_iata:
            url+=f'&arr_iata={arr_iata}'
        try:
            r = requests.get(url=url,verify=False)
            data = r.json()['data']
        except Exception as e:
            return False, f"Could not obtain Flights. Reason: {e}"
        return True, data

    def parse_flights_data(self, flights, user_budget: float):
        res = []
        for flight in flights:
            flight_price = round(random.uniform(10.0, 150.0),2)
            if user_budget:
                if flight_price > user_budget:
                    continue
            obj = {
                        'departure_iata': flight['departure']['iata'],
                        'departure_time': flight['departure']['estimated'],
                        'airline_name': flight['airline']['name'],
                        'arrival_iata': flight['arrival']['iata'],
                        'arrival_time': flight['arrival']['estimated'],
                        'flight_number': flight['flight']['number'],
                        'flight_icao': flight['flight']['icao'],
                        'price': flight_price
            }
            res.append(obj)
        return json.dumps(res)

    def get_availableFlights(self,departure_city,arrival_city,user_budget=None):
        dep_status,dep_city = self.getCityByName(departure_city)
        arr_status, arr_city = self.getCityByName(arrival_city)
        if not dep_status or not arr_status:
            return None
        #print(dep_city)
        dep_iata = dep_city['iata_code']
        arr_iata = arr_city['iata_code']
        _,flights = self.getFlightsByIATACode(dep_iata,arr_iata)
        if not flights:
            return []
        return self.parse_flights_data(flights,user_budget)
    

aviationStackHandler = AviationStackHandler()
    


