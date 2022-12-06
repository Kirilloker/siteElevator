DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timeCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tag TEXT NOT NULL,
    content TEXT NOT NULL
);