import json

with open(r"output/realty_data/realties.json", "r") as json_file:
    realties = json.load(json_file)["realties"]
    print(len(realties))
    repeats = dict()  # Initialize an empty dictionary
    for item in realties:
        aux = item["realty_location"]["neighborhood"]
        if aux in repeats.keys():
            repeats[aux] += 1
        else:
            repeats[aux] = 1
    print(repeats)

    

        