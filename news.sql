--
-- ��SQLiteStudio v3.1.1 �������ļ� ���� 4�� 8 18:10:02 2018
--
-- �ı����룺System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- ��news
DROP TABLE IF EXISTS news;

CREATE TABLE news (
    news_class   INT,
    news_addr    VARCHAR (200),
    news_title   VARCHAR (100),
    news_content TEXT
);


-- ��news_class
DROP TABLE IF EXISTS news_class;

CREATE TABLE news_class (
    id         INT,
    class_name VARCHAR (100),
    class_addr VARCHAR (200) 
);


-- ��news_idx
DROP TABLE IF EXISTS news_idx;

CREATE TABLE news_idx (
    word NVARCHAR (20),
    idx  TEXT
);


-- ��news_idx_max
DROP TABLE IF EXISTS news_idx_max;

CREATE TABLE news_idx_max (
    rowid_max  INT,
    createtime DATETIME,
    tm         DECIMAL (18, 4) 
);


-- ��news_idx_tmp
DROP TABLE IF EXISTS news_idx_tmp;

CREATE TABLE news_idx_tmp (
    word VARCHAR (20),
    idx  TEXT
);


-- ��words_idf
DROP TABLE IF EXISTS words_idf;

CREATE TABLE words_idf (
    word VARCHAR (20),
    idf  REAL
);


-- ��words_tf
DROP TABLE IF EXISTS words_tf;

CREATE TABLE words_tf (
    word   VARCHAR (20),
    newsid INT,
    tf     REAL
);


-- ������1
DROP INDEX IF EXISTS [1];

CREATE UNIQUE INDEX [1] ON news_idx_tmp (
    word
);


-- ������idx_1
DROP INDEX IF EXISTS idx_1;

CREATE UNIQUE INDEX idx_1 ON news_idx (
    word
);


-- ������u_q
DROP INDEX IF EXISTS u_q;

CREATE UNIQUE INDEX u_q ON words_idf (
    word
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
