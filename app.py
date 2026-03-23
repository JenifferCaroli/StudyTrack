# Importa a classe Flask (para criar o servidor)
# e render_template (para renderizar páginas HTML)
from flask import Flask, render_template, request
from flask import redirect, url_for

import sqlite3

# Cria a aplicação Flask
app = Flask(__name__)

def conectar_db():
    return sqlite3.connect("database.db")

# Criar tabela se não existir
def criar_tabela():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    # Execute ao iniciar
criar_tabela()

# Define a rota principal ("/" = página inicial)
@app.route("/")
def home():
    return render_template("index.html")  # Renderiza a página index.html
# Rota para cadastro de matérias
@app.route("/materias", methods=["GET", "POST"])
def cadastro_materias():

    conn = conectar_db()
    cursor = conn.cursor()

# Se o usuário enviar o formulário
    if request.method == "POST":
        nome_materia = request.form.get("nome")
    
        if nome_materia:
            cursor.execute(
                "INSERT INTO materias (nome) VALUES (?)", 
                (nome_materia,)
            )
            conn.commit()
            conn.close()

            return redirect(url_for("cadastro_materias"))
# Buscar todas as matérias 
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()
  
    conn.close()

    return render_template("materias.html", materias=materias)
if __name__ == "__main__":                      
    app.run(debug=True)