from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]
    complaint = request.form["complaint"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO complaints (student_name, email, complaint, status) VALUES (?, ?, ?, ?)",
        (name, email, complaint, "Pending")
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/admin")
def admin():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM complaints")
    data = cur.fetchall()
    conn.close()
    return render_template("admin.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
