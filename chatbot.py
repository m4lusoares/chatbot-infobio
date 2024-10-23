import google.generativeai as genai
import chaves

genai.configure(api_key=chaves.api_key)

#model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Quantos dias tem um ano?")

print(response.text)