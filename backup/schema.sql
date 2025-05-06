CREATE TABLE IF NOT EXISTS tickets (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data_richiesta DATE,
  numero_ticket VARCHAR(20),
  data_esecuzione DATE,
  ore INT,
  minuti INT,
  email_tecnico VARCHAR(100),
  email_cliente VARCHAR(100),
  data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);