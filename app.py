from flask import Flask, render_template, request, redirect, send_file
import mysql.connector
import csv
import io
from config import MYSQL_CONFIG

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket")
    tickets = cursor.fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/submit', methods=['POST'])
def submit():
    id = request.form.get('id')
    data = (
        request.form['data_richiesta'],
        request.form['numero_ticket'],
        request.form['data_esecuzione'],
        request.form['ore'],
        request.form['minuti'],
        request.form['email_tecnico'],
        request.form['email_cliente']
    )
    conn = get_connection()
    cursor = conn.cursor()
    if id:  # Modifica
        cursor.execute("""
            UPDATE ticket SET data_richiesta=%s, numero_ticket=%s, data_esecuzione=%s,
            ore=%s, minuti=%s, email_tecnico=%s, email_cliente=%s WHERE id=%s
        """, data + (id,))
    else:  # Nuovo inserimento
        cursor.execute("""
            INSERT INTO ticket (data_richiesta, numero_ticket, data_esecuzione,
            ore, minuti, email_tecnico, email_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, data)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ticket WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete_all', methods=['POST'])
def delete_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ticket")
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/export_csv')
def export_csv():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket")
    tickets = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Data Richiesta', 'Numero Ticket', 'Data Esecuzione', 'Ore', 'Minuti', 'Email Tecnico', 'Email Cliente'])
    for t in tickets:
        writer.writerow([t['id'], t['data_richiesta'], t['numero_ticket'], t['data_esecuzione'], t['ore'], t['minuti'], t['email_tecnico'], t['email_cliente']])

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='tickets.csv')

if __name__ == '__main__':
    app.run(debug=True)