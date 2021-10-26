CREATE TABLE IF NOT EXISTS independant_requirements (
    id_independant_requirements BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    plant VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    quantity FLOAT NOT NULL,
    unit VARCHAR(2) NOT NULL,
    PRIMARY KEY(id_independant_requirements)
)