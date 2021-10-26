USE erpsim_games ;

CREATE TABLE IF NOT EXISTS pricing_conditions_test (
    id_pricing_conditions BIGINT   AUTO_INCREMENT,
    price FLOAT  ,
    sales_organization VARCHAR(2)  ,
    row_number INT  ,
    sim_round INT  ,
    sim_step INT  ,
    #sim_date TEXT,
    sim_calendar_date DATETIME  ,
    sim_period INT  ,
    sim_elapsed_steps INT  ,
    material_number VARCHAR(6)  ,
    material_description TEXT  ,
    distribution_channel INT  ,
    dc_name  TEXT  ,
    currency VARCHAR(3)  ,
    PRIMARY KEY(id_pricing_conditions)
)