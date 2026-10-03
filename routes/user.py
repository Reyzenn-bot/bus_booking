from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Bus, Route, Schedule, Booking
user_bp = Blueprint('user', __name__)

# home page

@user_bp.route('/')
def home():
    routes = Route.query.all()
    schedules = Schedule.query.all()

    # ប្រសិនបើ User ចុចលើប៊ូតុង "View Seats" (មាន select_id)
    selected_bus = None
    select_id = request.args.get('select_id')

    if select_id:
        selected_bus = Schedule.query.get(select_id)
    return render_template('index.html', routes=routes, schedules=schedules, selected_bus=selected_bus)

#search bus

@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    routes = Route.query.all()

    origin = request.args.get('origin', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '').strip()

    query = Schedule.query.join(Route)

    if origin:
        query = query.filter(Route.origin==origin)
    if destination:
        query = query.filter(Route.destination==destination)    

    schedules = query.all()
    return render_template('search.html', routes=routes, schedules=schedules, origin=origin, destination=destination, date=date)

#my bookings

@user_bp.route('/my_bookings', methods=['GET'])
def my_bookings():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your bookings.', 'warning')
        return redirect(url_for('user.login'))  # Redirect to login page if user is not logged in

    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.id.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

#user profile

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('user.login'))  # Redirect to login page if user is not logged in
    
    current_user = User.query.get(user_id)

    if request.method == 'POST':
        # Update user profile
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        current_user.phone = request.form.get('phone')

        # Update password if provided
        new_password = request.form.get('password')
        if new_password:
            current_user.password = generate_password_hash(new_password)

        try:
            db.session.commit()
            flash('Profile updated successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'error')

        return redirect(url_for('user.profile'))  # Redirect to home page after updating profile

    return render_template('profile.html', current_user=current_user)