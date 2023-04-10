import os
import json

def getJsonCount():
    cwd = os.getcwd()
    jsonCount = 0
    for file in os.listdir(cwd):
        if file.endswith('.json'):
            jsonCount += 1
    return int(jsonCount)

def writeStackToJson(stackIn):
    writeName = "{}_{}".format(stackIn.name, getJsonCount())
    with open(("{}.json".format(writeName)), 'w') as f:
        json.dump(stackIn.to_json(), f, indent=4)