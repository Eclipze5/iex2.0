from flask_sqlalchemy import SQLAlchemy

# flask db migrate -m "Description of the changes"
# flask db upgrade

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    sex = db.Column(db.String(16), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<Patient {self.name}>'

class ANC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    compulsory = db.Column(db.Boolean, nullable=True, default=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    expected_delivery_date = db.Column(db.Date, nullable=True)
    terminate = db.Column(db.Boolean, nullable=True, default=False)
    height = db.Column(db.String(8), nullable=True)
    last_menstrual_period = db.Column(db.Date, nullable=True)
    parity = db.Column(db.String(8), nullable=True)
    living_children = db.Column(db.String(8), nullable=True)
    gravida = db.Column(db.String(8), nullable=True)

    medical_surgical_complications = db.Column(db.Text, nullable=True)
    obstetric_other_complications = db.Column(db.Text, nullable=True)
    weight = db.Column(db.String(8), nullable=True)
    gestation = db.Column(db.String(8), nullable=True)
    blood_pressure = db.Column(db.String(8), nullable=True)
    urine_dipstick = db.Column(db.Boolean, nullable=True, default=False)
    fetal_assessment = db.Column(db.Text, nullable=True)
    fetal_heartbeat = db.Column(db.String(8), nullable=True)
    symphysiofundal_height = db.Column(db.String(8), nullable=True)
    complications = db.Column(db.Text, nullable=True)
    vaccination = db.Column(db.Boolean, nullable=True, default=False)
    folic_acid = db.Column(db.Boolean, nullable=True, default=False)
    mendabazole = db.Column(db.Boolean, nullable=True, default=False)
    hepatitis = db.Column(db.Boolean, nullable=True, default=False)

class LDR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    category = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)

class PNC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    category = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Diagnosis {self.id}>'