from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta' 

def generar_id():
    if 'inscritos' in session and len(session['inscritos']) > 0:
        return max(inscrito['id'] for inscrito in session['inscritos']) + 1
    else:
        return 1

@app.route("/", methods=["GET", "POST"])
def index():
    if 'inscritos' not in session:
        session['inscritos'] = []

    seminarios_disponibles = [
        "Inteligencia Artificial",
        "Machine Learning",
        "Simulación con Arena",
        "Robótica Educativa"
    ]

    if request.method == "POST":
        nuevo_id = generar_id()

        fecha = request.form["fecha"]
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        turno = request.form["turno"]
        seminario = request.form["seminario"]

        inscritos = session['inscritos']
        inscritos.append({
            "id": nuevo_id,  
            "fecha": fecha,
            "nombre": nombre,
            "apellidos": apellidos,
            "turno": turno,
            "seminario": seminario
        })
        session['inscritos'] = inscritos

        return redirect(url_for("listado"))

    return render_template("index.html", seminarios_disponibles=seminarios_disponibles)

@app.route("/listado")
def listado():
    inscritos = session.get('inscritos', [])
    return render_template("listado.html", inscritos=inscritos)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    inscritos = session.get('inscritos', [])
    inscritos = [inscrito for inscrito in inscritos if inscrito['id'] != id]
    session['inscritos'] = inscritos
    return redirect(url_for('listado'))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    inscritos = session.get('inscritos', [])
    inscrito = next((inscrito for inscrito in inscritos if inscrito['id'] == id), None)
    
    if inscrito:
        if request.method == "POST":
            
            inscrito['fecha'] = request.form["fecha"]
            inscrito['nombre'] = request.form["nombre"]
            inscrito['apellidos'] = request.form["apellidos"]
            inscrito['turno'] = request.form["turno"]
            inscrito['seminario'] = request.form["seminario"]

            session['inscritos'] = inscritos
            return redirect(url_for('listado'))

        return render_template("editar.html", inscrito=inscrito)
    
    return redirect(url_for('listado'))

if __name__ == "__main__":
    app.run(debug=True)
