# Importa a classe Flask (para criar o servidor)
# e render_template (para renderizar páginas HTML)
from flask import Flask, render_template

# Cria a aplicação Flask
app = Flask(__name__)

# Define a rota principal ("/" = página inicial)
@app.route("/")
def home():
    return render_template("index.html")  # Renderiza a página index.html

if __name__ == "__main__":
    app.run(debug=True)