import os
from flask import Flask, jsonify, render_template, request
from database.noticia import Noticia

app = Flask(__name__)
noticia_dao = Noticia()
UPLOAD_FOLDER = "static/imgs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/criar-noticia')
def criarNoticias():
    return render_template('criar-noticia.html')

@app.route('/listar-noticias')
def listarNoticias():
    noticias = noticia_dao.listar_todas()
    print(noticias)
    return render_template('noticias.html', noticias=noticias)

@app.route('/noticia')
def noticia():
    return render_template('noticia.html')

@app.route("/cadastro", methods=["POST"])
def cadastrar():
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    categoria = request.form.get("categoria")
    imagem = request.files.get("imagem")

    nome_img = None
    if imagem and imagem.filename != "":
        nome_img = imagem.filename
        caminho = os.path.join(UPLOAD_FOLDER, nome_img)
        imagem.save(caminho)

    sucesso = noticia_dao.criarNoticia(titulo, descricao, categoria, nome_img)
    return jsonify({"sucesso": sucesso})

    

if __name__ == '__main__':
    app.run(debug=True)