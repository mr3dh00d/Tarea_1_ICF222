import json

__file = open("environments.json")
ENV = json.load(__file)
__file.close()