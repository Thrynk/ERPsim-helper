USE erpsim_games_flux ;
DROP TABLE company_valuation;
CREATE TABLE IF NOT EXISTS company_valuation (
    id_company_valuation BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    company_code CHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    bank_cash_account FLOAT NOT NULL,
    accounts_receivable INT NOT NULL,
    bank_loan FLOAT NOT NULL,
    accounts_payable FLOAT NOT NULL, 
    profit FLOAT NOT NULL, 
    debt_loading FLOAT NOT NULL,
    credit_rating VARCHAR(10) NOT NULL, 
    company_risk_rate_pct FLOAT NOT NULL,
    company_valuation FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_company_valuation
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_company_valuation)
)