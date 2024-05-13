from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv

from flaskr.auth import login_required
from .models import User, Patient, ANC, LDR, PNC, db
from .pagination_collection import PaginationCollection
load_dotenv()

bp = Blueprint('patient', __name__)

@bp.route('/add_patient', methods=('GET', 'POST'))
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        address = request.form['address']
        error = None

        if not name:
            error = 'Name is required.'
        elif not date_of_birth:
            error = 'Date of Birth is required.'
        elif not phone:
            error = 'Phone is required.'
        elif not address:
            error = 'Address is required.'

        if error is not None:
            flash(error)
        else:
            new_patient = Patient(name=str(name), sex=str(sex), date_of_birth=str(date_of_birth), phone=str(phone), address=str(address))
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('main.index'))

    return render_template('patient/add_patient.html')

@bp.route('/update_patient/<int:patient_id>', methods=('GET', 'POST'))
@login_required
def update_patient(patient_id):
    if g.user.is_admin == 0:
        abort(403)

    patient = get_patient(patient_id)

    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        date_of_birth = request.form['date_of_birth']
        phone = request.form['phone']
        address = request.form['address']

        if not name:
            error = 'Name is required.'
        elif not date_of_birth:
            error = 'Date of Birth is required.'
        elif not phone:
            error = 'Phone is required.'
        elif not address:
            error = 'Address is required.'

        if 'error' in locals():
            flash(error)
        else:
            Patient.query.filter_by(id=patient_id).update(
                {"name": name, "sex": sex, "date_of_birth": date_of_birth, "phone": phone, "address": address}
            )
            db.session.commit()
            flash('Patient is updated', 'success')
            return redirect(url_for('main.index'))

    return render_template('patient/update_patient.html', patient=patient)

@bp.route('/delete_patient/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient_to_delete = Patient.query.get(patient_id)
    if patient_to_delete:
        db.session.delete(patient_to_delete)
        db.session.commit()
        flash(f"Patient {patient_id} deleted successfully", 'success')
    else:
        flash(f"Patient with ID {patient_id} not found", 'danger')
    return redirect(url_for('main.index'))

@bp.route('/view/<int:patient_id>')
@login_required
def view_patient(patient_id):
    anc_count = (
        db.session.query(ANC, User)
        .filter(ANC.patient_id == patient_id)
        .count()
    )
    ldr_count = (
        db.session.query(LDR, User)
        .filter(ANC.patient_id == patient_id)
        .count()
    )
    pnc_count = (
        db.session.query(PNC, User)
        .filter(ANC.patient_id == patient_id)
        .count()
    )
    return render_template('patient/view_patient.html', patient=get_patient(patient_id), anc_count=anc_count, ldr_count=ldr_count, pnc_count=pnc_count)

@bp.route('/view/<int:patient_id>/<int:type>')
@login_required
def view_patient_diagnosis(patient_id, type):
    if type == 0:
        builder = (
            db.session.query(ANC, User)
            .filter(ANC.patient_id == patient_id)
            .join(User, ANC.author_id == User.id)
            .order_by(ANC.created.desc())
        )
    elif type == 1:
        builder = (
            db.session.query(LDR, User)
            .filter(ANC.patient_id == patient_id)
            .join(User, ANC.author_id == User.id)
            .order_by(ANC.created.desc())
        )
    elif type == 2:
        builder = (
            db.session.query(PNC, User)
            .filter(ANC.patient_id == patient_id)
            .join(User, ANC.author_id == User.id)
            .order_by(ANC.created.desc())
        )
    page = request.args.get('page', type=int, default=1)
    pagination_collection = PaginationCollection(builder, page)
    return render_template('patient/view_patient_diagnosis.html',
                           patient=get_patient(patient_id),
                           diagnosis=pagination_collection.items,
                           type=type,
                           pagination=pagination_collection.pagination)

def get_patient(patient_id):
    patient = Patient.query.get(patient_id)

    if patient is None:
        abort(404, f"Patient id {patient_id} doesn't exist.")

    return patient