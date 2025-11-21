from flask import Flask, request
import sqlite3
import json
import subprocess
import pickle

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT OR IGNORE INTO users VALUES(1, 'admin')")
    conn.commit()
    conn.close()

init_db()

# 1. SQL INJECTION

@app.route("/sql-injection-vulnerable")
def sql_injection():
    name = request.args.get("name", "")

    query = f"SELECT * FROM users WHERE name = '{name}'"
    
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    try:
        cur.execute(query)
        result = cur.fetchall()
        if result:
            return "infectado" 
        return "ok"
    except:
        return "infectado"

@app.route("/sql-injection-safe")
def sql_injection_safe():
    name = request.args.get("name", "")
    
    query = "SELECT * FROM users WHERE name = ?"
    
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute(query, (name,))
    result = cur.fetchall()

    return "ok"

# 2. CONTROLE DE ACESSO

@app.route("/acesso-vulneravel")
def acesso_vulneravel():
    role = request.args.get("role", "user")
    
    if role == "admin":  
        return "infectado"
    return "ok"

@app.route("/acesso-seguro")
def acesso_seguro():
    token = request.headers.get("X-Token")

    if token != "admin-token":
        return "ok"
    return "ok" 

# 3. DESSERIALIZAÇÃO INSEGURA

@app.route("/deserializacao-vulneravel", methods=["POST"])
def deserializacao_vulneravel():
    payload = request.data
    try:
        obj = pickle.loads(payload) 
        return "infectado"
    except:
        return "ok"

@app.route("/deserializacao-segura", methods=["POST"])
def deserializacao_segura():
    try:
        data = json.loads(request.data)
        return "ok"
    except:
        return "ok"
    
# 4. INJEÇÃO DE COMANDO

@app.route("/comando-vulneravel")
def comando_vulneravel():
    cmd = request.args.get("cmd", "")

    try:
        output = subprocess.check_output(cmd, shell=True)
        return "infectado"
    except:
        return "ok"

@app.route("/comando-seguro")
def comando_seguro():
    allowed = ["date", "whoami"]
    cmd = request.args.get("cmd", "")

    if cmd not in allowed:
        return "ok"
    
    output = subprocess.check_output(["/usr/bin/" + cmd])
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
