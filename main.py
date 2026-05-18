from flask import Flask, request, Response
import requests
import os
import google.generativeai as genai

# Cargar variables de entorno desde .env si existe
from dotenv import load_dotenv
load_dotenv()


# Configura Gemini API Key
gemini_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)

app = Flask(__name__)

# Telegram BOT Token
token = os.environ.get("TELEGRAM_BOT_TOKEN")

# Función para generar respuesta con Gemini
def generate_answer(question):
    model = genai.GenerativeModel("gemini-2.0-flash")
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
        print("Payload recibido:", msg)

        chat_id = None
        try:
            chat_id, incoming_que = message_parser(msg)
            print("Pregunta recibida:", incoming_que)

            answer = generate_answer(incoming_que)
            print("Respuesta de Gemini:", answer)

            send_message_telegram(chat_id, answer)
        except KeyError:
            print("Mensaje sin texto, ignorado.")
        except Exception as e:
            print("Error:", e)
            if chat_id:
                try:
                    send_message_telegram(chat_id, "Lo siento, ocurrió un error. Intenta de nuevo.")
                except Exception:
                    pass

        return Response('ok', status=200)
    else:
        return "<h1>Bot corriendo con Gemini</h1>"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
