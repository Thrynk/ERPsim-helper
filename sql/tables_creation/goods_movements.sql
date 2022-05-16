USE erpsim_games_flux;
DROP TABLE goods_movements;
CREATE TABLE IF NOT EXISTS goods_movements (
    id_good_movements BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    plant VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    event_type TEXT NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    storage_location VARCHAR(3) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    material_code VARCHAR(3) NOT NULL,
    material_label VARCHAR(50) NOT NULL,
    unit VARCHAR(2) NOT NULL,
    quantity_abs FLOAT NOT NULL,
    quantity FLOAT NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_goods_movements
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_good_movements)
)