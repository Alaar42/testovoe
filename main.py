import requests
import json
import pprint

url = 'http://127.0.0.1:5000/json-example'
data = {"login": "user123",
        "pass": "pass123"}


# data_json  = simplejson.dumps(data)
# payload = {'json_payload': data_json}
# print(payload)
r = requests.post(url, json=data)
#datanew = r.json()
print(r)

