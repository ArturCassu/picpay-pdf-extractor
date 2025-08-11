USE financial_insights;
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nome VARCHAR(255),
    cpf VARCHAR(14),
    agencia VARCHAR(10),
    conta VARCHAR(20),
    cliente_desde DATE
);