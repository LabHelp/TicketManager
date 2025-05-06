from flask import Flask, render_template, request, redirect, send_file
import mysql.connector
import csv
import io
from config import MYSQL_CONFIG  # ✅ Import della configurazione DB

app = Flask(__name__)

# Connessione al database usando config.py
conn = mysql.connector.connect(
    host=MYSQL_CONFIG['host'],
    user=MYSQL_CONFIG['user'],
    password=MYSQL_CONFIG['password'],
    database=MYSQL_CONFIG['database']
)
#------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')
#------------------------------------------------------------------------------
@app.route('/submit', methods=['POST'])
def submit():
    data_richiesta = request.form['data_richiesta']
    numero_ticket = request.form['numero_ticket']
    data_esecuzione = request.form['data_esecuzione']
    ore = request.form['ore']
    minuti = request.form['minuti']
    email_tecnico = request.form['email_tecnico']
    email_cliente = request.form['email_cliente']

    cursor = conn.cursor()
    sql = """
        INSERT INTO ticket (
            data_richiesta, numero_ticket, data_esecuzione,
            ore, minuti, email_tecnico, email_cliente
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (data_richiesta, numero_ticket, data_esecuzione, ore, minuti, email_tecnico, email_cliente))
    conn.commit()
    cursor.close()
    return redirect('/')
#------------------------------------------------------------------------------
@app.route('/visualizza')
def visualizza():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket")
    tickets = cursor.fetchall()
    cursor.close()  #a cosa serve ?
    return render_template('visualizza.html', dati=tickets)
#------------------------------------------------------------------------------
@app.route('/edit/<int:id>')
def edit(id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM ticket WHERE id = %s", (id,))
        ticket = cursor.fetchone()
    return render_template('modals.html', dati=ticket)
#------------------------------------------------------------------------------
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    data_richiesta = request.form['data_richiesta']
    numero_ticket = request.form['numero_ticket']
    data_esecuzione = request.form['data_esecuzione']
    ore = request.form['ore']
    minuti = request.form['minuti']
    email_tecnico = request.form['email_tecnico']
    email_cliente = request.form['email_cliente']

    with conn.cursor() as cursor:
        sql = """
            UPDATE ticket
            SET data_richiesta = %s,
                numero_ticket = %s,
                data_esecuzione = %s,
                ore = %s,
                minuti = %s,
                email_tecnico = %s,
                email_cliente = %s
            WHERE id = %s
        """
        cursor.execute(sql, (data_richiesta, numero_ticket, data_esecuzione,
                             ore, minuti, email_tecnico, email_cliente, id))
        conn.commit()
    return redirect('/visualizza')
#------------------------------------------------------------------------------
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM ticket WHERE id = %s", (id,))
        conn.commit()

        cursor.execute("SELECT * FROM ticket")
        tickets = cursor.fetchall()
    return redirect('/visualizza')
    #return render_template('visualizza.html', dati=tickets)
#------------------------------------------------------------------------------
@app.route('/export_csv')
def export_csv():
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket")
    tickets = cursor.fetchall()
    cursor.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Data Richiesta', 'Numero Ticket', 'Data Esecuzione', 'Ore', 'Minuti', 'Email Tecnico', 'Email Cliente'])
    for ticket in tickets:
        writer.writerow([
            ticket['id'], ticket['data_richiesta'], ticket['numero_ticket'],
            ticket['data_esecuzione'], ticket['ore'], ticket['minuti'],
            ticket['email_tecnico'], ticket['email_cliente']
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='tickets.csv'
    )
#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
