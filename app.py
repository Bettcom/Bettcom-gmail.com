from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MMGHTY'

questions_and_answers = {
    "Hello": "Hi! How can I assist you today?",
    "Hi": "Hello! How can I help you?",
    "1": "Answer to question 1...",
    "2": "Answer to question 2...",
    "3": "Answer to question 3...",
}

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN") 
client = Client(account_sid, auth_token)

def sendMessage(body_mess, phone_number):
    print("BODY MESSAGE " + body_mess)
    message = client.messages.create(
                                from_='whatsapp:+14155238886',                  
                                body=body_mess,
                                to='whatsapp:' + phone_number                   
                            )
    print(message)                                                              


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values['Body']
    phone_number = (request.values['WaId'])

    response = MessagingResponse()
    
    if incoming_msg in questions_and_answers:
        if incoming_msg in ["Hello", "Hi"]:
            response.message(questions_and_answers[incoming_msg])
        else:
            response.message(questions_and_answers[incoming_msg])
            sendMessage(questions_and_answers[incoming_msg], phone_number)
    else:
        response.message("I'm sorry, I didn't understand your message.")

    return str(response)

if __name__ == '__main__':
    app.run()
