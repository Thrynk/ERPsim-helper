CREATE TABLE IF NOT EXISTS market (
    id_market BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    company_code CHAR(2) NOT NULL,
    sales_organization VARCHAR(2) NOT NULL,
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
    PRIMARY KEY(id_market)
)