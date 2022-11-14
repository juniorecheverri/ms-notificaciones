from flask import Flask, request
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

print(os.environ.get("SENDGRID_API_KEY"))
print(os.environ.get("NOMBRE"))
print(os.environ.get("HASH_VALIDATOR"))


app = Flask(__name__)


@app.route("/")
def hello():
    print("hhhhhhhh")
    return "Hello, World From Flask!"


@app.route("/email", methods=['POST'])
def email():

    print(os.environ.get("SENDGRID_API_KEY"))
    hash = request.form['hash_validator']

    if (hash == os.environ.get("HASH_VALIDATOR")):
        print("Entrooooooooooooooooooooooooooooooo")
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = request.form['destination']
            subject = request.form['subject']
            message_content = request.form['message']
           
            mensajito = json.loads(message_content)
         
            print(type(mensajito))
           
          
            print("#################")
            print(mensajito["mensaje"])
            print(mensajito["codigo"])

            
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                mensaje = Mail(
                from_email=email_sender,
                to_emails=to
                )

                mensaje.dynamic_template_data = {
                    "asunto": subject,
                    "mensaje":  mensajito["mensaje"],
                    "codigo": mensajito["codigo"]
                }
                if subject == "Codigo de Verificación":
                    mensaje.template_id = os.environ.get(
                        "IDPLANTILLAENVIOCODIGO")
                elif subject == "Recuperacion de Contraseña":
                    mensaje.template_id = os.environ.get(
                        "IDPLANTILLARECUPERARCONTRASENA")
                elif subject == "Cambio de Contraseña":
                    mensaje.template_id = os.environ.get(
                        "IDPLANTILLACAMBIOCONTRASENA")

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
        return "Hash"

if __name__=='__main__':
    app.run()
