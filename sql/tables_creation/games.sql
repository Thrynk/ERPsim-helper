CREATE TABLE IF NOT EXISTS games (
    id_games BIGINT NOT NULL AUTO_INCREMENT,
    odata_flow TEXT NOT NULL,
    game_set INT NOT NULL,
    team VARCHAR(26) NOT NULL,
    creation_datetime DATETIME NOT NULL,
    PRIMARY KEY(id_games)
)