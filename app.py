from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Users, Movie
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("admin_dashboard") if current_user.role == "admin" else url_for("dashboard"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin_dashboard") if user.role == "admin" else url_for("dashboard"))
        flash("Correo o contraseña inválidos")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        role = request.form.get("role")

        if password != confirm:
            flash("Las contraseñas no coinciden")
            return redirect(url_for("register"))

        if Users.query.filter_by(email=email).first():
            flash("Este correo ya está registrado")
            return redirect(url_for("register"))

        if role not in ["admin", "user"]:
            flash("Rol inválido.")
            return redirect(url_for("register"))

        user = Users(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("admin_dashboard") if role == "admin" else url_for("dashboard"))

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "user":
        flash("Acceso no autorizado.")
        return redirect(url_for("admin_dashboard"))
    movies = Movie.query.all()
    return render_template("dashboard.html", movies=movies)

@app.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Acceso denegado.")
        return redirect(url_for("dashboard"))
    movies = Movie.query.all()
    return render_template("admin_dashboard.html", movies=movies)

@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_movie():
    if current_user.role != "admin":
        flash("Acceso denegado.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        new_movie = Movie(
            title=request.form.get("title"),
            rating=request.form.get("rating"),
            year=request.form.get("year"),
            description=request.form.get("description"),
            image_url=request.form.get("image_url")
        )
        db.session.add(new_movie)
        db.session.commit()
        flash("Película agregada correctamente.")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_movie.html")

@app.route("/admin/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit_movie(movie_id):
    if current_user.role != "admin":
        flash("Acceso denegado.")
        return redirect(url_for("dashboard"))

    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        movie.title = request.form.get("title")
        movie.rating = request.form.get("rating")
        movie.year = request.form.get("year")
        movie.description = request.form.get("description")
        movie.image_url = request.form.get("image_url")

        db.session.commit()
        flash("Película actualizada correctamente.")
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_movie.html", movie=movie)

@app.route("/admin/delete/<int:movie_id>", methods=["POST"])
@login_required
def delete_movie(movie_id):
    if current_user.role != "admin":
        flash("Acceso denegado.")
        return redirect(url_for("dashboard"))

    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Película eliminada correctamente.")
    return redirect(url_for("admin_dashboard"))

@app.route("/view/<int:id>")
@login_required
def view_movie(id):
    movie = Movie.query.get_or_404(id)
    return render_template("view.html", movie=movie)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
