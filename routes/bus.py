from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Bus
from routes.admin import admin_required

bus_bp = Blueprint('bus_admin', __name__, url_prefix='/admin/buses')

@bus_bp.route('/')
@admin_required
def index():
    all_buses = Bus.query.all()
    return render_template('admin/buses.html', buses=all_buses)

#create bus
@bus_bp.route('/add', methods=['POST'])
@admin_required
def add():
    name = request.form.get('name')
    type = request.form.get('type')
    image = request.form.get('image')
    logo = request.form.get('logo')
    amenities = request.form.get('amenities')
    seat = request.form.get('seat')
    
    try:
        new_bus = Bus(name=name, type=type, image=image, logo=logo, amenities=amenities, seat=seat)
        db.session.add(new_bus)
        db.session.commit()
        flash('Bus added successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the bus.', 'danger')

    return redirect(url_for('bus_admin.index'))

#update bus
@bus_bp.route('/edit/<int:bus_id>', methods=['POST'])
@admin_required
def edit(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    bus.name = request.form.get('name')
    bus.type = request.form.get('type')
    bus.image = request.form.get('image')
    bus.logo = request.form.get('logo')
    bus.amenities = request.form.get('amenities')
    bus.seat = int(request.form.get('seat'))

    try:
        db.session.commit()
        flash('Bus updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the bus.', 'danger')

    return redirect(url_for('bus_admin.index'))

#delete bus
@bus_bp.route('/delete/<int:bus_id>', methods=['POST'])
@admin_required
def delete(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    try:
        db.session.delete(bus)
        db.session.commit()
        flash('Bus deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete bus because it is linked with schedules.', 'danger')

    return redirect(url_for('bus_admin.index'))