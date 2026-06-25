from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB CREATE
def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

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

# HOME PAGE
@app.route('/')
def home():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", students=students)

# ADD STUDENT
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']
    student_class = request.form['student_class']
    email = request.form['email']
    phone = request.form['phone']

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students(name, roll, student_class, email, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (name, roll, student_class, email, phone))

    conn.commit()
    conn.close()

    return redirect('/')

# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

# SEARCH STUDENT
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + query + '%',))
    students = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", students=students)

# EDIT STUDENT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect("students.db")
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


if __name__ == '__main__':
    app.run(debug=True)