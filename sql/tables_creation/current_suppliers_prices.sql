CREATE TABLE IF NOT EXISTS current_suppliers_prices (
    id_current_suppliers_prices BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    purchasing_organization VARCHAR(2) NOT NULL,
    material_number VARCHAR(6) NOT NULL,
    material_description TEXT NOT NULL,
    vendor_code VARCHAR(3) NOT NULL,
    vendor_name TEXT NOT NULL,
    net_price FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    PRIMARY KEY(id_current_suppliers_prices)
)