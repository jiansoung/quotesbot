CREATE DATABASE IF NOT EXISTS quotesbot;
USE quotesbot;

CREATE TABLE IF NOT EXISTS authors (
    id          INTEGER PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    name_hash   CHAR(32) NOT NULL,
    image_path  VARCHAR(255) DEFAULT '',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (name_hash)
);

DELIMITER //
DROP TRIGGER IF EXISTS before_insert_authors //
CREATE TRIGGER before_insert_authors BEFORE INSERT ON authors
FOR EACH ROW
BEGIN
    SET NEW.name_hash = MD5(NEW.name);
END; //
DELIMITER ;

DELIMITER //
DROP TRIGGER IF EXISTS before_update_authors //
CREATE TRIGGER before_update_authors BEFORE UPDATE ON authors
FOR EACH ROW
BEGIN
    SET NEW.name_hash = MD5(NEW.name);
END; //
DELIMITER ;

CREATE TABLE IF NOT EXISTS tags (
    id          INTEGER PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(255) NOT NULL,
    name_hash   CHAR(32) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (name_hash)
);

DELIMITER //
DROP TRIGGER IF EXISTS before_insert_tags //
CREATE TRIGGER before_insert_tags BEFORE INSERT ON tags
FOR EACH ROW
BEGIN
    SET NEW.name_hash = MD5(NEW.name);
END; //
DELIMITER ;

DELIMITER //
DROP TRIGGER IF EXISTS before_update_tags //
CREATE TRIGGER before_update_tags BEFORE UPDATE ON tags
FOR EACH ROW
BEGIN
    SET NEW.name_hash = MD5(NEW.name);
END; //
DELIMITER ;

CREATE TABLE IF NOT EXISTS quotes (
    id          INTEGER PRIMARY KEY AUTO_INCREMENT,
    `text`      TEXT NOT NULL,
    text_hash   CHAR(32) NOT NULL,
    author_id   INTEGER,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    UNIQUE (author_id, text_hash)
);

DELIMITER //
DROP TRIGGER IF EXISTS before_insert_quotes //
CREATE TRIGGER before_insert_quotes BEFORE INSERT ON quotes
FOR EACH ROW
BEGIN
    SET NEW.text_hash = MD5(NEW.text);
END; //
DELIMITER ;

DELIMITER $$
DROP TRIGGER IF EXISTS before_update_quotes $$
CREATE TRIGGER before_update_quotes BEFORE UPDATE ON quotes
FOR EACH ROW
BEGIN
    set NEW.text_hash = MD5(NEW.text);
END; $$
DELIMITER ;


CREATE TABLE IF NOT EXISTS quote_tag_assoc (
    id          INTEGER PRIMARY KEY AUTO_INCREMENT,
    quote_id    INTEGER NOT NULL,
    tag_id      INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (quote_id) REFERENCES quotes(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    UNIQUE (quote_id, tag_id)
);
