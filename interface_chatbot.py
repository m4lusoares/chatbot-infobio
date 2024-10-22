import tkinter as tk
from tkinter import scrolledtext, Toplevel
import sqlite3
import google.generativeai as genai
import chaves

genai.configure(api_key=chaves.api_key)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Erro ao instanciar o modelo: {e}")

# Configura o banco de dados
def setup_database():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar no banco de dados
def save_to_database(pergunta, resposta):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO conversa (pergunta, resposta) VALUES (?, ?)', (pergunta, resposta))
    conn.commit()
    conn.close()

# Função para gerar textos
def generate_text():
    try:
        prompt = input_text.get("1.0", tk.END).strip()  # Obtem texto de entrada
        if prompt:
            # Método para gerar o texto
            response = model.generate_content(prompt)
            resposta_texto = response.text
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, resposta_texto)  # Insere resposta na área de saída
            
            # Salva a pergunta e resposta no banco de dados
            save_to_database(prompt, resposta_texto)
        else:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "Por favor, insira uma pergunta.")
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Erro: {e}")

# Função para acessar e exibir os dados
def show_history():
    history_window = Toplevel(root)  # Cria uma nova janela
    history_window.title("Histórico de Perguntas e Respostas")
    history_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, width=60, height=20, bg="#1C1C1C", fg="white")
    history_text.pack()

    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pergunta, resposta FROM conversa')
    records = cursor.fetchall()
    conn.close()

    if records:
        for record in records:
            pergunta, resposta = record
            history_text.insert(tk.END, f"Pergunta: {pergunta}\nResposta: {resposta}\n\n")
    else:
        history_text.insert(tk.END, "Nenhum histórico encontrado.")

# Função para limpar o histórico
def clear_history():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM conversa')  # Apaga todos os registros
    conn.commit()
    conn.close()
    output_text.delete("1.0", tk.END)  # Limpa o campo de saída
    output_text.insert(tk.END, "Histórico limpo com sucesso.")

# Função para sair
def exit_app():
    root.quit()

# Configura a janela principal
root = tk.Tk()
root.title("Chatbot hihihi")

# Cores para fonte e fundo das caixas de texto
bg_color = "#1C1C1C"
fonte_color = "#FFFFFF"

# Cria o painel
panel = tk.Frame(root, bg=bg_color)
panel.pack(padx=10, pady=10)

# Label para pergunta
input_label = tk.Label(panel, text="Qual sua pergunta?", bg=bg_color, fg=fonte_color)
input_label.pack()

# Cria a caixa de texto para pergunta
input_text = scrolledtext.ScrolledText(panel, wrap=tk.WORD, width=50, height=8, bg="#363636", fg=fonte_color)
input_text.pack()

# Botão para enviar
send_button = tk.Button(panel, text="Enviar", command=generate_text, bg="#1C1C1C", fg="white")
send_button.pack(pady=(5, 10))

# Botão para ver histórico
history_button = tk.Button(panel, text="Ver Histórico", command=show_history, bg="#1C1C1C", fg="white")
history_button.pack(pady=(5, 10))

# Botão para limpar histórico
clear_button = tk.Button(panel, text="Limpar Histórico", command=clear_history, bg="#1C1C1C", fg="white")
clear_button.pack(pady=(5, 10))

# Texto da área de saída
output_label = tk.Label(panel, text="Resposta:", bg=bg_color, fg=fonte_color)
output_label.pack()

# Área que sai o texto
output_text = scrolledtext.ScrolledText(panel, wrap=tk.WORD, width=50, height=8, bg="#1C1C1C", fg=fonte_color)
output_text.pack()

# Botão para sair
exit_button = tk.Button(panel, text="Sair", command=exit_app, bg="#1C1C1C", fg="white")
exit_button.pack()

# Chama a função para configurar o banco de dados
setup_database()

# Loop da interface
root.mainloop()
