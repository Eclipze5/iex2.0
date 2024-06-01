from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv

from flaskr.auth import login_required
from .models import ANC, LDR, PNC, db
from flaskr.patient import get_patient

load_dotenv()

bp = Blueprint("diagnosis", __name__)

@bp.route('/view_anc/<int:diagnosis_id>')
@login_required
def view_anc(diagnosis_id):
    diagnosis = get_anc(diagnosis_id)
    patient = get_patient(diagnosis.patient_id)
    return render_template("diagnosis/view_anc.html", patient=patient, diagnosis=diagnosis)

@bp.route("/add_anc_compulsory/<int:patient_id>", methods=("GET", "POST"))
@login_required
def add_anc_compulsory(patient_id):
    if request.method == "POST":
        expected_delivery_date = request.form["expected_delivery_date"]
        terminate = "terminate" in request.form
        height = request.form["height"]
        last_menstrual_period = request.form["last_menstrual_period"]
        parity = request.form["parity"]
        living_children = request.form["living_children"]
        gravida = request.form["gravida"]
        
        error = None

        if not expected_delivery_date:
            error = "Expected date of delivery is required."
        elif not height:
            error = "Mother's height is required."
        elif not last_menstrual_period:
            error = "Last menstral period is required."
        elif not parity:
            error = "Parity is required."
        elif not living_children:
            error = "Number of living children is required."
        elif not gravida:
            error = "Gravida is required."

        if error is not None:
            flash(error)
        else:
            new_diagnosis = ANC(
                author_id=g.user.id,
                patient_id=patient_id,
                compulsory=True,

                expected_delivery_date=expected_delivery_date,
                terminate=terminate,
                height=height,
                last_menstrual_period=last_menstrual_period,
                parity=parity,
                living_children=living_children,
                gravida=gravida,
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient_anc", patient_id=patient_id))

    return render_template("diagnosis/add_anc_compulsory.html", patient_id=patient_id)

@bp.route("/add_anc_optional/<int:patient_id>", methods=("GET", "POST"))
@login_required
def add_anc_optional(patient_id):
    if request.method == "POST":
        medical_surgical_complications = request.form["medical_surgical_complications"]
        obstetric_other_complications = request.form["obstetric_other_complications"]
        weight = request.form["weight"]
        gestation = request.form["gestation"]
        blood_pressure = request.form["blood_pressure"]
        fetal_assessment = request.form["fetal_assessment"]
        fetal_heartbeat = request.form["fetal_heartbeat"]
        symphysiofundal_height = request.form["symphysiofundal_height"]
        complications = request.form["complications"]
        urine_dipstick = "urine_dipstick" in request.form
        vaccination = "vaccination" in request.form
        folic_acid = "folic_acid" in request.form
        mendabazole = "mendabazole" in request.form
        hepatitis = "hepatitis" in request.form

        error = None

        if not (medical_surgical_complications or
                obstetric_other_complications or
                weight or
                gestation or
                blood_pressure or
                fetal_assessment or
                fetal_heartbeat or
                symphysiofundal_height or
                complications or
                urine_dipstick or
                vaccination or
                folic_acid or
                mendabazole or
                hepatitis):
            error = "Can not submit an empty form."


        if error is not None:
            flash(error)
        else:
            new_diagnosis = ANC(
                author_id=g.user.id,
                patient_id=patient_id,
                compulsory=False,

                medical_surgical_complications=medical_surgical_complications,
                obstetric_other_complications=obstetric_other_complications,
                weight=weight,
                gestation=gestation,
                blood_pressure=blood_pressure,
                fetal_assessment=fetal_assessment,
                fetal_heartbeat=fetal_heartbeat,
                symphysiofundal_height=symphysiofundal_height,
                complications=complications,
                urine_dipstick=urine_dipstick,
                vaccination=vaccination,
                folic_acid=folic_acid,
                mendabazole=mendabazole,
                hepatitis=hepatitis,
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient_anc", patient_id=patient_id))

    return render_template("diagnosis/add_anc_optional.html", patient_id=patient_id)

@bp.route("/add_ldr/<int:patient_id>", methods=("GET", "POST"))
@login_required
def add_ldr(patient_id):
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        error = None

        if not category:
            error = "Category is required."
        elif not description:
            error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            new_diagnosis = LDR(
                category=category,
                description=description,
                author_id=g.user.id,
                patient_id=patient_id
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient", patient_id=patient_id))

    return render_template("diagnosis/add_diagnosis.html", patient_id=patient_id)

@bp.route("/add_pnc/<int:patient_id>", methods=("GET", "POST"))
@login_required
def add_pnc(patient_id):
    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        error = None

        if not category:
            error = "Category is required."
        elif not description:
            error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            new_diagnosis = PNC(
                category=category,
                description=description,
                author_id=g.user.id,
                patient_id=patient_id
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient", patient_id=patient_id))

    return render_template("diagnosis/add_diagnosis.html", patient_id=patient_id)

@bp.route("/update_anc/<int:diagnosis_id>", methods=["GET", "POST"])
@login_required
def update_anc(diagnosis_id):
    diagnosis = get_anc(diagnosis_id)

    if request.method == "POST":
        if diagnosis.compulsory:
            expected_delivery_date = request.form["expected_delivery_date"]
            terminate = "terminate" in request.form
            height = request.form["height"]
            last_menstrual_period = request.form["last_menstrual_period"]
            parity = request.form["parity"]
            living_children = request.form["living_children"]
            gravida = request.form["gravida"]

            error = None

            if not expected_delivery_date:
                error = "Expected date of delivery is required."
            elif not height:
                error = "Mother's height is required."
            elif not last_menstrual_period:
                error = "Last menstral period is required."
            elif not parity:
                error = "Parity is required."
            elif not living_children:
                error = "Number of living children is required."
            elif not gravida:
                error = "Gravida is required."

            if error is not None:
                flash(error)
            else:
                ANC.query.filter_by(id=diagnosis_id).update(
                    {"expected_delivery_date": expected_delivery_date,
                     "terminate": terminate,
                     "height": height,
                     "last_menstrual_period": last_menstrual_period,
                     "parity": parity,
                     "living_children": living_children,
                     "gravida": gravida}
                )
                db.session.commit()
                return redirect(url_for("patient.view_patient_anc", patient_id=diagnosis.patient_id))
        else:
            medical_surgical_complications = request.form["medical_surgical_complications"]
            obstetric_other_complications = request.form["obstetric_other_complications"]
            weight = request.form["weight"]
            gestation = request.form["gestation"]
            blood_pressure = request.form["blood_pressure"]
            fetal_assessment = request.form["fetal_assessment"]
            fetal_heartbeat = request.form["fetal_heartbeat"]
            symphysiofundal_height = request.form["symphysiofundal_height"]
            complications = request.form["complications"]
            urine_dipstick = "urine_dipstick" in request.form
            vaccination = "vaccination" in request.form
            folic_acid = "folic_acid" in request.form
            mendabazole = "mendabazole" in request.form
            hepatitis = "hepatitis" in request.form

            error = None

            if not (medical_surgical_complications or
                    obstetric_other_complications or
                    weight or
                    gestation or
                    blood_pressure or
                    fetal_assessment or
                    fetal_heartbeat or
                    symphysiofundal_height or
                    complications or
                    urine_dipstick or
                    vaccination or
                    folic_acid or
                    mendabazole or
                    hepatitis):
                error = "Can not submit an empty form."

            if error is not None:
                flash(error)
            else:
                ANC.query.filter_by(id=diagnosis_id).update(
                    {"medical_surgical_complications": medical_surgical_complications,
                     "obstetric_other_complications": obstetric_other_complications,
                     "weight": weight,
                     "gestation": gestation,
                     "blood_pressure": blood_pressure,
                     "urine_dipstick": urine_dipstick,
                     "fetal_assessment": fetal_assessment,
                     "fetal_heartbeat": fetal_heartbeat,
                     "symphysiofundal_height": symphysiofundal_height,
                     "complications": complications,
                     "vaccination": vaccination,
                     "folic_acid": folic_acid,
                     "mendabazole": mendabazole,
                     "hepatitis": hepatitis}
                )
                db.session.commit()
                return redirect(url_for("patient.view_patient_anc", patient_id=diagnosis.patient_id))

    return render_template("diagnosis/update_anc.html", diagnosis=diagnosis)

@bp.route("/update_ldr/<int:diagnosis_id>", methods=["GET", "POST"])
@login_required
def update_ldr(diagnosis_id):
    diagnosis = get_ldr(diagnosis_id)

    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        error = None

        if not category:
            error = "Category is required."
        elif not description:
            error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            ANC.query.filter_by(id=diagnosis_id).update(
                {"category": category, "description": description}
            )
            db.session.commit()
            return redirect(url_for("patient.view_patient", patient_id=diagnosis.patient_id))

    return render_template("diagnosis/update_diagnosis.html", diagnosis=diagnosis)

@bp.route("/update_pnc/<int:diagnosis_id>", methods=["GET", "POST"])
@login_required
def update_pnc(diagnosis_id):
    diagnosis = get_pnc(diagnosis_id)

    if request.method == "POST":
        category = request.form["category"]
        description = request.form["description"]
        error = None

        if not category:
            error = "Category is required."
        elif not description:
            error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            ANC.query.filter_by(id=diagnosis_id).update(
                {"category": category, "description": description}
            )
            db.session.commit()
            return redirect(url_for("patient.view_patient", patient_id=diagnosis.patient_id))

    return render_template("diagnosis/update_diagnosis.html", diagnosis=diagnosis)

@bp.route("/delete_anc/<int:diagnosis_id>", methods=["POST"])
@login_required
def delete_anc(diagnosis_id):
    patient_id = get_anc(diagnosis_id).patient_id
    diagnosis_to_delete = ANC.query.get(diagnosis_id)

    if diagnosis_to_delete:
        db.session.delete(diagnosis_to_delete)
        db.session.commit()
        flash(f"Diagnosis deleted successfully", "success")
    else:
        flash(f"Diagnosis not found", "danger")

    return redirect(url_for("patient.view_patient_anc", patient_id=patient_id))

@bp.route("/delete_anc/<int:diagnosis_id>", methods=["POST"])
@login_required
def delete_ldr(diagnosis_id):
    patient_id = get_ldr(diagnosis_id).patient_id
    diagnosis_to_delete = LDR.query.get(diagnosis_id)

    if diagnosis_to_delete:
        db.session.delete(diagnosis_to_delete)
        db.session.commit()
        flash(f"Diagnosis deleted successfully", "success")
    else:
        flash(f"Diagnosis not found", "danger")

    return redirect(url_for("patient.view_patient", patient_id=patient_id))

@bp.route("/delete_anc/<int:diagnosis_id>", methods=["POST"])
@login_required
def delete_pnc(diagnosis_id):
    patient_id = get_pnc(diagnosis_id).patient_id
    diagnosis_to_delete = PNC.query.get(diagnosis_id)

    if diagnosis_to_delete:
        db.session.delete(diagnosis_to_delete)
        db.session.commit()
        flash(f"Diagnosis deleted successfully", "success")
    else:
        flash(f"Diagnosis not found", "danger")

    return redirect(url_for("patient.view_patient", patient_id=patient_id))

def get_anc(diagnosis_id, check_author=True):
    diagnosis = ANC.query.get(diagnosis_id)

    if diagnosis is None:
        abort(404, f"Patient id {diagnosis_id} doesn't exist.")

    if check_author and diagnosis.author_id != g.user.id:
        abort(403)

    return diagnosis

def get_ldr(diagnosis_id, check_author=True):
    diagnosis = LDR.query.get(diagnosis_id)

    if diagnosis is None:
        abort(404, f"Patient id {diagnosis_id} doesn't exist.")

    if check_author and diagnosis.author_id != g.user.id:
        abort(403)

    return diagnosis

def get_pnc(diagnosis_id, check_author=True):
    diagnosis = PNC.query.get(diagnosis_id)

    if diagnosis is None:
        abort(404, f"Patient id {diagnosis_id} doesn't exist.")

    if check_author and diagnosis.author_id != g.user.id:
        abort(403)

    return diagnosis