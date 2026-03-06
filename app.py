from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)

# ---------------- App Config ----------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---------------- Models ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    tictactoe_score = db.Column(db.Integer, default=0)
    sudoku_score = db.Column(db.Integer, default=0)
    memory_score = db.Column(db.Integer, default=0)


class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    score = db.Column(db.Integer)
    time_taken = db.Column(db.String(50))


# ---------------- Login Loader ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- Routes ----------------
@app.route('/')
def progress():
    return render_template('progress.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- Register ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for('register'))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username'],
            password=request.form['password']
        ).first()

        if user:
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))

        flash("Invalid username or password")

    return render_template('login.html')


# ---------------- Logout ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ---------------- User Dashboard ----------------
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


# ---------------- Admin Dashboard ----------------
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Access denied!")
        return redirect(url_for('dashboard'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


# ---------------- Games ----------------
@app.route('/game/tictactoe', methods=['GET', 'POST'])
@login_required
def tictactoe():
    if request.method == 'POST':
        current_user.tictactoe_score = int(request.form['score'])
        db.session.commit()
        flash("Tic Tac Toe score saved!")
        return redirect(url_for('dashboard'))

    return render_template('tictactoe.html')


@app.route('/game/sudoku', methods=['GET', 'POST'])
@login_required
def sudoku():
    if request.method == 'POST':
        current_user.sudoku_score = int(request.form['score'])
        db.session.commit()
        flash("Sudoku score saved!")
        return redirect(url_for('dashboard'))

    return render_template('sudoku.html')


@app.route('/game/memory', methods=['GET', 'POST'])
@login_required
def memory():
    if request.method == 'POST':
        score = int(request.form['score'])
        time_taken = request.form['time']

        entry = Leaderboard(
            username=current_user.username,
            score=score,
            time_taken=time_taken
        )
        db.session.add(entry)
        db.session.commit()

        flash("Memory game score saved!")

    leaderboard = Leaderboard.query.order_by(
        Leaderboard.score.desc()
    ).limit(10).all()

    return render_template('memory.html', leaderboard=leaderboard)

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- Main ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
