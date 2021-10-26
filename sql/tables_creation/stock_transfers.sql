CREATE TABLE IF NOT EXISTS stock_transfers (
    id_stock_transfers BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    plant VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    storage_location VARCHAR(3) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    material_code VARCHAR(3) NOT NULL,
    material_label VARCHAR(50) NOT NULL,
    unit VARCHAR(2) NOT NULL,
    quantity INT NOT NULL,    
    PRIMARY KEY(id_stock_transfers)
)