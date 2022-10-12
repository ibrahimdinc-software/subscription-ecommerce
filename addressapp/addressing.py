import json


class Address():
    def provList(self):
        with open("addressapp/data.json", encoding="utf-8") as data_file:
            data = json.load(data_file)
            list = []
            for info in data:
                list.append(info["il"])
            return list

    def distWid(self, id):
        with open("addressapp/data.json", encoding="utf-8") as data_file:
            data = json.load(data_file)
            list = []
            for info in data:
                if id == info["il"]:
                    for district in info["ilceleri"]:
                        list.append(district)
            return list
