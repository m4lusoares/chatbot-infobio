import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai

genai.configure(api_key='AIzaSyDKKADe2mzk7Nez3G9UjRxw_vLBUbiPKYU') 

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Erro ao instanciar o modelo: {e}")

# função para gerar textos
def generate_text():
    try:
        prompt = input_text.get("1.0", tk.END).strip()  #obtem texto d entrada
        if prompt: 
            # metodo para gerar o texto
            response = model.generate_content(prompt) 
            output_text.delete("1.0", tk.END)  
            output_text.insert(tk.END, response.text)  # insere resposta na área de saída
        else:
            output_text.delete("1.0", tk.END)  
            output_text.insert(tk.END, "Por favor, insira uma pergunta.")  
    except Exception as e:
        output_text.delete("1.0", tk.END)  
        output_text.insert(tk.END, f"Erro: {e}") 

# função p sair 
def exit_app():
    root.quit()

# configura a janela principal
root = tk.Tk()
root.title("Chatbot hihihi")

# cores para fonte e fundo das caixas de texto
bg_color = "#1C1C1C"  
fonte_color = "#FFFFFF" 

# cria o painel
panel = tk.Frame(root, bg=bg_color)
panel.pack(padx=10, pady=10)

# label p pergunta
input_label = tk.Label(panel, text="Qual sua pergunta?", bg=bg_color, fg=fonte_color)
input_label.pack()

# cria a caixa de texto para pergunta
input_text = scrolledtext.ScrolledText(panel, wrap=tk.WORD, width=50, height=8, bg="#363636", fg=fonte_color)  
input_text.pack()

# botão para enviar
send_button = tk.Button(panel, text="Enviar", command=generate_text, bg="#1C1C1C", fg="white")  
send_button.pack(pady=(5, 10))

# texto da area de saída
output_label = tk.Label(panel, text="Resposta:", bg=bg_color, fg=fonte_color)
output_label.pack()

# area que sai o texto
output_text = scrolledtext.ScrolledText(panel, wrap=tk.WORD, width=50, height=8, bg="#1C1C1C", fg=fonte_color)
output_text.pack()

# botão para sair
exit_button = tk.Button(panel, text="Sair", command=exit_app, bg="#1C1C1C", fg="white") 
exit_button.pack()

# loop da interface
root.mainloop()
