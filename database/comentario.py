import pymysql
from pymysql.cursors import DictCursor

class Comentario:
    def __init__(self, host="localhost", user="root", password="password", database="db_noticias", port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def conectar(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            charset="utf8mb4",
            database=self.database,
            cursorclass=DictCursor
        )

    # 🔹 Criar comentário
    def criarComentario(self, autor, comentario, id_noticia):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO comentario (autor, comentario, id_noticia)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (autor, comentario, id_noticia))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao criar comentário:", e)
            return False
        finally:
            conn.close()

    # 🔹 Buscar todos os comentários de uma notícia específica
    def listarPorNoticia(self, id_noticia):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM comentario WHERE id_noticia = %s ORDER BY id DESC", (id_noticia,))
                return cursor.fetchall()
        finally:
            conn.close()

    # 🔹 Deletar um comentário
    def deletarComentario(self, id):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM comentario WHERE id = %s", (id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # 🔹 Buscar um comentário específico (caso precise editar no futuro)
    def buscarPorId(self, id):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM comentario WHERE id = %s", (id,))
                return cursor.fetchone()
        finally:
            conn.close()
