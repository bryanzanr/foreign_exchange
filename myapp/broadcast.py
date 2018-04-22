# from django.shortcuts import redirect
import requests
import json
import os


def main(temp):
    arr = []
    # line = json.load(open('website/myapp/static/text/image.txt'))
    # for i in range(len(line)):
    #     image.append(line[i]['link'])
    #     author.append(line[i]['user'])
    title = [li['title'] for li in temp]
    desc = [li['description'] for li in temp]
    image = []
    latitude = [li['lat'] for li in temp]
    longitude = [li['long'] for li in temp]
    author = [li['author'] for li in temp]
    publish = [li['publish'] for li in temp]
    for li in temp:
        try:
            image.append(li['img'])
        except KeyError:
            image.append('')
        # try:
        #     latitude.append(li['lat'])
        #     longitude.append(li['long'])
        # except KeyError:
        #     latitude.append('')
        #     longitude.append('')
    for i in range(len(image)):
        param = {"title": title[i], "description": desc[i],
                 "image": image[i], "author": author[i], "publish": publish[i],
                 "lat": latitude[i], "long": longitude[i]}
        arr.append(param)
    ads = {"advertisements": arr}
    data = json.dumps(ads)
    headers = {'Content-type': 'application/json'}
    link = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    try:
        # req_change = requests.put(link, data=data, headers=headers)
        requests.put(link, data=data, headers=headers)
    except ConnectionError:
        # return redirect('response/', {'no_record_check': 0})
        return False
    # print(req_change.content.decode())
    # print(">> change server status complete")
    return True


# if __name__ == "__main__":
#     main()
