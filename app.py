from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MMGHTY'
load_dotenv()

greeting = ""
questions = []
with open("question.txt", "r") as f:
    lines = f.readlines()
    greeting = lines[0].strip().split(": ")[1]
    questions = [line.strip() for line in lines[1:]]

answers = {}

with open("answer.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.strip().split(": ")
        if len(parts) == 2:
            answers[parts[0]] = parts[1]

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
    phone_number = request.values['WaId']

    response = MessagingResponse()

    if incoming_msg == "Hello" or incoming_msg == "Hi":
        all_questions = "\n".join(questions)
        response.message(f"{greeting}\n{all_questions}")
    elif incoming_msg in [str(i + 1) for i in range(len(questions))]:
        question_index = int(incoming_msg) - 1
        response.message(answers.get(str(question_index + 1), "Sorry, I couldn't find an answer for that question."))
    elif incoming_msg in answers:
        response.message(answers[incoming_msg])
        sendMessage(answers[incoming_msg], phone_number)
    else:
        response.message("I'm sorry, I didn't understand your message.")

    return str(response)

if __name__ == '__main__':
    app.run()
