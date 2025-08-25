import requests
import json
import os

# --- PASO 1: Configurar tu clave de API ---
# Reemplaza 'TU_API_KEY_AQUI' con tu clave real de la API de Gemini.
# Es una buena práctica usar variables de entorno para las claves,
# pero para esta prueba, la pondremos directamente aquí.
# Obtén tu clave aquí: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyBsoV3Z0Ez2UOv09KNeZLUOTvWNtMmtZBo"
print(GEMINI_API_KEY)

# --- PASO 2: Definir la URL de la API y los encabezados ---
# Esta es la URL del modelo gemini-2.0-flash, como en tu ejemplo de curl.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {
    'Content-Type': 'application/json',
    # La clave de API se envía como un parámetro en la URL en este caso,
    # no en un encabezado 'X-goog-api-key'. La siguiente línea es solo
    # una nota para referencia de cómo se haría.
    # 'X-goog-api-key': GEMINI_API_KEY,
}
# La clave de API se agrega como un parámetro en la URL.
params = {'key': GEMINI_API_KEY}

# --- PASO 3: Definir el cuerpo (payload) de la solicitud ---
# Este es el mismo JSON que usaste en tu comando curl.
# La "conversación" se envía dentro de la lista 'contents'.
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works in a few words"
                }
            ]
        }
    ]
}

# --- PASO 4: Enviar la solicitud POST y manejar la respuesta ---
try:
    # Hacemos la solicitud POST a la URL de la API.
    # El 'json' es el cuerpo de la solicitud y 'params' agrega la clave a la URL.
    print("Enviando solicitud a la API de Gemini...")
    response = requests.post(API_URL, json=payload, params=params)
    
    # Verificamos si la solicitud fue exitosa.
    response.raise_for_status()
    
    # Parseamos la respuesta JSON.
    data = response.json()
    
    # Navegamos a través del JSON para obtener el texto generado.
    # El camino es: data -> candidates[0] -> content -> parts[0] -> text
    generated_text = data['candidates'][0]['content']['parts'][0]['text']
    
    # --- PASO 5: Imprimir la respuesta ---
    print("\n--- Respuesta de la API ---")
    print(generated_text)
    
except requests.exceptions.RequestException as e:
    # Manejamos errores de red o del servidor.
    print(f"\n❌ Error de solicitud: {e}")
    print(f"Respuesta del servidor: {response.text}")
except (KeyError, IndexError) as e:
    # Manejamos errores si la estructura de la respuesta no es la esperada.
    print(f"\n❌ Error al analizar la respuesta JSON: {e}")
    print(f"Respuesta completa: {response.text}")

