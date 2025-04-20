CREATE TABLE planets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    distance FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    habitable BOOLEAN DEFAULT 0,
    description TEXT,
    image_url VARCHAR(255),
    discovery_date DATE
);

CREATE TABLE explorers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    speciality VARCHAR(100) NOT NULL,
    experience INTEGER DEFAULT 0,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    planet_id INTEGER NOT NULL,
    explorer_id INTEGER NOT NULL,
    departure_date DATE NOT NULL,
    duration INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    FOREIGN KEY (planet_id) REFERENCES planets(id),
    FOREIGN KEY (explorer_id) REFERENCES explorers(id)
);

-- Données fictives pour les planètes
INSERT INTO planets (name, type, distance, temperature, habitable, description, image_url, discovery_date)
VALUES
('Kepler-452b', 'habitable', 1400, 22.0, 1, 'Une planète similaire à la Terre.', 'uploads/kepler452b.jpg', '2145-05-21'),
('Zentar-9', 'gazeuse', 3000, -150, 0, 'Une géante gazeuse bleue avec des anneaux brillants.', 'uploads/zentar9.jpg', '2138-11-14'),
('Roxia Prime', 'rocheuse', 560, 45, 0, 'Une planète volcanique active.', 'uploads/roxiaprime.jpg', '2142-08-07'),
('Elara', 'habitable', 800, 18, 1, 'Une planète océanique habitable.', 'uploads/elara.jpg', '2149-03-12');
