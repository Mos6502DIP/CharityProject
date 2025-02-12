DROP TABLE IF EXISTS Places;

-- Create the Users table
CREATE TABLE IF NOT EXISTS Places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    thumbnail_image TEXT NOT NULL,
    banner_image TEXT NOT NULL,
    adult_price INT NOT NULL,
    child_price INT NOT NULL,
    facilities TEXT NOT NULL
);