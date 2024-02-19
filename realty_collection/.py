import json

with open("output/realty_data/realties.json") as json_file:
    dict = json.load(json_file)
print(dict)
print(len(dict["realties"]))
print("foi")