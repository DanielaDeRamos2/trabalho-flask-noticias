from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('listar-noticias.html')
    

if __name__ == '__main__':
    app.run(debug=True)