from flask import Flask, render_template, request, redirect, session
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "student_management_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")


# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        student_class TEXT,
        email TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )
            conn.commit()

        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect('/login')

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/')

        return "Invalid Credentials"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ---------------- DASHBOARD ----------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", students=students)


# ---------------- ADD STUDENT ----------------
@app.route('/add', methods=['POST'])
def add_student():
    if 'user' not in session:
        return redirect('/login')

    name = request.form['name']
    roll = request.form['roll']
    student_class = request.form['student_class']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students
        (name, roll, student_class, email, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (name, roll, student_class, email, phone))

    conn.commit()
    conn.close()

    return redirect('/')


# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete_student(id):
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')


# ---------------- SEARCH ----------------
@app.route('/search')
def search():
    if 'user' not in session:
        return redirect('/login')

    query = request.args.get('query', '')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + query + '%',)
    )

    students = cur.fetchall()
    conn.close()

    return render_template("dashboard.html", students=students)


# ---------------- EDIT ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        student_class = request.form['student_class']
        email = request.form['email']
        phone = request.form['phone']

        cur.execute("""
        UPDATE students
        SET name=?, roll=?, student_class=?, email=?, phone=?
        WHERE id=?
        """, (name, roll, student_class, email, phone, id))

        conn.commit()
        conn.close()

        return redirect('/')

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()

    conn.close()

    return render_template("edit.html", student=student)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)