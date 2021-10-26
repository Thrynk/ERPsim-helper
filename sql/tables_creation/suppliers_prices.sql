CREATE TABLE IF NOT EXISTS suppliers_prices (
    id_suppliers_prices BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    purchasing_organization VARCHAR(2) NOT NULL,
    plant VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    material_description TEXT NOT NULL,
    material_type TEXT NOT NULL,
    vendor_code VARCHAR(3) NOT NULL,
    vendor_name TEXT NOT NULL,
    net_price FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    PRIMARY KEY(id_suppliers_prices)
)