# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
# import sys
# sys.path[0] = ''
import sendgrid
import os
import requests
from sendgrid.helpers.mail import Mail, Content, Email
from django.shortcuts import redirect


def main(arr, mail):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("support@fly-it.com")
    to_email = Email(mail)
    subject = "Welcome to Fly-It! Confirm Your Email"
    with open('email.html', 'r') as myfile:
        text = myfile.read()
    content = Content("text/plain", text)
    mail = Mail(from_email, subject, to_email, content)
    print(mail.get())
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

    # data = json.dumps(user)
    # headers = {'Content-type': 'application/json'}
    # link = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # try:
    #     req_change = requests.put(link, data=data, headers=headers)
    # data = json.dumps(user)
    user = {"user": arr}
    link = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    try:
        req_change = requests.put(link, json=user)
    except ConnectionError:
        return redirect('response/', {'no_record_check': 0})
    print(req_change.content.decode())
    print(">> change server status complete")

    # client = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    # message = sendgrid.Mail()

    # message.add_to("test@sendgrid.com")
    # message.set_from("you@youremail.com")
    # message.set_subject("Sending with SendGrid is Fun")
    # message.set_html("and easy to do anywhere, even with Python")

    # client.send(message)
