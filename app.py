from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_database():
    conn = sqlite3.connect("inventario.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def listar():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("index.html", productos=productos)

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        conn = sqlite3.connect("inventario.db")
        conn.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                       (nombre, categoria, precio, stock))
        conn.commit()
        conn.close()
        return redirect(url_for("listar")) 

    return render_template("registrar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        
        conn.execute("UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?",
                     (nombre, categoria, precio, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for("listar"))

    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("editar.html", producto=producto)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = sqlite3.connect("inventario.db")
    conn.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("listar"))

if __name__ == '__main__':
    init_database() 
    app.run(debug=True)