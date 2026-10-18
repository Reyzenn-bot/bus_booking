from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Booking, Bus, Schedule, Route
from sqlalchemy import func
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# មុខងារពិនិត្យសិទ្ធិ Admin (Admin Route Guard)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            flash('Access denied! Admin privileges required.', 'danger')
            return redirect(url_for('user.home'))
        
        return f(*args, **kwargs)
    return decorated_function

# 1. Admin Dashboard
@admin_bp.route('/')
@admin_required
def dashboard():
    total_bookings = Booking.query.count()
    total_buses = Bus.query.count()
    total_routes = Route.query.count()
    total_users = User.query.count()
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           total_bookings=total_bookings,
                           total_buses=total_buses,
                           total_routes=total_routes,
                           total_users=total_users,
                           recent_bookings=recent_bookings)

# 2. Bookings Management
@admin_bp.route('/bookings')
@admin_required
def bookings():
    all_bookings = Booking.query.order_by(Booking.id.desc()).all()
    return render_template('admin/bookings.html', bookings=all_bookings)

# 3. Reject Booking by Admin
@admin_bp.route('/bookings/reject/<int:booking_id>', methods=['POST'])
@admin_required
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    try:
        booking.booking_status = 'Rejected'
        db.session.commit()
        flash(f'Booking #{booking.id} has been rejected.', 'warning')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while rejecting the booking.', 'danger')
    return redirect(url_for('admin.bookings'))

# 4. Delete Booking by Admin
@admin_bp.route('/bookings/delete/<int:booking_id>', methods=['POST'])
@admin_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    try:
        db.session.delete(booking)
        db.session.commit()
        flash(f'Booking #{booking_id} has been completely deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the booking.', 'danger')
    return redirect(url_for('admin.bookings'))

# 5. Passengers Management 
@admin_bp.route('/passengers')
@admin_required
def passengers():
    all_passengers = Booking.query.filter(Booking.passenger_name.isnot(None)).order_by(Booking.id.desc()).all()
    return render_template('admin/passengers.html', passengers=all_passengers)

# 6. Delete Passenger by Admin
@admin_bp.route('/passengers/delete/<int:passenger_id>', methods=['POST'])
@admin_required
def delete_passenger(passenger_id):
    passenger_booking = Booking.query.get_or_404(passenger_id)
    try:
        db.session.delete(passenger_booking)
        db.session.commit()
        flash('Passenger record has been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting passenger record.', 'danger')
    return redirect(url_for('admin.passengers'))

# 7. Users & Roles Management
@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/users/edit/<int:user_id>', methods=['POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.role = request.form.get('role')
    try:
        db.session.commit()
        flash('User role updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating user role.', 'danger')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Cannot delete user with active bookings.', 'danger')
    return redirect(url_for('admin.users'))

# 8. Reports & Statistics
@admin_bp.route('/reports')
@admin_required
def reports():
    all_bookings = Booking.query.all()
    total_revenue = db.session.query(func.sum(Booking.total_price)).scalar() or 0
    total_oneway = Booking.query.filter_by(trip_type='oneway').count()
    total_roundtrip = Booking.query.filter_by(trip_type='roundtrip').count()

    return render_template('admin/report.html', 
                           bookings=all_bookings,
                           total_revenue=total_revenue,
                           total_oneway=total_oneway,
                           total_roundtrip=total_roundtrip)

# 9. Dev Login Shortcut
@admin_bp.route('/dev-login')
def dev_login():
    from werkzeug.security import generate_password_hash
    
    admin_user = User.query.filter_by(role='admin').first()
    
    if not admin_user:
        admin_user = User(
            name='System Admin',
            email='admin@busbooking.com',
            password=generate_password_hash('admin123'),
            phone='012345678',
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
    
    session['user_id'] = admin_user.id
    flash('Logged in as Admin successfully!', 'success')
    return redirect(url_for('admin.dashboard'))