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
db_connection_name = os.environ.get('INSTANCE_CONNECTION_NAME')

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

# Definición del modelo de Doctor
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    specialty = db.Column(db.String(80), nullable=False)
    # Ejemplo de disponibilidad, puedes expandir esto a una tabla separada si es más complejo
    availability = db.Column(db.String(255)) # Ej. "Lunes 9-17, Martes 9-13"

    def __repr__(self):
        return '<Doctor %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'availability': self.availability
        }

# API Resource para Doctores Individuales (GET, PUT, DELETE)
class DoctorResource(Resource):
    def get(self, doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        return doctor.to_dict()

    def put(self, doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        doctor.name = data.get('name', doctor.name)
        doctor.specialty = data.get('specialty', doctor.specialty)
        doctor.availability = data.get('availability', doctor.availability)
        
        db.session.commit()
        return doctor.to_dict()

    def delete(self, doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return {'message': 'Doctor deleted'}, 204 # 204 No Content

# API Resource para Listar y Crear Doctores (GET, POST)
class DoctorListResource(Resource):
    def get(self):
        doctors = Doctor.query.all()
        return [d.to_dict() for d in doctors]

    def post(self):
        data = request.get_json()
        if not data or not 'name' in data or not 'specialty' in data:
            return {'message': 'Name and specialty are required'}, 400
        
        new_doctor = Doctor(
            name=data['name'],
            specialty=data['specialty'],
            availability=data.get('availability')
        )
        db.session.add(new_doctor)
        db.session.commit()
        return new_doctor.to_dict(), 201 # 201 Created

# Añadir recursos a la API
api.add_resource(DoctorListResource, '/doctors','/doctors/')
api.add_resource(DoctorResource, '/doctors/<int:doctor_id>')

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