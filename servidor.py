from flask import Flask, request
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World From Flask!"

@app.route("/email", methods=['POST'])
def email():
    print(os.environ.get("SENDGRID_API_KEY"))
    print(request.form["message"])
    hash = request.form['hash_validator']

    print(os.environ.get("HASH_VALIDATOR"))
    print(hash)
   
    
    if(hash == os.environ.get("HASH_VALIDATOR")):
        print("Entrooooooooooooooooooooooooooooooo")
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = request.form['destination']
            subject = request.form['subject']
            message_content = request.form['message']
            print(to,subject,message_content)

            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                mensaje = Mail(
                from_email=email_sender,
                to_emails=to,
                subject=subject,
                html_content=message_content)
            
            
                respuesta = sg.send(mensaje)
                print(respuesta.status_code)
                print(respuesta.body)
                print(respuesta.headers)
                return "OK"
            except Exception as e:
                return "KO"
        except:
            return "Faltan datos"
           
    else:
        return "Hash error"

if __name__=='__main__':
    app.run()
