from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Configuración de la base de datos SQLite
# Usa la variable de entorno DATABASE_URL definida en docker-compose.yml
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.environ.get('DATABASE_URL', '/app/data/medical_agenda.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    app.run(debug=True, host='0.0.0.0', port=5000)