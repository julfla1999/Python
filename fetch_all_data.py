import requests

url = 'https://api.nbp.pl/api/exchangerates/tables/a/'
for year in range(2002,2024,1):
    response = requests.get(url + str(year) + "-01-01/" + str(year) + "-03-31" + "/?format=json")
    with open('historical_data/' + str(year) + "_1" + '.json', 'wb') as f:
        f.write(response.content)

    response = requests.get(url + str(year) + "-04-01/" + str(year) + "-06-30" + "/?format=json")
    with open('historical_data/' +str(year) + "_2" + '.json', 'wb') as f:
        f.write(response.content)

    response = requests.get(url + str(year) + "-07-01/" + str(year) + "-09-30" + "/?format=json")
    with open('historical_data/' +str(year) + "_3" + '.json', 'wb') as f:
        f.write(response.content)

    response = requests.get(url + str(year) + "-10-01/" + str(year) + "-12-31" + "/?format=json")
    with open('historical_data/' +str(year) + "_4" + '.json', 'wb') as f:
        f.write(response.content)
