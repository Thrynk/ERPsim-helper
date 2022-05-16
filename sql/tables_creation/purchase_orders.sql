USE erpsim_games_flux;
DROP TABLE purchase_orders;
CREATE TABLE IF NOT EXISTS purchase_orders (
    id_purchase_orders BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    company_code VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    purchasing_order TEXT NOT NULL,
    vendor VARCHAR(3) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    unit VARCHAR(2) NOT NULL,
    goods_receipt_round INT NOT NULL,
    goods_receipt_step INT NOT NULL,
    goods_receipt_date VARCHAR(5) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_purchase_orders
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_purchase_orders)
)