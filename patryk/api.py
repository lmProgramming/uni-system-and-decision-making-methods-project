import requests
import json
import os


class api:
    baseUrl: str = "http://apps.who.int/gho/athena/api/"
    formatter: str = "?format=json"
    countries: dict = {}
    dimensions: dict = {}
    indicators: dict = {}

    def getCountries(self, write=False) -> dict:
        if os.path.exists('data/countries.json') and not write:
            with open('data/countries.json', "r", encoding="utf-8") as f:
                self.countries = json.load(f)
                return self.countries
        response = requests.get(f'{self.baseUrl}/COUNTRY{self.formatter}')

        if response.status_code == 200:
            data = json.loads(response.text)
            for entry in data["dimension"][0]["code"]:
                self.countries[entry["label"]] = entry["display"]
        else:
            print('No response')

        if write:
            with open("data/countries.json", "a+", encoding="utf-8") as f:
                f.truncate(0)
                json.dump(self.countries, f, indent=4)
        return self.countries

    def getDimensions(self, write=False) -> dict:
        '''Get the dimensions of the GHO API,
           if wirte is True, it will write the data to a json file.\n
           If data has been already written, retrieve data from a file'''
        if os.path.exists('data/dimensions.json') and not write:
            with open('data/dimensions.json', "r", encoding="utf-8") as f:
                self.dimensions = json.load(f)
        response = requests.get(f"{self.baseUrl}{self.formatter}")
        if response.status_code == 200:
            self.dimensions = json.loads(response.text)["dimension"]
        else:
            print('No response')
            return []
        if write:
            with open("data/dimensions.json", "a+", encoding="utf-8") as f:
                f.truncate(0)
                json.dump(self.dimensions, f, indent=4)
        return self.dimensions

    def getIndicators(self, dimension: str, write=False) -> dict:
        '''Get the indicators of a specific dimension,
           if wirte is True, it will write the data to a json file.\n
           If data has been already written, retrieve data from a file\n
           To get list of dimensions, use getDimensions() method'''
        if os.path.exists('data/indicators.json') and not write:
            with open('data/indicators.json', "r", encoding="utf-8") as f:
                self.indicators = json.load(f)
                return self.indicators
        response = requests.get(f"{self.baseUrl}/{dimension}{self.formatter}")
        if response.status_code == 200:
            responseData: dict = json.loads(response.text)
            for entry in responseData["dimension"][0]["code"]:
                self.indicators[entry["label"]] = entry["display"]
        else:
            print('No response')
            return
        if write:
            with open("data/indicators.json", "a+", encoding="utf-8") as f:
                f.truncate(0)
                json.dump(self.indicators, f, indent=4)
        return self.indicators

    def getValues(self, indicator: str, wirte=False) -> dict:
        '''Get the values of a specific indicator in the GHO dimension.
           If wirte is True, it will write the data to a json file.\n
           If data has been already written, retrieve data from a file
           To get list of indicators, use getIndicators('GHO') method'''
        if not self.countries:
            self.getCountries()
        if os.path.exists(f'data/{indicator}.json') and not wirte:
            with open(f'data/{indicator}.json', "r", encoding="utf-8") as f:
                return json.load(f)
        response = requests.get(
            f"{self.baseUrl}/GHO/{indicator}{self.formatter}"
        )
        display = "No data avaliable"
        values: dict = {}
        if response.status_code == 200:
            responseData: dict = json.loads(response.text)
            if responseData["fact"] == []:
                return {"indicator": indicator, "display": display, "values": values}
            for entry in responseData["fact"]:
                country = ""
                for dim in entry["Dim"]:
                    if dim["category"] == "COUNTRY":
                        country = dim["code"]
                        break
                if not country:
                    continue
                if entry["value"]["numeric"]:
                    value = entry["value"]["numeric"]
                else:
                    try:
                        value = float(entry["value"]["display"])
                    except ValueError:
                        value = None
                values[country] = value
            display = responseData["dimension"][0]["code"][0]["display"]
        if wirte:
            for country in self.countries:
                if country not in values.keys():
                    values[country] = None
            self.writeIndicatorValues({"indicator": indicator, "display": display, "values": values})
        return {"indicator": indicator, "display": display, "values": values}

    def writeIndicatorValues(self, data: dict) -> None:
        '''Write the indicator data to a json file if the data is not empty\n
           If the the data is not empty, it will write the data to a json file and add the indicator to the avaliable.txt file\n'''
        if data["values"] == {}:
            return
        with open(f'data/{data["indicator"]}.json', "a+", encoding="utf-8") as f:
            f.truncate(0)
            json.dump(data, f, indent=4)
        with open("data/avaliable.txt", "a") as f:
            f.write(f'{data['indicator']} - {data["display"]}\n')

    def combineIndicators(self, indicators: list[dict]):
        '''Combine multiple indicators into a single dict,
           where the key is the country name and the value is a dict
           with the indicator name as the key and the value as the value'''
        countries = self.getCountries()
        combined = {k: {} for k in countries.values()}
        for indicator in indicators:
            for country, value in indicator["values"].items():
                combined[countries[country]][indicator["display"]] = value
        return combined


if __name__ == "__main__":
    # Example of how to use the api class
    _api = api()
    countries = _api.getCountries()
    indicators = _api.getIndicators("GHO")
    # list all indicators from the GHO dimension
    for i, (indicator, display) in enumerate(indicators.items()):
        print(f"{indicator} - {display}")
        if i == 10:
            break
    # indicator = "WHOSIS_000001" contains data about the life expectancy per country
    lifeExpectancy = _api.getValues("WHOSIS_000001")
    # indicator = "RS_576" contains data about gni per capita
    gniPerCapita = _api.getValues("RS_576")
    # combine the data from the two indicators
    combined = _api.combineIndicators([lifeExpectancy, gniPerCapita])
    print(combined)
    # note - not all indicators contain data, and some indicators contain data only for a specific set of countries
