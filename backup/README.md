
# Ticket Manager - Mini App con Flask + HTMX

Questa è una semplice applicazione web per la gestione di ticket tecnici, sviluppata con Flask, HTMX e Bootstrap. Permette l'inserimento, modifica, cancellazione, visualizzazione e esportazione CSV dei dati.

## 📆 Requisiti

- Python 3.8+
- MySQL o MariaDB

## 🔧 Installazione

1. **Clona il progetto** o scarica i file:

```bash
git clone https://tuo-repo-url.git
cd flask-htmx-app
```

2. **Installa i pacchetti Python**:

```bash
pip install -r requirements.txt
```

3. **Crea il database** in MySQL:

```sql
CREATE DATABASE nome_database;
```

4. **Importa lo schema**:

```bash
mysql -u utente -p nome_database < schema.sql
```

5. **Configura le credenziali MySQL** in `app.py`:

```python
app.config['MYSQL_DATABASE_USER'] = 'utente'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'nome_database'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
```

6. **Avvia l'applicazione**:

```bash
python app.py
```

Visita [http://localhost:5000](http://localhost:5000) per iniziare.

## 💻 Funzionalità

- ✅ Inserimento nuovi ticket
- ✅ Visualizzazione in tabella
- ✅ Modifica ed eliminazione (modale dinamica)
- ✅ Esportazione in CSV

## 🎨 Aspetto grafico

- Bootstrap 5
- Colori personalizzati via `style.css` (blu `#0000FF` e rosso `#FF0000`)

## 📁 Struttura

```
/flask-htmx-app/
│
├── app.py               # Applicazione Flask
├── requirements.txt     # Dipendenze Python
├── schema.sql           # Script MySQL per creazione tabella
├── README.md            # Guida all'installazione e utilizzo
│
├── /templates/          # File HTML con HTMX + Bootstrap
│   ├── base.html
│   ├── index.html
│   ├── visualizza.html  # Pagina di visualizzazione
│   └── modals.html
│
├── /static/
│   └── style.css        # Stile personalizzato
```

---

Creato con ❤️ usando Flask + HTMX
