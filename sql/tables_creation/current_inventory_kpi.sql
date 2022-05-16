USE erpsim_games_flux;
DROP TABLE current_inventory_kpi;
CREATE TABLE IF NOT EXISTS current_inventory_kpi (
    id_current_inventory_kpi BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    plant VARCHAR(2) NOT NULL,
    storage_location VARCHAR(3) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    material_code VARCHAR(3) NOT NULL, 
    material_label TEXT NOT NULL,
    current_inventory INT NOT NULL, 
    quantity_sold INT NOT NULL, 
    nb_steps_available INT NOT NULL, 
    sim_elapsed_steps INT NOT NULL,
    unit VARCHAR(2) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_current_inventory_kpi
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_current_inventory_kpi)
)