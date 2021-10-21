CREATE TABLE IF NOT EXISTS pricing_conditions (
    id_pricing_conditions BIGINT NOT NULL AUTO_INCREMENT,
    price FLOAT NOT NULL,
    sales_organization VARCHAR(2) NOT NULL,
    row_number INT NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    #sim_date TEXT,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    distribution_channel INT NOT NULL,
    dc_name  TEXT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    PRIMARY KEY(id_inventory)
)