USE erpsim_games_flux;
DROP TABLE nps_surveys;
CREATE TABLE IF NOT EXISTS nps_surveys (
    id_nps_surveys BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    plant VARCHAR(2) NOT NULL,
    type VARCHAR(30) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    material_code VARCHAR(3) NOT NULL,
    material_label VARCHAR(50) NOT NULL,
    customer_number INT NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    postal_code INT NOT NULL,
    region VARCHAR(50) NOT NULL,
    area ENUM('North', 'West', 'South'),
    distribution_channel INT NOT NULL,
    score_0 INT NOT NULL,
    score_1 INT NOT NULL,
    score_2 INT NOT NULL,
    score_3 INT NOT NULL,
    score_4 INT NOT NULL,
    score_5 INT NOT NULL,
    score_6 INT NOT NULL,
    score_7 INT NOT NULL,
    score_8 INT NOT NULL,
    score_9 INT NOT NULL,
    score_10 INT NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_nps_surveys
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_nps_surveys)
)