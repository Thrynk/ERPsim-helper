USE erpsim_games_flux;
DROP TABLE market;
CREATE TABLE IF NOT EXISTS market (
    id_market BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    company_code CHAR(2) NOT NULL,
    sales_organization VARCHAR(20) NOT NULL,
    sim_round INT NOT NULL,
    sim_period INT NOT NULL,
    material_description TEXT NOT NULL,
    distribution_channel INT NOT NULL,
    area ENUM('North', 'West', 'South'),
    quantity INT NOT NULL,
    unit VARCHAR(2) NOT NULL,
    average_price FLOAT NOT NULL,
    net_value FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_market
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_market)
)