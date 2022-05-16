USE erpsim_games_flux;
DROP TABLE financial_postings;
CREATE TABLE IF NOT EXISTS financial_postings (
    id_financial_postings BIGINT NOT NULL AUTO_INCREMENT,
    row_number INT NOT NULL,
    company_code VARCHAR(2) NOT NULL,
    sim_round INT NOT NULL,
    sim_step INT NOT NULL,
    sim_calendar_date DATETIME NOT NULL,
    sim_period INT NOT NULL,
    sim_elapsed_steps INT NOT NULL,
    gl_account_number TEXT NOT NULL,
    gl_account_name TEXT NOT NULL,
    fs_level_1 TEXT,
    fs_level_2 TEXT,
    fs_level_3 TEXT,
    fs_level_4 TEXT,
    debit_credit_indicator VARCHAR(10) NOT NULL,
    amount_abs FLOAT NOT NULL,
    amount FLOAT NOT NULL,
    amount_inv FLOAT NOT NULL,
    amount_bs FLOAT NOT NULL,
    amount_is FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL,
    id_game BIGINT NOT NULL,
    CONSTRAINT fk_game_financial_postings
    FOREIGN KEY (id_game)
    REFERENCES erpsim_helper_game(id)
    ON DELETE CASCADE,
    PRIMARY KEY(id_financial_postings)
)