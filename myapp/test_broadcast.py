import requests
import json

param = {"status": False, "image": ""}
data = json.dumps(param)
headers = {'Content-type': 'application/json'}
link = 'https://api.myjson.com/bins/rr49j'
req_change = requests.put(link, data=data, headers=headers)
print(req_change.content.decode())
print(">> change server status complete")
