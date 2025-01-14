from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uqc7o8xpmfjx3bp8:h6IFc0cg54goGKKpAi7A@byzou5xdwhdq5g0tauyq-mysql.services.clever-cloud.com:3306/byzou5xdwhdq5g0tauyq'
db = SQLAlchemy(app)

# Modelo para almacenar diagnósticos
class Diagnostico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    diagnostico = db.Column(db.String(200), nullable=False)

# Base de conocimiento simple
diagnosticos = {
    "fiebre": "Puede ser un signo de infección.",
    "tos": "Puede ser un síntoma de resfriado o gripe.",
    "dolor de cabeza": "Puede ser causado por estrés o deshidratación.",
    # Agrega más diagnósticos aquí
}

@app.route('/')
def index():
    diagnosticos = Diagnostico.query.all()  # Obtener todos los diagnósticos
    return render_template('index.html', diagnosticos=diagnosticos)

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    sintomas = request.form.get('sintomas')
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    
    # Verifica si los valores son nulos
    if not nombre or not telefono:
        return "Nombre y teléfono son obligatorios", 400
    
    resultado = diagnosticos.get(sintomas.lower(), "Síntoma no encontrado.")
    
    # Guardar en la base de datos
    nuevo_diagnostico = Diagnostico(nombre=nombre, telefono=telefono, diagnostico=resultado)
    db.session.add(nuevo_diagnostico)
    db.session.commit()
    
    return render_template('result.html', resultado=resultado)

@app.route('/historial')
def historial():
    diagnosticos = Diagnostico.query.all()
    return render_template('historial.html', diagnosticos=diagnosticos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos
    app.run(debug=True)