from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Schedule, Bus, Route
from routes.admin import admin_required
from datetime import datetime

schedule_bp = Blueprint('schedule_admin', __name__, url_prefix='/admin/schedules')

@schedule_bp.route('/')
@admin_required
def index():
    all_schedules = Schedule.query.all()
    all_buses = Bus.query.all()
    all_routes = Route.query.all()
    return render_template('admin/schedules.html', schedules=all_schedules, buses=all_buses, routes=all_routes)

#create schedule
@schedule_bp.route('/add', methods=['POST'])
@admin_required
def add():
    bus_id = request.form.get('bus_id')
    route_id = request.form.get('route_id')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')

    try:
        new_schedule = Schedule(
            bus_id=int(bus_id),
            route_id=int(route_id),
            departure_time=datetime.strptime(departure_time, '%H:%M').time(),
            arrival_time=datetime.strptime(arrival_time, '%H:%M').time(),
            price=float(price)
        )
        db.session.add(new_schedule)
        db.session.commit()
        flash('Schedule added successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the schedule.', 'danger')

    return redirect(url_for('schedule_admin.index'))

# Edit schedule
@schedule_bp.route('/edit/<int:schedule_id>', methods=['POST'])
@admin_required
def edit(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    
    schedule.bus_id = request.form.get('bus_id')
    schedule.route_id = request.form.get('route_id')
    departure_time = request.form.get('departure_time')
    arrival_time = request.form.get('arrival_time')
    price = request.form.get('price')

    try:
        if departure_time:
            schedule.departure_time = datetime.strptime(departure_time, '%H:%M').time()
        if arrival_time:
            schedule.arrival_time = datetime.strptime(arrival_time, '%H:%M').time()
        if price:
            schedule.price = float(price)
            
        db.session.commit()
        flash('Schedule updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the schedule.', 'danger')

    return redirect(url_for('schedule_admin.index'))

#delete schedule
@schedule_bp.route('/delete/<int:schedule_id>', methods=['POST'])
@admin_required
def delete(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    try:
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete schedule because it is linked with bookings.', 'danger')

    return redirect(url_for('schedule_admin.index'))