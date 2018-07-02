import json
from pprint import pprint

def makeBusStopDict():
    with open('busstopinformation.json', encoding='utf8') as f:
        data = json.load(f)

    #pprint(data["results"][2]["latitude"])

    #pprint(len(data["results"]))

    dictlist = [dict() for x in range(len(data["results"]))]

    for i in range(0, len(dictlist)):
        dictlist[i]["stopid"] = data["results"][i]["stopid"]
        dictlist[i]["latitude"] = data["results"][i]["latitude"]
        dictlist[i]["longitude"] = data["results"][i]["longitude"]

    return dictlist

#print(makeBusStopDict())