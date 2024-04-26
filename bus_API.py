import requests

apiKey = "c7f9574084c5817d26ebe99fe521b4a6e97d28fb"

def fetchData(url):
    response = requests.get(url + f'/?api_key={apiKey}')
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return None
