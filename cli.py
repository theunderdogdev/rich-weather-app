import requests as rq
from rich.panel import Panel
from rich import print
from rich.console import Console


class WeatherCli:
    def __init__(self, city: str, color="bright_green"):
        self.__console = Console()
        self.__color = color
        self.__api_key = "<your openweathermap api key here>"
        self.icon_map = {
            "01": "🌞",
            "02": "⛅️",
            "03": "☁️",
            "04": "🌤",
            "09": "🌧",
            "10": "🌦",
            "11": "⛈",
            "13": "❄️",
            "50": "🌫",
        }
        self.city = city.title()
        self.url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.__api_key}&units=metric"

    def perform_request(self, resp_return=False):
        try:
            response = rq.get(self.url)
            response = response.json()
            if response["cod"] == 200:
                if resp_return:
                    return response
                else:
                    self.parse_data(response)
            else:
                print("[bright_white on bright_red] Err [/] Invalid city!")
        except rq.exceptions.ConnectionError:
            self.__console.log(
                "[bright_red]Your internet connection seems to be offline![/]"
            )

    def temp__coloring(self, temp):
        colored_val = None
        if temp >= 30:
            colored_val = "bright_red"
        elif temp < 30 and temp >= 25:
            colored_val = "#ED6E26"
        elif temp < 25 and temp >= 20:
            colored_val = "#FFEA00"
        elif temp < 20 and temp >= 15:
            colored_val = "#00A975"
        elif temp < 15 and temp >= 10:
            colored_val = "#016EB5"
        elif temp < 10 and temp >= 5:
            colored_val = "#2854A3"
        else:
            colored_val = "#294C9F"
        return f"[{colored_val}]{temp}°C[/]"

    def parse_data(self, resp):
        long = resp["coord"]["lon"]
        lati = resp["coord"]["lat"]
        desc = resp["weather"][0]["description"]
        temp = resp["main"]["temp"]
        win_dir = resp["wind"]["deg"]
        speed = resp["wind"]["speed"]
        country = resp["sys"]["country"]
        timezone = resp["timezone"]
        icon = resp["weather"][0]["icon"][:-1]
        icon = self.icon_map[icon]
        main = resp["weather"][0]["main"]
        the_str = f"""Lati: [{self.__color}]{lati}[/]\tLong: [{self.__color}]{long}[/]\n\nDesc: [{self.__color}]{desc}[/]\
                    \n\nTemp: {self.temp__coloring(temp)}\
                    \n\nWind:[ \n\n\tSpeed: [{self.__color}]{speed} Km/h[/]\n\tDir  : [{self.__color}]{win_dir}[/]\n\n     ]\
                    """
        title = f"City: [{self.__color}]{self.city}[/]\t\tWeather: [{self.__color}]{main}[/] {self.icon_map['04']} "
        subtitle = f"Country: [bright_green]{country}[/]\tTimezone: [bright_green]{timezone}[/]"
        panel = Panel(the_str, title=title, subtitle=subtitle, padding=(0, 8))
        print(panel)


if __name__ == "__main__":
    console = Console()
    city = console.input("[green][i][b]City[/b][/i][/green] 📍:")
    WeatherCli(city=city).perform_request()
