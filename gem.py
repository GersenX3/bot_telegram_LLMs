import google.generativeai as genai
import os
from dotenv import load_dotenv 
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

resp = model.generate_content("Hola Gemini, dime un chiste corto")
print(resp.text)
