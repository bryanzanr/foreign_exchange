import requests
import json
import time


def get_server_data():
    req = requests.get('https://api.myjson.com/bins/rr49j')
    req_status = req.content.decode()
    status = json.loads(req_status)
    # parsed_status = status.get("status")
    return status


def change_server_status():
    param = {"status": False, "image": ""}
    data = json.dumps(param)
    headers = {'Content-type': 'application/json'}
    link = 'https://api.myjson.com/bins/rr49j'
    requests.put(link, data=data, headers=headers)
    print(">> change server status complete")


def main():
    # main method
    while(True):
        status = get_server_data().get("status")
        # image_url = get_server_data().get("image")
        if(status is True):
            print("status is true, downloading image")
            print("download complete")
            change_server_status()
        else:
            print("status is false, re-looping")
            time.sleep(2)


if __name__ == '__main__':
    main()
