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

@bp.route('/view_ldr/<int:diagnosis_id>')
@login_required
def view_ldr(diagnosis_id):
    diagnosis = get_ldr(diagnosis_id)
    patient = get_patient(diagnosis.patient_id)
    return render_template("diagnosis/view_ldr.html", patient=patient, diagnosis=diagnosis)

@bp.route('/view_pnc/<int:diagnosis_id>')
@login_required
def view_pnc(diagnosis_id):
    diagnosis = get_pnc(diagnosis_id)
    patient = get_patient(diagnosis.patient_id)
    return render_template("diagnosis/view_pnc.html", patient=patient, diagnosis=diagnosis)

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
        medical_surgical_complications = request.form["medical_surgical_complications"]
        obstetric_other_complications = request.form["obstetric_other_complications"]
        
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
                medical_surgical_complications=medical_surgical_complications,
                obstetric_other_complications=obstetric_other_complications,
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient_anc", patient_id=patient_id))

    return render_template("diagnosis/add_anc_compulsory.html", patient_id=patient_id)

@bp.route("/add_anc_optional/<int:patient_id>", methods=("GET", "POST"))
@login_required
def add_anc_optional(patient_id):
    if request.method == "POST":
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

        if not (weight or
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
        labour_onset = request.form["labour_onset"]
        membranes_ruptured = request.form["membranes_ruptured"]
        duration_2nd_stage = request.form["duration_2nd_stage"]
        duration_3rd_stage = request.form["duration_3rd_stage"]
        placenta_delivery = request.form["placenta_delivery"]
        placenta_complete = "placenta_complete" in request.form
        membranes_complete = "membranes_complete" in request.form
        placenta_weight = request.form["placenta_weight"]
        blood_loss = request.form["blood_loss"]
        shoulder_dystocia = "shoulder_dystocia" in request.form
        tear = "tear" in request.form
        ulterine_rupture = "ulterine_rupture" in request.form
        obsteric_hysterectomy = "obsteric_hysterectomy" in request.form
        comments = request.form["comments"]
        attendent = request.form["attendent"]
        other_delivery_method = request.form["other_delivery_method"]
        delivery_liquor = request.form["delivery_liquor"]
        name = request.form["name"]
        delivery_date = request.form["delivery_date"]
        sex = request.form["sex"]
        condition = request.form["condition"]
        weight = request.form["weight"]
        length = request.form["length"]
        head_circumference = request.form["head_circumference"]
        death_time = None if request.form["death_time"] == "" else request.form["death_time"]

        error = None

        # if not expected_delivery_date:
        #     error = "Expected date of delivery is required."
        # elif not height:
        #     error = "Mother's height is required."

        if error is not None:
            flash(error)
        else:
            new_diagnosis = LDR(
                author_id=g.user.id,
                patient_id=patient_id,

                labour_onset=labour_onset,
                membranes_ruptured=membranes_ruptured,
                duration_2nd_stage=duration_2nd_stage,
                duration_3rd_stage=duration_3rd_stage,
                placenta_delivery=placenta_delivery,
                placenta_complete=placenta_complete,
                membranes_complete=membranes_complete,
                placenta_weight=placenta_weight,
                blood_loss=blood_loss,
                shoulder_dystocia=shoulder_dystocia,
                tear=tear,
                ulterine_rupture=ulterine_rupture,
                obsteric_hysterectomy=obsteric_hysterectomy,
                comments=comments,
                attendent=attendent,
                other_delivery_method=other_delivery_method,
                delivery_liquor=delivery_liquor,
                name=name,
                delivery_date=delivery_date,
                sex=sex,
                condition=condition,
                weight=weight,
                length=length,
                head_circumference=head_circumference,
                death_time=death_time,
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient_ldr", patient_id=patient_id))

    return render_template("diagnosis/add_ldr.html", patient_id=patient_id)

@bp.route("/add_pnc/<int:patient_id>", methods=("GET", "POST"))
@login_required
def add_pnc(patient_id):
    if request.method == "POST":
        transferred_from = request.form["transferred_from"]
        mother_height = request.form["mother_height"]
        mother_weight = request.form["mother_weight"]
        baby_weight = request.form["baby_weight"]
        mother_comments = request.form["mother_comments"]
        baby_comments = request.form["baby_comments"]
        other_comments = request.form["other_comments"]

        error = None

        # if not category:
        #     error = "Category is required."
        # elif not description:
        #     error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            new_diagnosis = PNC(
                author_id=g.user.id,
                patient_id=patient_id,

                transferred_from = transferred_from,
                mother_height = mother_height,
                mother_weight=mother_weight,
                baby_weight=baby_weight,
                mother_comments=mother_comments,
                baby_comments=baby_comments,
                other_comments=other_comments,
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            return redirect(url_for("patient.view_patient_pnc", patient_id=patient_id))

    return render_template("diagnosis/add_pnc.html", patient_id=patient_id)

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
            medical_surgical_complications = request.form["medical_surgical_complications"]
            obstetric_other_complications = request.form["obstetric_other_complications"]

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
                    {"medical_surgical_complications": medical_surgical_complications,
                     "obstetric_other_complications": obstetric_other_complications,
                     "expected_delivery_date": expected_delivery_date,
                     "terminate": terminate,
                     "height": height,
                     "last_menstrual_period": last_menstrual_period,
                     "parity": parity,
                     "living_children": living_children,
                     "gravida": gravida}
                )
                db.session.commit()
                flash('Ante natal care is updated', 'success')
                return redirect(url_for("patient.view_patient_anc", patient_id=diagnosis.patient_id))
        else:
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

            if not (weight or
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
                    {"weight": weight,
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
                flash('Ante natal care is updated', 'success')
                return redirect(url_for("patient.view_patient_anc", patient_id=diagnosis.patient_id))

    return render_template("diagnosis/update_anc.html", diagnosis=diagnosis)

@bp.route("/update_ldr/<int:diagnosis_id>", methods=["GET", "POST"])
@login_required
def update_ldr(diagnosis_id):
    diagnosis = get_ldr(diagnosis_id)

    if request.method == "POST":
        labour_onset = request.form["labour_onset"]
        membranes_ruptured = request.form["membranes_ruptured"]
        duration_2nd_stage = request.form["duration_2nd_stage"]
        duration_3rd_stage = request.form["duration_3rd_stage"]
        placenta_delivery = request.form["placenta_delivery"]
        placenta_complete = "placenta_complete" in request.form
        membranes_complete = "membranes_complete" in request.form
        placenta_weight = request.form["placenta_weight"]
        blood_loss = request.form["blood_loss"]
        shoulder_dystocia = "shoulder_dystocia" in request.form
        tear = "tear" in request.form
        ulterine_rupture = "ulterine_rupture" in request.form
        obsteric_hysterectomy = "obsteric_hysterectomy" in request.form
        comments = request.form["comments"]
        attendent = request.form["attendent"]
        other_delivery_method = request.form["other_delivery_method"]
        delivery_liquor = request.form["delivery_liquor"]
        name = request.form["name"]
        delivery_date = request.form["delivery_date"]
        sex = request.form["sex"]
        condition = request.form["condition"]
        weight = request.form["weight"]
        length = request.form["length"]
        head_circumference = request.form["head_circumference"]
        death_time = None if request.form["death_time"] == "" else request.form["death_time"]

        error = None

        # if not category:
        #     error = "Category is required."
        # elif not description:
        #     error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            LDR.query.filter_by(id=diagnosis_id).update(
                {"labour_onset": labour_onset,
                "membranes_ruptured": membranes_ruptured,
                "duration_2nd_stage": duration_2nd_stage,
                "duration_3rd_stage": duration_3rd_stage,
                "placenta_delivery": placenta_delivery,
                "placenta_complete": placenta_complete,
                "membranes_complete": membranes_complete,
                "placenta_weight": placenta_weight,
                "blood_loss": blood_loss,
                "shoulder_dystocia": shoulder_dystocia,
                "tear": tear,
                "ulterine_rupture": ulterine_rupture,
                "obsteric_hysterectomy": obsteric_hysterectomy,
                "comments": comments,
                "attendent": attendent,
                "other_delivery_method": other_delivery_method,
                "delivery_liquor": delivery_liquor,
                "name": name,
                "delivery_date": delivery_date,
                "sex": sex,
                "condition": condition,
                "weight": weight,
                "length": length,
                "head_circumference": head_circumference,
                "death_time": death_time}
            )
            db.session.commit()
            flash('Labour & delivery record is updated', 'success')
            return redirect(url_for("patient.view_patient_ldr", patient_id=diagnosis.patient_id))

    return render_template("diagnosis/update_ldr.html", diagnosis=diagnosis)

@bp.route("/update_pnc/<int:diagnosis_id>", methods=["GET", "POST"])
@login_required
def update_pnc(diagnosis_id):
    diagnosis = get_pnc(diagnosis_id)

    if request.method == "POST":
        transferred_from = request.form["transferred_from"]
        mother_height = request.form["mother_height"]
        mother_weight = request.form["mother_weight"]
        baby_weight = request.form["baby_weight"]
        mother_comments = request.form["mother_comments"]
        baby_comments = request.form["baby_comments"]
        other_comments = request.form["other_comments"]

        error = None

        # if not category:
        #     error = "Category is required."
        # elif not description:
        #     error = "Description of Birth is required."

        if error is not None:
            flash(error)
        else:
            PNC.query.filter_by(id=diagnosis_id).update(
                {"transferred_from": transferred_from,
                 "mother_height": mother_height,
                 "mother_weight": mother_weight,
                 "baby_weight": baby_weight,
                 "mother_comments": mother_comments,
                 "baby_comments": baby_comments,
                 "other_comments": other_comments}
            )
            db.session.commit()
            flash('Post natal care is updated', 'success')
            return redirect(url_for("patient.view_patient_pnc", patient_id=diagnosis.patient_id))

    return render_template("diagnosis/update_pnc.html", diagnosis=diagnosis)

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

@bp.route("/delete_ldr/<int:diagnosis_id>", methods=["POST"])
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

    return redirect(url_for("patient.view_patient_ldr", patient_id=patient_id))

@bp.route("/delete_pnc/<int:diagnosis_id>", methods=["POST"])
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

    return redirect(url_for("patient.view_patient_pnc", patient_id=patient_id))

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