from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Route
from routes.admin import admin_required

route_bp = Blueprint('route_admin', __name__, url_prefix='/admin/routes')

@route_bp.route('/')
@admin_required
def index():
    all_routes = Route.query.all()
    return render_template('admin/routes.html', routes=all_routes)

#create route
@route_bp.route('/add', methods=['POST'])
@admin_required
def add():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    distance = request.form.get('distance')
    via = request.form.get('via')

    try:
        new_route = Route(origin=origin, destination=destination, distance=int(distance) if distance else None, via=via)
        db.session.add(new_route)
        db.session.commit()
        flash('Route added successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the route.', 'danger')

    return redirect(url_for('route_admin.index'))

#update route
@route_bp.route('/edit/<int:route_id>', methods=['POST'])
@admin_required
def edit(route_id):
    route = Route.query.get_or_404(route_id)
    route.origin = request.form.get('origin')
    route.destination = request.form.get('destination')
    distance = request.form.get('distance')
    route.distance = int(distance) if distance else None
    route.via = request.form.get('via')

    try:
        db.session.commit()
        flash('Route updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the route.', 'danger')

    return redirect(url_for('route_admin.index'))

#delete route
@route_bp.route('/delete/<int:route_id>', methods=['POST'])
@admin_required
def delete(route_id):
    route = Route.query.get_or_404(route_id)
    try:
        db.session.delete(route)
        db.session.commit()
        flash('Route deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete route because it is linked with schedules.', 'danger')

    return redirect(url_for('route_admin.index'))