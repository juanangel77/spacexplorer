# app/routes.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime

from spaceapp import app


app.config['UPLOAD_FOLDER'] = 'app/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def get_db_connection():
    conn = sqlite3.connect('spacexplorer.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    conn = get_db_connection()
    explorers = conn.execute('SELECT * FROM explorers').fetchall()
    missions = conn.execute('SELECT missions.*, planets.name AS planet_name, explorers.name AS explorer_name FROM missions JOIN planets ON missions.planet_id = planets.id JOIN explorers ON missions.explorer_id = explorers.id').fetchall()
    conn.close()
    return render_template('index.html', explorers=explorers, missions=missions)

@app.route('/catalog')
def catalog():
    conn = get_db_connection()
    query = "SELECT * FROM planets"
    filters = []
    values = []

    type_filter = request.args.get('type')
    if type_filter:
        if type_filter == 'habitable':
            filters.append("habitable = 1")
        else:
            filters.append("type = ?")
            values.append(type_filter)

    sort = request.args.get('sort')
    if filters:
        query += " WHERE " + " AND ".join(filters)
    if sort in ['distance', 'temperature', 'size']:
        query += f" ORDER BY {sort}"

    planets = conn.execute(query, values).fetchall()
    conn.close()
    return render_template('catalog.html', planets=planets)

@app.route('/planet/<int:planet_id>')
def planet_detail(planet_id):
    conn = get_db_connection()
    planet = conn.execute("SELECT * FROM planets WHERE id = ?", (planet_id,)).fetchone()
    conn.close()
    if planet is None:
        return "Planète non trouvée", 404
    return render_template('planet_detail.html', planet=planet)

@app.route('/add', methods=['GET', 'POST'])
def add_planet():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        distance = request.form['distance']
        temperature = request.form['temperature']
        habitable = 1 if 'habitable' in request.form else 0
        description = request.form['description']
        discovery_date = request.form['discovery_date']
        file = request.files['planetImage']
        image_url = ''

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = file_path

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO planets (name, type, distance, temperature, habitable, description, image_url, discovery_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, type_, distance, temperature, habitable, description, image_url, discovery_date))
        conn.commit()
        conn.close()
        return redirect(url_for('catalog'))

    return render_template('form.html')

@app.route('/explorers/add', methods=['GET', 'POST'])
def add_explorer():
    if request.method == 'POST':
        name = request.form['name']
        speciality = request.form['speciality']
        experience = request.form['experience']
        email = request.form['email']

        conn = get_db_connection()
        conn.execute('INSERT INTO explorers (name, speciality, experience, email) VALUES (?, ?, ?, ?)',
                     (name, speciality, experience, email))
        conn.commit()
        conn.close()
        return redirect(url_for('list_explorers'))

    return render_template('add_explorer.html')

@app.route('/explorers')
def list_explorers():
    conn = get_db_connection()
    explorers = conn.execute('SELECT * FROM explorers').fetchall()
    conn.close()
    return render_template('list_explorers.html', explorers=explorers)

@app.route('/missions/reserve', methods=['GET', 'POST'])
def reserve_mission():
    conn = get_db_connection()
    planets = conn.execute('SELECT id, name FROM planets').fetchall()
    explorers = conn.execute('SELECT id, name FROM explorers').fetchall()

    if request.method == 'POST':
        planet_id = request.form['planet_id']
        explorer_id = request.form['explorer_id']
        departure_date = request.form['departure_date']
        duration = request.form['duration']

        conn.execute('INSERT INTO missions (planet_id, explorer_id, departure_date, duration) VALUES (?, ?, ?, ?)',
                     (planet_id, explorer_id, departure_date, duration))
        conn.commit()
        conn.close()
        return "Mission réservée avec succès !"

    conn.close()
    return render_template('reserve_mission.html', planets=planets, explorers=explorers)
