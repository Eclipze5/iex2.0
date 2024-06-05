from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import abort
from .pagination_collection import PaginationCollection
from sqlalchemy import union_all

from .models import User, Patient, ANC, LDR, PNC, db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/user', methods=('GET', 'POST'))
def index():
    if not g.user.is_admin:
        abort(403)

    builder = User.query.order_by(User.username)

    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('user/index.html', pagination_collection=pagination_collection)

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    anc_count = (
        db.session.query(ANC)
        .filter(ANC.author_id == g.user.id)
        .count()
    )
    ldr_count = (
        db.session.query(LDR)
        .filter(LDR.author_id == g.user.id)
        .count()
    )
    pnc_count = (
        db.session.query(PNC)
        .filter(PNC.author_id == g.user.id)
        .count()
    )
    return render_template('user/profile.html',
                           user=g.user,
                           anc_count=anc_count,
                           ldr_count=ldr_count,
                           pnc_count=pnc_count)

@bp.route('/profile/<int:type>', methods=('GET', 'POST'))
def recent_diagnosis(type):
    if type == 0:
        builder = (
            db.session.query(ANC, Patient)
            .filter(ANC.author_id == g.user.id)
            .join(Patient, ANC.patient_id == Patient.id)
            .order_by(ANC.created.desc())
        )
    if type == 1:
        builder = (
            db.session.query(LDR, Patient)
            .filter(LDR.author_id == g.user.id)
            .join(Patient, LDR.patient_id == Patient.id)
            .order_by(LDR.created.desc())
        )
    if type == 2:
        builder = (
            db.session.query(PNC, Patient)
            .filter(PNC.author_id == g.user.id)
            .join(Patient, PNC.patient_id == Patient.id)
            .order_by(PNC.created.desc())
        )

    page = request.args.get('page', type=int, default=1)

    pagination_collection = PaginationCollection(builder, page)

    return render_template('user/recent_diagnosis.html',
                           user=g.user,
                           type=type,
                           diagnosis=pagination_collection.items,
                           pagination=pagination_collection.pagination)

@bp.route('/<int:id>', methods=('GET', 'POST'))
def user_edit(id):

    if not g.user.is_admin:
        abort(403)

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        username = request.form.get('username', type=str)
        password = request.form.get('password', type=str, default=None)
        confirm_password = request.form.get('confirmation', type=str, default=None)
        is_admin = request.form.get('is_admin', type=bool, default=False)
        if password:
            if password != confirm_password:
                error = 'Passwords do not match.'
            else:
                user.password = generate_password_hash(password)

        user.username = username
        user.is_admin = is_admin
        db.session.commit()
        if 'error' in locals():
            flash(error)
        else:
            flash('User is updated', 'success')
            return redirect(url_for('user.index'))

    return render_template('user/form.html', user=user)

@bp.route('/create', methods=('GET', 'POST'))
def user_create():
    if not g.user.is_admin:
        abort(403)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        is_admin = True if request.form.get('is_admin') == 1 else False

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmation:
            error = 'Passwords do not match.'
        elif User.query.filter_by(username=username).count():
            error = f"User {username} is already registered."

        if 'error' in locals():
            flash(error)
        else:
            new_user = User(username=username, password=generate_password_hash(password), is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("user.index"))

    return render_template('user/form.html', user=User())

@bp.route('/delete/<int:user_id>', methods=['POST'])
def user_delete(user_id):
    user_to_delete = User.query.get(user_id)

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"User deleted successfully", 'success')
    else:
        flash(f"User not found", 'danger')

    return redirect(url_for('user.index'))