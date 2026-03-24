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
# Tabela de matérias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

# Tabela de tarefas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status INTEGER DEFAULT 0,
        materia_id INTEGER,
        FOREIGN KEY (materia_id) REFERENCES materias(id)
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

# Rota para excluir matéria
@app.route("/excluir/<int:id>")
def excluir_materia(id):
    
    conn = conectar_db()
    cursor = conn.cursor()

    # Deletar pelo ID
    cursor.execute("DELETE FROM materias WHERE id = ?", (id,))
    conn.commit()

    conn.close()

    # Redirecionar de volta para a página de matérias
    return redirect(url_for("cadastro_materias"))

# Editar matérias
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_materias(id):

    conn = conectar_db()
    cursor = conn.cursor()

    if request.method == "POST":
        novo_nome = request.form.get("nome")

        if novo_nome:
            cursor.execute(
                "UPDATE materias SET nome = ? WHERE id = ?",
                (novo_nome, id)
            )
            conn.commit()
            conn.close()

            return redirect(url_for("cadastro_materias"))
        # Busccar materias atual
    cursor.execute("SELECT * FROM materias WHERE id = ?", (id,))
    materia = cursor.fetchone()

    conn.close()

    return render_template("editar.html", materia=materia)

# Rota para ver tarefas
@app.route("/tarefas/<int:materia_id>", methods=["GET", "POST"])
def tarefas(materia_id):

    conn = conectar_db()
    cursor = conn.cursor()

    # Adicionar nova tarefa
    if request.method == "POST":
        nome_tarefa = request.form.get("nome")

        if nome_tarefa:
            cursor.execute(
                "INSERT INTO tarefas (nome, materia_id) VALUES (?, ?)",
                (nome_tarefa, materia_id)
            )
            conn.commit()

            return redirect(url_for("tarefas", materia_id=materia_id))
            
 # Buscar tarefas da matéria
    cursor.execute(
        "SELECT * FROM tarefas WHERE materia_id = ?",
        (materia_id,)
    )    
        
    tarefas = cursor.fetchall()

    conn.close()

    return render_template("tarefas.html", tarefas=tarefas)

  
if __name__ == "__main__":
    app.run(debug=True)