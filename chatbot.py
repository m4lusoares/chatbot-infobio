import google.generativeai as genai

genai.configure(api_key="AIzaSyDKKADe2mzk7Nez3G9UjRxw_vLBUbiPKYU")

#model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Quantos dias tem um ano?")

print(response.text)