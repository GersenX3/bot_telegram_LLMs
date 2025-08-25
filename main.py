from flask import Flask, request, Response
import requests
import os
import google.generativeai as genai

# Configura Gemini API Key
gemini_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)

app = Flask(__name__)

# Telegram BOT Token
token = os.environ.get("TELEGRAM_BOT_TOKEN")

# Función para generar respuesta con Gemini
def generate_answer(question):
    model = genai.GenerativeModel("gemini-1.5-flash")  # puedes usar gemini-1.5-pro también
    response = model.generate_content(question)
    return response.text.strip() if response.text else "Lo siento, no pude generar una respuesta."

# Parsear mensaje de Telegram
def message_parser(message):
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    print("Chat ID: ", chat_id)
    print("Message: ", text)
    return chat_id, text

# Enviar mensaje a Telegram
def send_message_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        print("Payload recibido:", msg)  # 👈 Debug

        chat_id, incoming_que = message_parser(msg)
        print("Pregunta recibida:", incoming_que)  # 👈 Debug

        answer = generate_answer(incoming_que)
        print("Respuesta de Gemini:", answer)  # 👈 Debug

        resp = send_message_telegram(chat_id, answer)
        print("Respuesta de Telegram API:", resp.json())  # 👈 Debug

        return Response('ok', status=200)
    else:
        return "<h1>Bot corriendo con Gemini</h1>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
