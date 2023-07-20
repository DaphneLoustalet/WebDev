import requests

url = "https://my.ucdavis.edu/schedulebuilder/"

response = requests.get(url)

if response.status_code == 200:
    print("Request was successful (200 OK).")
elif response.status_code == 404:
    print("Requested resource not found (404 Not Found).")
else:
    print(f"Server returned status code: {response.status_code}")
