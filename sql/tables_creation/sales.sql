USE erpsim_games_flux;
DROP TABLE sales;
CREATE TABLE IF NOT EXISTS sales (
    id_sales BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    sales_organization VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    sales_order_number INT NOT NULL,
    line_item INT NOT NULL,
    storage_location VARCHAR(3) NOT NULL,
    region VARCHAR(50) NOT NULL,
    area ENUM('North', 'West', 'South'),
    city VARCHAR(50) NOT NULL,
    country VARCHAR(20) NOT NULL,
    postal_code INT NOT NULL,
    customer_number INT NOT NULL,
    distribution_channel INT NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    material_code VARCHAR(3) NOT NULL,
    material_label VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    quantity_delivered INT NOT NULL,
    unit VARCHAR(2) NOT NULL,
    net_price FLOAT NOT NULL,
    net_value FLOAT NOT NULL,
    cost FLOAT NOT NULL,
    currency VARCHAR(5) NOT NULL,
    contribution_margin FLOAT NOT NULL,
    contribution_margin_pct FLOAT NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_sales
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_sales)
);