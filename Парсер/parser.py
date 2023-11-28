import requests
import json
import fake_useragent
phone_name = []
phone_GB = []
phone_price = []
URL = 'https://catalog.onliner.by/sdapi/catalog.api/search/mobile?mfr[0]=apple&mobile_type[0]=smartphone&mobile_type[operation]=union&group=1'
user = fake_useragent.UserAgent().random
headers = {'user-agent': user}
response = requests.get(URL, headers=headers)

json_data = json.loads(response.text)
products = json_data['products']


for elements in products:

    GB = elements["micro_description_list"][1].split()
    phone_name.append(elements['extended_name'])
    phone_GB.append(int(GB[1]))
    phone_price.append(float(elements['prices']['price_min']['amount']))







