import json
import requests


class WeatherForecast:
    def __init__(self):
        self.url = "https://eolink.o.apispace.com/456456/weather/v001/day"
        self.headers = {
            "X-APISpace-Token": "nvhoi17uexu3fufqacfl7xng7s6xlieh"
        }
        self.temperature = []
        self.humidity = []
        self.air_quality = []

    def get_forecast(self, days=8, areacode="101270101"):
        if self.humidity == [] or self.temperature == [] or self.air_quality == []:
            payload = {"days": days, "areacode": areacode}
            response = requests.request("GET", self.url, params=payload, headers=self.headers)
            data = json.loads(response.text)
            for forecast in data['result']['daily_fcsts']:
                self.temperature.append(forecast['high'])
                self.humidity.append(forecast['maxrh'])
                uv_scaled = ((forecast['uv'] - 0) / (10 - 0)) * (500 - 0) + 0
                self.air_quality.append(uv_scaled)
        else:
            pass

    def print_forecast(self):
        print("Temperature: ", self.temperature)
        print("Humidity: ", self.humidity)
        print("Air Quality: ", self.air_quality)

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_air_quality(self):
        return self.air_quality
