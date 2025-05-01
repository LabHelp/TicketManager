from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configurazione DB
conn = mysql.connector.connect(
    host="localhost",
    user="tuo_utente",
    password="tua_password",
    database="tuo_database"
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    form = request.form
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ticket_entries (data_richiesta, numero_ticket, data_esecuzione, ore, minuti, email_tecnico, email_cliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (form['data_richiesta'], form['numero_ticket'], form['data_esecuzione'], form['ore'], form['minuti'], form['email_tecnico'], form['email_cliente']))
    conn.commit()
    cursor.close()
    return "<div class='alert alert-success'>Salvato correttamente!</div>"

@app.route("/visualizza")
def visualizza():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket_entries ORDER BY id DESC")
    dati = cursor.fetchall()
    cursor.close()
    return render_template("visualizza.html", dati=dati)

@app.route("/edit/<int:id>")
def edit(id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket_entries WHERE id=%s", (id,))
    record = cursor.fetchone()
    cursor.close()
    return render_template("modals.html", record=record)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    form = request.form
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ticket_entries SET data_richiesta=%s, numero_ticket=%s, data_esecuzione=%s, ore=%s, minuti=%s, email_tecnico=%s, email_cliente=%s
        WHERE id=%s
    """, (form['data_richiesta'], form['numero_ticket'], form['data_esecuzione'], form['ore'], form['minuti'], form['email_tecnico'], form['email_cliente'], id))
    conn.commit()
    cursor.close()
    return "<div class='alert alert-success'>Modifica completata!</div>"

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ticket_entries WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    return "<div class='alert alert-danger'>Record eliminato!</div>"

@app.route("/export/csv")
def export_csv():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket_entries ORDER BY id DESC")
    records = cursor.fetchall()
    cursor.close()

    si = []
    headers = ["ID", "Data Richiesta", "Numero Ticket", "Data Esecuzione", "Ore", "Minuti", "Email Tecnico", "Email Cliente"]
    si.append(",".join(headers))

    for row in records:
        si.append(",".join(str(row[col]) for col in ['id', 'data_richiesta', 'numero_ticket', 'data_esecuzione', 'ore', 'minuti', 'email_tecnico', 'email_cliente']))

    csv_content = "\n".join(si)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    return (
        csv_content,
        200,
        {
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename=ticket_export_{now}.csv"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)