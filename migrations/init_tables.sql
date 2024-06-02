CREATE TABLE squad (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE family (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    squad_id INTEGER NOT NULL,

    FOREIGN KEY (squad_id) REFERENCES squad (id) ON DELETE CASCADE
);


CREATE TABLE insect
(
    id SERIAL PRIMARY KEY,
    lat_name VARCHAR(255) UNIQUE NOT NULL,
    ru_name VARCHAR(255) UNIQUE NOT NULL,
    img VARCHAR(256),

    family_id INTEGER NOT NULL,

    description TEXT, -- Описание
    category_and_status TEXT, -- Категория и статус
    distribution TEXT, -- Распространение
    area TEXT, -- Ареал
    habitat TEXT, -- Места обитания и особенности экологии
    limiting_factors TEXT, -- (Лимитирующие факторы
    count_ TEXT, -- Численность
    security_notes TEXT, -- Принятие мер по охране

    FOREIGN KEY (family_id) REFERENCES family (id) ON DELETE CASCADE
);

