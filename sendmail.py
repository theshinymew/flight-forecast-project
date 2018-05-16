import sendgrid
import os
from sendgrid.helpers.mail import *
import base64

def sendemail(recipient, emailSubject, body):
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('SENDGRID_API_KEY'))
    
    from_email = Email("app95271153@heroku.com")
    to_email = Email(recipient)
    content = Content("text/plain", body)
    
    with open("flight-forecast.py.png", 'rb') as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    attachment = Attachment()
    attachment.content = encoded
    attachment.type = "image/png"
    attachment.filename = "graph.png"
    attachment.disposition = "attachment"
    attachment.content_id = "PNG Image file"
    
    mail = Mail(from_email, emailSubject, to_email, content)
    mail.add_attachment(attachment)
    
    response = sg.client.mail.send.post(request_body = mail.get())
    print("### Email sent to: "+ recipient + " ###")
    print(response.status_code)
    print(response.body)
    print(response.headers)