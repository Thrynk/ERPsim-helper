USE erpsim_games_flux;
DROP TABLE inventory;
CREATE TABLE IF NOT EXISTS inventory (
    id_inventory BIGINT NOT NULL AUTO_INCREMENT,
    inventory_opening_balance INT NOT NULL,
    row_number INT NOT NULL,
    plant CHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    #sim_date TEXT,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    storage_location VARCHAR(3) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    material_code VARCHAR(3) NOT NULL,
    #material_size TEXT NOT NULL,
    material_label TEXT NOT NULL,
    unit VARCHAR(2) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_inventory
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_inventory)
)