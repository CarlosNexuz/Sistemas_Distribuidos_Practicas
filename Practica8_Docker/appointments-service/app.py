from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

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

# Definición del modelo de Cita
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False) # Asumimos que el paciente existe
    doctor_id = db.Column(db.Integer, nullable=False)  # Asumimos que el doctor existe
    date = db.Column(db.String(10), nullable=False)  # Formato YYYY-MM-DD
    time = db.Column(db.String(5), nullable=False)   # Formato HH:MM
    status = db.Column(db.String(20), default='Scheduled') # Ej: Scheduled, Completed, Cancelled

    def __repr__(self):
        return '<Appointment %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
            'time': self.time,
            'status': self.status
        }

# API Resource para Citas Individuales (GET, PUT, DELETE)
class AppointmentResource(Resource):
    def get(self, appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        return appointment.to_dict()

    def put(self, appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided'}, 400
        
        # Validaciones básicas de formato de fecha/hora si se proporcionan
        if 'date' in data:
            try:
                datetime.strptime(data['date'], '%Y-%m-%d')
                appointment.date = data['date']
            except ValueError:
                return {'message': 'Invalid date format. Use YYYY-MM-DD'}, 400
        
        if 'time' in data:
            try:
                datetime.strptime(data['time'], '%H:%M')
                appointment.time = data['time']
            except ValueError:
                return {'message': 'Invalid time format. Use HH:MM'}, 400

        appointment.patient_id = data.get('patient_id', appointment.patient_id)
        appointment.doctor_id = data.get('doctor_id', appointment.doctor_id)
        appointment.status = data.get('status', appointment.status)
        
        db.session.commit()
        return appointment.to_dict()

    def delete(self, appointment_id):
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return {'message': 'Appointment deleted'}, 204

# API Resource para Listar y Crear Citas (GET, POST)
class AppointmentListResource(Resource):
    def get(self):
        appointments = Appointment.query.all()
        return [a.to_dict() for a in appointments]

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ('patient_id', 'doctor_id', 'date', 'time')):
            return {'message': 'Missing required fields: patient_id, doctor_id, date, time'}, 400
        
        # Validaciones de formato de fecha/hora
        try:
            datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return {'message': 'Invalid date format for date. Use YYYY-MM-DD'}, 400
        
        try:
            datetime.strptime(data['time'], '%H:%M')
        except ValueError:
            return {'message': 'Invalid time format for time. Use HH:MM'}, 400
        
        new_appointment = Appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            date=data['date'],
            time=data['time'],
            status=data.get('status', 'Scheduled')
        )
        db.session.add(new_appointment)
        db.session.commit()
        return new_appointment.to_dict(), 201

# Añadir recursos a la API
api.add_resource(AppointmentListResource, '/appointments', '/appointments/')
api.add_resource(AppointmentResource, '/appointments/<int:appointment_id>')

# Crear las tablas de la base de datos si no existen
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