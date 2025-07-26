from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configurações do banco
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "flaskdb")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Senha123!")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def index():
    return "Flask App is running!"

@app.route("/health")
def health():
    return "Healthy"

@app.route("/db")
def db_check():
    try:
        conn = get_connection()
        conn.close()
        return "Database connected!"
    except Exception as e:
        return f"Database connection failed: {e}"

@app.route("/add")
def add_person():
    name = request.args.get("name")
    if not name:
        return "Missing name", 400
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS people (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
        cur.execute("INSERT INTO people (name) VALUES (%s)", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return f"Person '{name}' added!"
    except Exception as e:
        return f"Error: {e}"

@app.route("/list")
def list_people():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM people ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"people": [{"id": r[0], "name": r[1]} for r in rows]})
    except Exception as e:
        return f"Error: {e}"

@app.route("/update")
def update_person():
    person_id = request.args.get("id")
    new_name = request.args.get("name")
    if not person_id or not new_name:
        return "Missing id or name", 400
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE people SET name = %s WHERE id = %s", (new_name, person_id))
        conn.commit()
        cur.close()
        conn.close()
        return f"Person {person_id} updated to {new_name}"
    except Exception as e:
        return f"Error: {e}"

@app.route("/delete")
def delete_person():
    person_id = request.args.get("id")
    if not person_id:
        return "Missing id", 400
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM people WHERE id = %s", (person_id,))
        conn.commit()
        cur.close()
        conn.close()
        return f"Person {person_id} deleted"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
