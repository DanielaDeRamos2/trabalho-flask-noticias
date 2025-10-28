--Noticia

CREATE TABLE noticia(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50),
    views INT DEFAULT 0,
    img VARCHAR(255),
    dataN DATE
);

CREATE TABLE comentario(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    autor VARCHAR(100),
    comentario TEXT,
    id_noticia INT NOT NULL,
    FOREIGN KEY(id_noticia) REFERENCES noticia(id)
);

--ALTER TABLE noticia
--MODIFY views INT DEFAULT 0;

--ALTER TABLE noticia
--ADD dataN DATE;