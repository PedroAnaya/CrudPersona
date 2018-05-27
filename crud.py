from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from raven.contrib.flask import Sentry
from datetime import datetime

app = Flask(__name__)

sentry = Sentry(app, dsn='https://34b4dd07263949959a499ac3a98ea9d2:bba044ffa89544af98017e588e66e975@sentry.io/1210257')

ADMINS = ['exceptionappweb@gmail.com']
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'exceptionappweb@gmail.com',
                               ADMINS, 'Error en la aplicaion')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pedro0319'
app.config['MYSQL_DB'] = 'Prueba'
mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Persona")
    rv = cur.fetchall()
    cur.close()
    return render_template('home.html', Persona=rv)

@app.route('/simpan',methods=["POST"])
def simpan():
    strNombre = request.form['strNombre']
    strApaterno = request.form['strApaterno']
    strAmaterno = request.form['strAmaterno']
    dtefechaNacimiento =request.form['dtefechaNacimiento']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Persona (strNombre,strApaterno,strAmaterno,dtefechaNacimiento) VALUES (%s,%s,%s,%s) ",(strNombre,strApaterno,strAmaterno,dtefechaNacimiento))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/update', methods=["POST"])
def update():
    id_data = request.form['id']
    strNombre = request.form['strNombre']
    strApaterno = request.form['strApaterno']
    strAmaterno = request.form['strAmaterno']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Persona SET strNombre=%s, strApaterno=%s, strAmaterno=%s WHERE id=%s", (strNombre,strApaterno,strAmaterno,id_data,))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/hapus/<string:id_data>', methods=["GET"])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Persona WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)