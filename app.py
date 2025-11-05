import os
from flask import Flask, jsonify, redirect, render_template, request
from database.noticia import Noticia
from database.comentario import Comentario

app = Flask(__name__)
noticia_dao = Noticia()
comentario_dao = Comentario()

UPLOAD_FOLDER = "static/imgs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔹 Página inicial
@app.route('/')
def home():
    noticias = noticia_dao.listar_todas()[:4]  # pega apenas as 4 mais recentes
    return render_template('home.html', noticias=noticias)


# 🔹 Listar todas as notícias
@app.route('/noticias')
def noticias():
    noticias = noticia_dao.listar_todas()
    return render_template('noticias.html', noticias=noticias)


# 🔹 Criar notícia
@app.route('/criar-noticia')
def criarNoticias():
    return render_template('criar-noticia.html')


# 🔹 Listar para edição
@app.route('/listar-noticias')
def listarNoticias():
    noticias = noticia_dao.listar_todas() 
    return render_template("listar-noticias.html", noticias=noticias)


# 🔹 Página da notícia (agora com comentários)
@app.route('/noticia/<int:id>', methods=["GET", "POST"])
def noticia(id):
    noticia = noticia_dao.buscarPorId(id)
    if not noticia:
        return "Notícia não encontrada", 404

    # Se o usuário enviar um comentário
    if request.method == "POST":
        autor = request.form.get("autor")
        comentario = request.form.get("comentario")

        if autor and comentario:
            comentario_dao.criarComentario(autor, comentario, id)

    # Atualiza views
    noticia_dao.incrementar_views(id)
    noticia['views'] = (noticia['views'] or 0) + 1

    # Lista comentários da notícia
    comentarios = comentario_dao.listarPorNoticia(id)

    return render_template('noticia.html', noticia=noticia, comentarios=comentarios)


# 🔹 Cadastrar notícia (via formulário)
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


# 🔹 Editar notícia
@app.route("/editar-noticia/<int:id>", methods=["GET", "POST"])
def editar_noticia(id):
    noticia = noticia_dao.buscarPorId(id)

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        categoria = request.form["categoria"]

        imagem = request.files.get("imagem")
        nome_arquivo = noticia["img"] 

        if imagem and imagem.filename != "":
            from werkzeug.utils import secure_filename
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join("static", "imgs", nome_arquivo)
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            imagem.save(caminho)

        noticia_dao.atualizarNoticia(titulo, descricao, categoria, nome_arquivo, id)
        return redirect("/listar-noticias")

    return render_template("editar-noticia.html", noticia=noticia)


# 🔹 Deletar notícia
@app.route("/deletar-noticia/<int:id>", methods=["POST"])
def deletar_noticia(id):
    noticia_dao.deletarNoticia(id)
    return redirect("/listar-noticias")


# 🔹 Buscar notícia por título
@app.route("/buscar-noticia", methods=["GET"])
def buscar_noticia():
    termo = request.args.get("titulo", "")

    if termo:
        resultados = noticia_dao.buscarPorTitulo(termo)
    else:
        resultados = noticia_dao.listar_todas()

    return render_template("noticias.html", noticias=resultados, termo=termo)


# 🔹 Deletar comentário (caso queira gerenciar depois)
@app.route("/deletar-comentario/<int:id>", methods=["POST"])
def deletar_comentario(id):
    comentario_dao.deletarComentario(id)
    return redirect(request.referrer or "/")


if __name__ == '__main__':
    app.run(debug=True)
