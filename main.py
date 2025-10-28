from flask import Flask, render_template, redirect, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "gh9eph493vvh93-287"
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"User: {self.name}"
    
    
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for('login'))
    name = session.get("name")
    return render_template("index.html", name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        parol = request.form.get("parol")
        try:
            user = Users.query.filter_by(username=username, password=parol).first()
            if user:
                session['name'] = user.name
                session['user_id'] = user.id
                return redirect(url_for("index"))
        except:
            pass
        return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        ism = request.form.get("ism")
        username = request.form.get("username")
        parol = request.form.get("parol")
        try:
            user = Users(name=ism, username=username, password=parol)
            db.session.add(user)
            db.session.commit()
            session['name'] = user.name
            session['user_id'] = user.id
            return redirect(url_for("index"))
        except:
            print("xatolik")
        return redirect(url_for('register'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ← Shu yerda database.db yaratiladi
        print("✅ Database created successfully in instance folder.")
    app.run(debug=True)