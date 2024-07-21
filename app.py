from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/gym_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '3df01a7ae67ffd31218f264b3e04f8cd61b26194567c5f57836a6dd9bcf56857'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tel = db.Column(db.String(20), nullable=False)
    motdepasse = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    abonnement = db.Column(db.String(20), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_reception = db.Column(db.DateTime, default = datetime.utcnow)


nav = [
    {"title": "Accueil", "href": "home"},
    {"title": "Services", "href": "services"},
    {"title": "Horaires", "href": "horaires"},
    {"title": "Tarifs", "href": "tarifs"},
    {"title": "Galerie", "href": "galerie"},
    {"title": "Contact", "href": "contact"}
]

services_list = [
    {
        "title": "Entraînement Personnel",
        "image": "img-1.jpg",
        "description": "Bénéficiez d'un programme d'entraînement personnalisé avec l'un de nos coachs professionnels. Que vous souhaitiez perdre du poids, gagner en muscle ou améliorer votre forme générale, nous avons les solutions adaptées pour vous aider à atteindre vos objectifs."
    },
    {
        "title": "Cours Collectifs",
        "image": "img-2.jpg",
        "description": "Participez à nos cours collectifs pour rester motivé et faire de l'exercice en groupe. Du yoga au spinning en passant par la Zumba, nos cours sont adaptés à tous les niveaux et sont animés par des instructeurs certifiés."
    },
    {
        "title": "Nutrition et Conseil diététique",
        "image": "img-3.jpg",
        "description": "Recevez des conseils nutritionnels personnalisés de nos experts en diététique pour optimiser vos résultats d'entraînement. Nous vous aidons à adopter une alimentation saine et équilibrée pour améliorer votre bien-être général."
    },
    {
        "title": "Boxe",
        "image": "img-4.jpg",
        "description": "Entraînez-vous à la boxe avec nos coachs professionnels et améliorez votre condition physique, votre endurance et vos compétences en combat."
    },
    {
        "title": "Calisthénics",
        "image": "img-5.jpg",
        "description": "Découvrez l'art du calisthénics et utilisez le poids de votre corps pour développer votre force, votre flexibilité et votre coordination."
    },
    {
        "title": "Musculation",
        "image": "img-6.jpg",
        "description": "Profitez de notre salle de musculation équipée de matériel de pointe pour augmenter votre masse musculaire et améliorer votre condition physique globale."
    }
]

images = [
    {"filename": "g-1.jpg", "title": "01-01-2022"},
    {"filename": "g-2.jpg", "title": "15-02-2022"},
    {"filename": "g-3.jpg", "title": "30-03-2022"},
    {"filename": "g-4.jpg", "title": "10-04-2022"},
    {"filename": "g-5.jpg", "title": "25-05-2022"},
    {"filename": "g-6.jpg", "title": "12-06-2022"},
    {"filename": "g-7.jpg", "title": "08-07-2022"},
    {"filename": "g-8.jpg", "title": "21-08-2022"},
    {"filename": "g-9.jpg", "title": "09-09-2022"},
    {"filename": "g-10.jpg", "title": "18-10-2022"},
    {"filename": "g-11.jpg", "title": "05-11-2022"},
    {"filename": "g-12.jpg", "title": "20-12-2022"},
    {"filename": "g-13.jpg", "title": "03-01-2023"},
    {"filename": "g-14.jpg", "title": "14-02-2023"},
    {"filename": "g-15.jpg", "title": "29-03-2023"},
    {"filename": "g-16.jpg", "title": "10-04-2023"},
    {"filename": "g-17.jpg", "title": "25-05-2023"},
    {"filename": "g-18.jpg", "title": "12-06-2023"},
    {"filename": "g-19.jpg", "title": "08-07-2023"},
    {"filename": "g-20.jpg", "title": "21-08-2023"},
    {"filename": "g-21.jpg", "title": "09-09-2023"},
]

footer = {
    "social_media": [
        {"name": "Facebook", "url": "https://www.facebook.com", "icon": "facebook-icon.png"},
        {"name": "Twitter", "url": "https://www.twitter.com", "icon": "twitter-icon.png"},
        {"name": "Instagram", "url": "https://www.instagram.com", "icon": "instagram-icon.png"}
    ],
    "site_links": [
        {"title": "Accueil", "href": "home"},
        {"title": "Services", "href": "services"},
        {"title": "Horaires", "href": "horaires"},
        {"title": "Tarifs", "href": "tarifs"},
        {"title": "Galerie", "href": "galerie"},
        {"title": "Contact", "href": "contact"}
    ],
    "contact": [
        {"name": "E-mail", "url": "mailto:example@gmail.com"},
        {"name": "Phone", "url": "tel:+216 50 572 304"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com"},
        {"name": "GitHub", "url": "https://www.github.com"}
    ]
}

@app.route('/')
@app.route('/home')
@app.route('/accueil')
def home():
    return render_template('home.html', title='Accueil', nav=nav, footer=footer)

@app.route('/services')
def services():
    return render_template('services.html', title='Services', nav=nav, footer=footer, services=services_list)

@app.route('/horaires')
def horaires():
    return render_template('horaires.html', title='Horaires', nav=nav, footer=footer)

@app.route('/tarifs')
def tarifs():
    users = User.query.all()
    return render_template('tarifs.html', title='Tarifs', nav=nav, footer=footer, users = users)

@app.route('/souscrire/<abonnement>', methods=['GET', 'POST'])
def souscrire(abonnement):
    if 'user_name' not in session:
        flash('Vous devez être connecté pour souscrire.', 'danger')
        return redirect(url_for('login'))

    user_name = session.get('user_name')
    user = User.query.filter_by(nom=user_name).first()

    if user is None:
        flash('Utilisateur non trouvé.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        password = request.form.get('password')

        if check_password_hash(user.motdepasse, password):
            user.abonnement = abonnement
            db.session.commit()
            
            flash('Souscription réussie!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Mot de passe incorrect.', 'danger')

    return render_template('souscrire.html', title='Souscrire', nav=nav, footer=footer, abonnement=abonnement)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        message = request.form['message']
        
        new_message = Message(nom=nom, email=email, message=message)
        
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Votre message a été envoyé avec succès!', 'success')
        except Exception as e:
            flash(f'Erreur lors de l\'envoi du message: {str(e)}', 'danger')
    
    return render_template('contact.html', title='Contact', nav=nav, footer=footer)

@app.route('/galerie')
def galerie():
    return render_template('galerie.html', title='Galerie', nav=nav, footer=footer, images=images)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        tel = request.form['tel']
        motdepasse = request.form['motdepasse']
        confmotdepasse = request.form['confmotdepasse']
        role = request.form.get('role', 'user')

        if motdepasse != confmotdepasse:
            flash('Les mots de passe ne correspondent pas. Veuillez réessayer.', 'danger')
            return render_template('inscription.html', title='Inscription', nav=nav, footer=footer)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Cet email est déjà utilisé. Veuillez utiliser un autre email.', 'danger')
            return render_template('inscription.html', title='Inscription', nav=nav, footer=footer)

        motdepasse_hash = generate_password_hash(motdepasse, method='pbkdf2:sha256', salt_length=16)

        new_user = User(nom=nom, prenom=prenom, email=email, tel=tel, motdepasse=motdepasse_hash, role=role)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie! Veuillez vous connecter.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erreur lors de l\'inscription: {str(e)}', 'danger')
            db.session.rollback()
    return render_template('inscription.html', title='Inscription', nav=nav, footer=footer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        motdepasse = request.form['motdepasse']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.motdepasse, motdepasse):
            session['user_name'] = user.nom
            session['user_role'] = user.role
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard') if user.role == 'admin' else url_for('home'))
        else:
            flash('Identifiants incorrects. Veuillez réessayer.', 'danger')
    return render_template('login.html', title='Connexion', nav=nav, footer=footer)

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_role', None)
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('home'))

@app.route('/profil')
def profil():
    if 'user_name' in session:
        user = User.query.filter_by(nom=session['user_name']).first()
        return render_template('profil.html', title='Profil', nav=nav, footer=footer, user=user)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_name' not in session or session.get('user_role') != 'admin':
        flash('Accès interdit. Vous devez être un administrateur pour accéder à cette page.', 'danger')
        return redirect(url_for('home'))

    users = User.query.all()
    messages = Message.query.all()
    return render_template('dashboard.html', users=users, messages=messages)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.nom = request.form.get('nom')
        user.prenom = request.form.get('prenom')
        user.email = request.form.get('email')
        user.tel = request.form.get('tel')
        user.role = request.form.get('role')
        user.abonnement = request.form.get('abonnement')
        
        db.session.commit()
        flash('Utilisateur mis à jour avec succès!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/edit_profil', methods=['GET', 'POST'])
def edit_profil():
    if 'user_name' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))

    user_name = session.get('user_name')
    user = User.query.filter_by(nom=user_name).first()

    if request.method == 'POST':
        user.nom = request.form.get('nom')
        user.prenom = request.form.get('prenom')
        user.email = request.form.get('email')
        user.tel = request.form.get('tel')
        user.motdepasse = generate_password_hash(request.form.get('motdepasse'), method='pbkdf2:sha256', salt_length=16) if request.form.get('motdepasse') else user.motdepasse
        
        try:
            db.session.commit()
            flash('Profil mis à jour avec succès!', 'success')
            return redirect(url_for('profil'))
        except Exception as e:
            flash(f'Erreur lors de la mise à jour du profil: {str(e)}', 'danger')
            db.session.rollback()

    return render_template('edit_profil.html', title='Modifier Profil', nav=nav, footer=footer, user=user)

if __name__ == '__main__':
    app.run(debug=True)