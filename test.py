import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCd8KvANF4xdZMrCynUAGlTY1cfnKeeItc")

model = genai.GenerativeModel("models/gemini-2.0-flash")
res = model.generate_content("Me diga 3 frutas amarelas")

print(res.text)