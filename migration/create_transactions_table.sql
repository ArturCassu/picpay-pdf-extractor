USE financial_insights;
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    data VARCHAR(255),
    hora VARCHAR(255),
    descricao TEXT,
    valor DECIMAL(10, 2),
    saldo DECIMAL(10, 2),
    saldo_sacavel DECIMAL(10, 2),
    category VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user(id)
);