from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from datetime import datetime
from models import db, Booking, Schedule

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

# select seat and book ticket
@booking_bp.route('/book/<int:schedule_id>', methods=['GET', 'POST'])
def book_ticket(schedule_id):
    if 'user_id' not in session:
        flash('Please log in to book a ticket.', 'warning')
        return redirect(url_for('auth.login'))

    schedule = Schedule.query.get_or_404(schedule_id)

    # ទទួលបាន String នៃថ្ងៃខែធ្វើដំណើរពី Query Params (GET) ឬ Form (POST)
    travel_date_str = request.args.get('travel_date', '').strip() or request.form.get('travel_date', '').strip()

    booked_seats = []
    if travel_date_str:
        try:
            selected_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            booked_seats = [booking.seat_number for booking in Booking.query.filter_by(schedule_id=schedule_id, travel_date=selected_date).all()]
        except ValueError:
            travel_date_str = ''  # Reset ប្រសិនបើទម្រង់ថ្ងៃខែខុស

    if request.method == 'POST':
        selected_seat = request.form.get('seat_number')
        travel_date_input = request.form.get('travel_date')

        if not selected_seat or not travel_date_input:
            flash('Please select a seat and travel date.', 'danger')
            return redirect(url_for('booking.book_ticket', schedule_id=schedule_id))

        try:
            seat_num = int(selected_seat)
            travel_date = datetime.strptime(travel_date_input, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid seat number or travel date format.', 'danger')
            return redirect(url_for('booking.book_ticket', schedule_id=schedule_id))

        current_booked_seats = [booking.seat_number for booking in Booking.query.filter_by(schedule_id=schedule_id, travel_date=travel_date).all()]
        if seat_num in current_booked_seats:
            flash('Selected seat is already booked. Please choose another seat.', 'danger')
            return redirect(url_for('booking.book_ticket', schedule_id=schedule_id, travel_date=travel_date_input))

        # គណនាថ្លៃសំបុត្រ
        ticket_price = float(schedule.price)
        service_fee = 1.00
        total_price = ticket_price + service_fee

        new_booking = Booking(
            user_id=session['user_id'],
            schedule_id=schedule_id,
            travel_date=travel_date,
            seat_number=seat_num,
            passenger_count=1,
            ticket_price=ticket_price,
            service_price=service_fee,
            total_price=total_price,
            booking_status='Confirmed'
        )

        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Ticket booked successfully!', 'success')
            return redirect(url_for('booking.my_bookings'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the ticket. Please try again.', 'danger')
            return redirect(url_for('booking.book_ticket', schedule_id=schedule_id, travel_date=travel_date_input))

    # Pass travel_date_str ទៅឱ្យ Frontend ដើម្បបើកឱ្យ User ជ្រើសរើសកៅអីបាន
    return render_template('user/book_ticket.html', schedule=schedule, booked_seats=booked_seats, travel_date_str=travel_date_str)

# view my bookings
@booking_bp.route('/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please log in to view your bookings.', 'warning')
        return redirect(url_for('auth.login'))

    user_bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.id.desc()).all()
    return render_template('user/my_bookings.html', bookings=user_bookings)