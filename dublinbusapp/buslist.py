import json
from pprint import pprint

def makeBusStopDict():
    """
    Creates list of dictionaries containing all stopid's and their lat/long info
    """
    with open('busstopinformation.json', encoding='utf8') as f:
        data = json.load(f)

    # Create empty list of dictionaries to be filled
    buslist = [dict() for x in range(len(data["results"]))]

    for i in range(0, len(buslist)):
        buslist[i]["stopid"] = data["results"][i]["stopid"]
        buslist[i]["latitude"] = data["results"][i]["latitude"]
        buslist[i]["longitude"] = data["results"][i]["longitude"]

    return buslist