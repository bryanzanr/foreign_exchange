# from django.shortcuts import redirect
# from google.cloud import storage
# from PIL import Image
# import random
import requests
# import json
import os
# import pyrebase


def main(temp, auth, firebase):
    arr = []
    # client = storage.Client.from_service_account_json('Flyit-dbdcc3a8581e.json')
    # bucket = client.get_bucket('flyit-e0aa3.appspot.com')
    # blob = bucket.blob('Architecture.jpg')
    # blob.upload_from_filename(filename='Architecture.jpg')
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
    tag = [li['tag'] for li in temp]
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
                 "lat": latitude[i], "long": longitude[i], "tag": tag[i]}
        arr.append(param)
    ads = {"advertisements": arr}
    # Get a reference to the auth service
    # Log the user in
    user = auth.sign_in_with_email_and_password(os.environ['FIREBASE_EMAIL'],
                                                os.environ['SENDGRID_PASSWORD'])
    # Get a reference to the database service
    db = firebase.database()
    db.child('advertisements').child(
        '-LBYvWae4P3F3rZsgepL').update(ads, user['idToken'])
    # data = json.dumps(ads)
    link = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    try:
        # req_change = requests.put(link, data=data, headers=headers)
        requests.put(link, json=ads)
    except ConnectionError:
        # return redirect('response/', {'no_record_check': 0})
        return False
    # print(req_change.content.decode())
    # print(">> change server status complete")
    return True


# if __name__ == "__main__":
#     main()
