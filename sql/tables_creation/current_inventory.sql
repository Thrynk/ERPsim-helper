USE erpsim_games_flux;
DROP TABLE current_inventory;
CREATE TABLE IF NOT EXISTS current_inventory (
    id_current_inventory BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    plant VARCHAR(2) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    storage_location VARCHAR(3) NOT NULL,
    stock INT NOT NULL,
    restricted INT NOT NULL,
    unit VARCHAR(2) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_current_inventory
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_current_inventory)
)