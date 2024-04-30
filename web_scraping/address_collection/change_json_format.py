import json

new_dict = {}
file_path = r"output/addresses.json"
with open(file_path, "r") as json_file:
    addresses = json.load(json_file)["addresses"]
    for item in addresses:
        if item["state"] not in new_dict.keys():
            new_dict[item["state"]] = {}
        if item["city"] not in new_dict[item["state"]].keys():
            new_dict[item["state"]][item["city"]] = {}
        if item["neighborhood"] not in new_dict[item["state"]][item["city"]].keys():
            new_dict[item["state"]][item["city"]][item["neighborhood"]] = []
        new_dict[item["state"]][item["city"]][item["neighborhood"]].append(item["street"])
with open(file_path, "w") as json_file:
    json.dump(new_dict, json_file, ensure_ascii=False, indent=4)