import sqlite3
import pymysql
from pymysql.cursors import DictCursor
from datetime import date

class Noticia:
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
            cursorclass=DictCursor,
        )

    def criarNoticia(self, titulo, descricao, categoria, img):
        dataN = date.today()  
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO noticia (titulo, descricao, categoria, img, dataN)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (titulo, descricao, categoria, img, dataN))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao criar notícia:", e)
            return False
        finally:
            conn.close()

    def buscarPorTitulo(self, titulo):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM noticia WHERE titulo LIKE %s", (f"%{titulo}%",))
                return cursor.fetchall()
        finally:
            conn.close()

    def buscarPorCategoria(self, categoria):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM noticia WHERE categoria LIKE %s", (f"%{categoria}%",))
                return cursor.fetchall()
        finally:
            conn.close()

    def atualizarNoticia(self, titulo, descricao, categoria, img, id):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE noticia
                    SET titulo=%s, descricao=%s, categoria=%s, img=%s
                    WHERE id=%s
                """
                cursor.execute(sql, (titulo, descricao, categoria, img, id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def deletarNoticia(self, id):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM noticia WHERE id=%s", (id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def listar_todas(self):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM noticia ORDER BY id DESC")
                resultado = cursor.fetchall()
                print("DEBUG: resultado do banco:", resultado)
                return resultado
        finally:
            conn.close()


    def buscarPorId(self, id):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM noticia WHERE id = %s", (id,))
                return cursor.fetchone()
        finally:
            conn.close()


    def incrementar_views(self, id):
        conn = self.conectar()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE noticia SET views = views + 1 WHERE id = %s", (id,))
            conn.commit()
        finally:
            conn.close()
