from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)

# --- INICIO MODIFICACIÓN CLOUD ---
# Configuración de la base de datos para Cloud SQL (PostgreSQL)
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'Hola2626#')
db_name = os.environ.get('DB_NAME', 'medical_agenda')
# El 'Instance Connection Name' se obtiene de la consola de GCP (ej: project:region:instance)
db_connection_name = os.environ.get('microservicios-480304:northamerica-south1:medical-db-instance')

if db_connection_name:
    # Configuración para Producción en Cloud Run (usando Unix Socket)
    socket_path = f'/cloudsql/{db_connection_name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@/{db_name}?host={socket_path}'
else:
    # Configuración para Local/Testing (usando TCP)
    # Si no hay connection name, asume local o docker-compose con host explícito
    db_host = os.environ.get('DB_HOST', 'localhost')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# --- FIN MODIFICACIÓN CLOUD ---

db = SQLAlchemy(app)

# Definición del modelo de Paciente
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.String(10)) # Date of Birth YYYY-MM-DD
    history = db.Column(db.String(255))

    def __repr__(self):
        return '<Patient %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'history': self.history
        }

# API Resource para Pacientes
class PatientResource(Resource):
    def get(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        return patient.to_dict()

    def put(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()
        patient.name = data.get('name', patient.name)
        patient.dob = data.get('dob', patient.dob)
        patient.history = data.get('history', patient.history)
        db.session.commit()
        return patient.to_dict()

    def delete(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {'message': 'Patient deleted'}, 204

class PatientListResource(Resource):
    def get(self):
        patients = Patient.query.all()
        return [p.to_dict() for p in patients]

    def post(self):
        data = request.get_json()
        if not data or not 'name' in data:
            return {'message': 'Name is required'}, 400
        new_patient = Patient(name=data['name'], dob=data.get('dob'), history=data.get('history'))
        db.session.add(new_patient)
        db.session.commit()
        return new_patient.to_dict(), 201

# Añadir recursos a la API
api.add_resource(PatientListResource, '/patients','/patients/')
api.add_resource(PatientResource, '/patients/<int:patient_id>')

# Crear la base de datos si no existe
# Esto es importante para la primera vez que se ejecutan los servicios
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # --- INICIO MODIFICACIÓN CLOUD ---
    # Usar el puerto definido por la variable de entorno PORT (Cloud Run usa 8080 por defecto)
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
    # --- FIN MODIFICACIÓN CLOUD ---