import sendgrid
import os
from sendgrid.helpers.mail import *

def sendemail(recipient, emailSubject, body):
    sg = sendgrid.SendGridAPIClient(apikey = os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("app95271153@heroku.com")
    to_email = Email(recipient)
    content = Content("text/plain", body)
    mail = Mail(from_email, emailSubject, to_email, content)
    response = sg.client.mail.send.post(request_body = mail.get())

    print("### Email sent to: "+ recipient + " ###")
    print(response.status_code)
    print(response.body)
    print(response.headers)

if __name__ == "__main__":
    sendemail('alejandropons17@gmail.com', "test header", "test body")