import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for

DATABASE = 'db/animaux.sql'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = sqlite3.connect('db/animaux.db')
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Fonction pour récupérer les animaux depuis la base de données SQLite
def get_animaux_from_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animaux")
    animaux = cursor.fetchall()
    return animaux

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animaux ORDER BY RANDOM() LIMIT 5")
    animaux = cursor.fetchall()
    conn.close()

    return render_template('index.html', animaux=animaux)


@app.route('/submit')
def submit():
    return render_template('form.html')


@app.route('/adoption', methods=['GET', 'POST'])
def mise_en_adoption():
    if request.method == 'POST':
        nom = request.form['nom']
        espece = request.form['espece']
        race = request.form['race']
        age = int(request.form['age'])
        description = request.form['description']
        courriel = request.form['courriel']
        adresse = request.form['adresse']
        ville = request.form['ville']
        cp = request.form['cp']

        errors = []

        if not nom:
            errors.append("Le nom de l'animal est obligatoire.")
        if not espece:
            errors.append("L'espèce de l'animal est obligatoire.")
        if not race:
            errors.append("La race de l'animal est obligatoire.")
        if age < 0 or age > 30:
            errors.append("L'âge de l'animal doit être compris entre 0 et 30.")
        if not description:
            errors.append("La description de l'animal est obligatoire.")
        if not courriel:
            errors.append("L'adresse courriel du propriétaire est obligatoire.")

        if errors:
            return render_template('submit.html', errors=errors)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM animaux")
        animaux = cursor.fetchall()


        cursor.execute("INSERT INTO animaux (nom, espece, race, age, description, courriel, adresse, ville, cp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (nom, espece, race, age, description, courriel, adresse, ville, cp))
        conn.commit()
        conn.close()

        nouvel_animal = {"id": len(animaux) + 1, "nom": nom, "espece": espece, "race": race, "age": age, "description": description, "courriel": courriel, "adresse": adresse, "ville": ville, "cp": cp}
        animaux.append(nouvel_animal)

        return redirect(url_for('animal', animal_id=nouvel_animal['id']))

    return render_template('submit.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/animals')
def animals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animaux ORDER BY ID DESC")
    animaux = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM animaux")
    total_animaux = cursor.fetchone()[0]
    conn.close()

    return render_template('animals.html', animaux=animaux, total_animaux=total_animaux)


@app.route('/animal/<int:animal_id>')
def animal(animal_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animaux WHERE id = ?", (animal_id,))
    animal = cursor.fetchone()

    cursor.execute("SELECT * FROM animaux ORDER BY RANDOM() LIMIT 5")
    animaux = cursor.fetchall()
    conn.close()

    if animal:
        return render_template('animal.html', animal=animal, animaux=animaux)
    return "Animal non trouvé."


@app.route('/recherche', methods=['GET', 'POST'])
def recherche():
    animaux = []
    total_animaux = 0

    if request.method == 'POST':
        keyword = request.form['keyword']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM animaux ORDER BY ID DESC")
        animaux = cursor.fetchall()

        resultats = [animal for animal in animaux if keyword.lower() in animal[1].lower() or
                     keyword.lower() in animal[2].lower() or keyword.lower() in animal[3].lower()]

        total_animaux = len(resultats)

        conn.close()

        return render_template('results.html', animaux=resultats, keyword=keyword, total_animaux=total_animaux)

    return render_template('animals.html', animaux=animaux, total_animaux=total_animaux)




if __name__ == "__main__":
    app.run(debug=True)
