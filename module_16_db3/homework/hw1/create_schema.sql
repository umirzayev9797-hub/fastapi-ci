-- Включаем проверку связей
PRAGMA foreign_keys = ON;

-- Таблица актеров
CREATE TABLE IF NOT EXISTS actors (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_last_name VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL
);

-- Таблица фильмов
CREATE TABLE IF NOT EXISTS movie (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
);

-- Таблица директоров (режиссеров)
CREATE TABLE IF NOT EXISTS director (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL,
    dir_last_name VARCHAR(50) NOT NULL
);

-- Таблица состава фильма (связующая)
CREATE TABLE IF NOT EXISTS movie_cast (
    act_id INTEGER NOT NULL,
    mov_id INTEGER NOT NULL,
    role VARCHAR(50) NOT NULL,
    FOREIGN KEY (act_id) REFERENCES actors (act_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE CASCADE
);

-- Таблица наград
CREATE TABLE IF NOT EXISTS oscar_awarded (
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER NOT NULL,
    FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE CASCADE
);

-- Таблица режиссуры (связующая)
CREATE TABLE IF NOT EXISTS movie_direction (
    dir_id INTEGER NOT NULL,
    mov_id INTEGER NOT NULL,
    FOREIGN KEY (dir_id) REFERENCES director (dir_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie (mov_id) ON DELETE CASCADE
);