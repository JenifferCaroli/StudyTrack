# Importa a classe Flask (para criar o servidor)
# e render_template (para renderizar páginas HTML)
from flask import Flask, render_template

# Lista temporária para armazenar matérias (simulando banco de dados)
from flask import request

# Lista temporária para armazenar matérias (simulando banco de dados)
materias = []

# Cria a aplicação Flask
app = Flask(__name__)

# Define a rota principal ("/" = página inicial)
@app.route("/")
def home():
    return render_template("index.html")  # Renderiza a página index.html
# Rota para cadastro de matérias
@app.route("/materias", methods=["GET", "POST"])
def cadastro_materias():

# Se o usuário enviar o formulário
    if request.method == "POST":
        nome_materia = request.form.get("nome")
# Adiciona na lista
        materias.append(nome_materia)

# Envia a lista para o HTML
    return render_template("materias.html", materias=materias)       
if __name__ == "__main__":                      
    app.run(debug=True)