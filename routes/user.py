from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Bus, Route, Schedule, Booking
user_bp = Blueprint('user', __name__, url_prefix='/user')

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
        return redirect(url_for('auth.login'))  # Redirect to login page if user is not logged in

    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.id.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

#user profile

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page if user is not logged in
    
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

#book_ticket

@user_bp.route('/book_ticket/<int:schedule_id>', methods=['GET', 'POST'])
def book_ticket(schedule_id):
    if 'user_id' not in session:
        flash('Please log in to book a ticket.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to login page if user is not logged in

    schedule = Schedule.query.get(schedule_id)

    booked_seats = Booking.query.filter_by(schedule_id=schedule_id).all()
    booked_seat_numbers = [booking.seat_number for booking in booked_seats]

    if request.method == 'POST':
        selected_seat = request.form.get('seat_number')

        # Check if the selected seat is already booked
        if selected_seat in booked_seat_numbers:
            flash('Selected seat is already booked. Please choose a different seat.', 'danger')
            return redirect(url_for('user.book_ticket', schedule_id=schedule_id))

        # create a new booking instance
        new_booking = Booking(
            user_id=session['user_id'],
            schedule_id=schedule_id,
            seat_number=selected_seat
        )

        passenger_count = 1
        ticket_price = schedule.price
        service_price = 0.50  # Example service price
        total_price = ticket_price + service_price

        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Ticket booked successfully!', 'success')
            return redirect(url_for('user.my_bookings'))  # Redirect to my bookings page after successful booking
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the ticket. Please try again.', 'error')
            return redirect(url_for('user.book_ticket', schedule_id=schedule_id))
    return render_template('user/book_ticket.html', schedule=schedule, booked_seat_numbers=booked_seat_numbers)