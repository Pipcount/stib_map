import requests, json

url = "https://data.stib-mivb.brussels/api/explore/v2.1/catalog/datasets/vehicle-position-rt-production/records?limit=100"

response = requests.get(url)

with open('stop-details-production.json', 'r') as f:
    stops_raw = json.load(f)

stops = []
for stop in stops_raw:
    stops.append({'id': stop['id'], 'name': stop['name'].split(',')[0].split(":")[1].strip(' "')})


def parse_locations(line):
    vehicle_positions = []
    for vehicle in line['vehiclepositions'].strip("[]{}").split('}, {'):
        dict = {'line' : line['lineid'],
                'direction' : vehicle.split(',')[0].split(':')[1].strip(' "'),
                'distance' : vehicle.split(',')[1].split(':')[1].strip(' "'),
                'stop' : vehicle.split(',')[2].split(':')[1].strip(' "'),
                }
        for stop in stops:
            if stop['id'][:4] == dict['direction']:
                dict['direction'] = stop['name']
            if stop['id'][:4] == dict['stop']:
                dict['stop'] = stop['name']
        vehicle_positions.append(dict)

    return vehicle_positions

if response.status_code == 200:
    print("Response received successfully!")
    data = json.loads(response.text)
    data['results'].sort(key=lambda x: x['lineid'])
    lines = []
    for line in data['results']:
        lines.append(parse_locations(line))

    for line in lines:
        for vehicle in line:
            if vehicle['line'] == '82':
                print(f"A vehicle of line {vehicle['line']} is {vehicle['distance']} meters away from {vehicle['stop']} in the direction of {vehicle['direction']} \n")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
