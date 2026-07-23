import os
import requests

class WeatherFetcher:
    """Class to handle API requests and structure weather details."""
    
    BASE_URL = "https://wttr.in/"

    def __init__(self, city):
        self.city = city.strip()

    def fetch_weather(self):
        """Fetches live weather data in JSON format from the open API service."""
        # 'format=j1' tells wttr.in to give us raw JSON back instead of plain text
        target_url = f"{self.BASE_URL}{self.city}?format=j1"
        
        try:
            # Send HTTP GET request to the web server
            response = requests.get(target_url, timeout=5)
            
            # Check for HTTP status errors (like 404 or 500)
            response.raise_for_status()
            
            # Parse the incoming JSON string into a native Python dictionary
            return response.json()
            
        except requests.exceptions.ConnectionError:
            print("❌ Internet Error: Unable to connect to the weather service. Check your connection.")
            return None
        except requests.exceptions.Timeout:
            print("⏳ Timeout Error: The weather server took too long to respond.")
            return None
        except requests.exceptions.HTTPError as err:
            print(f"❌ HTTP Error encountered: {err}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

    def display_report(self, data):
        """Parses the nested JSON dictionary and prints formatted results."""
        if not data:
            return

        try:
            # Navigate nested JSON dictionaries
            current = data['current_condition'][0]
            area = data['nearest_area'][0]

            city_name = area['areaName'][0]['value']
            country = area['country'][0]['value']
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            feels_like_c = current['FeelsLikeC']
            condition = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']

            print("\n" + "="*40)
            print(f"🌍 LIVE WEATHER REPORT: {city_name.upper()}, {country.upper()}")
            print("="*40)
            print(f"🌤️  Condition:    {condition}")
            print(f"🌡️  Temperature:  {temp_c}°C ({temp_f}°F)")
            print(f"🤔 Feels Like:   {feels_like_c}°C")
            print(f"💧 Humidity:     {humidity}%")
            print(f"💨 Wind Speed:   {wind_speed} km/h")
            print("="*40)

        except (KeyError, IndexError):
            print("❌ Error: Could not parse the city data. Make sure you typed a valid city name!")


def main():
    print("=== 🌤️ PYTHON REAL-TIME WEATHER APP ===")
    
    while True:
        city = input("\nEnter a city name (or 'exit' to quit): ").strip()
        
        if city.lower() == 'exit':
            print("Closing Weather App. Stay safe out there!")
            break
            if not city:
                print("Please enter a valid city name.")
                continue

        print(f"\n📡 Contacting weather servers for '{city}'...")
        
        # Combine OOP and HTTP Requests
        tracker = WeatherFetcher(city)
        weather_data = tracker.fetch_weather()
        tracker.display_report(weather_data)


if __name__ == "__main__":
    main()