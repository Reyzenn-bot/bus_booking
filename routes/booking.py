from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from datetime import datetime, date
from models import db, Booking, Schedule

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

# 1. Select seat and book ticket
@booking_bp.route('/book/<int:schedule_id>', methods=['GET', 'POST'])
def book_ticket(schedule_id):
    if 'user_id' not in session:
        flash('Please log in to book a ticket.', 'warning')
        return redirect(url_for('auth.login'))

    schedule = Schedule.query.get_or_404(schedule_id)

    travel_date_str = request.args.get('travel_date', '').strip() or request.form.get('travel_date', '').strip()

    booked_seats = []
    if travel_date_str:
        try:
            selected_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            booked_seats = [booking.seat_number for booking in Booking.query.filter_by(schedule_id=schedule_id, travel_date=selected_date).all()]
        except ValueError:
            travel_date_str = ''

    return render_template('user/book_ticket.html', schedule=schedule, booked_seats=booked_seats, travel_date_str=travel_date_str)


# 2. Passenger info route
@booking_bp.route('/schedule/<int:schedule_id>/passenger-info', methods=['POST'])
def passenger_info(schedule_id):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    schedule = Schedule.query.get_or_404(schedule_id)
    travel_date_str = request.form.get('travel_date')
    selected_seats = request.form.getlist('seat_numbers')

    if not travel_date_str or not selected_seats:
        flash('Please select at least one seat/berth and travel date.', 'danger')
        return redirect(url_for('booking.book_ticket', schedule_id=schedule_id))

    try:
        travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid travel date format.', 'danger')
        return redirect(url_for('booking.book_ticket', schedule_id=schedule_id))

    current_booked_seats = [booking.seat_number for booking in Booking.query.filter_by(schedule_id=schedule_id, travel_date=travel_date).all()]
    
    for seat in selected_seats:
        if int(seat) in current_booked_seats:
            flash(f'Seat/Berth {seat} is already booked. Please choose another one.', 'danger')
            return redirect(url_for('booking.book_ticket', schedule_id=schedule_id, travel_date=travel_date_str))

    return render_template('user/passenger_info.html', 
                           schedule=schedule, 
                           travel_date=travel_date_str, 
                           selected_seats=selected_seats)


# 3. Booking summary
@booking_bp.route('/summary', methods=['POST'])
def booking_summary():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    Schedule_id = request.form.get('schedule_id')
    travel_date = request.form.get('travel_date')
    seat_numbers = request.form.getlist('seat_numbers')
    passenger_name = request.form.get('passenger_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone = request.form.get('phone')
    schedule = Schedule.query.get_or_404(Schedule_id)
    num_seats = len(seat_numbers)
    ticket_price_per_seat = float(schedule.price)
    subtotal = ticket_price_per_seat * num_seats
    service_fee = 1.00 * num_seats
    total_price = subtotal + service_fee

    return render_template('user/summary.html',
                           schedule=schedule,
                           travel_date=travel_date,
                           seat_numbers=seat_numbers,
                           passenger_name=passenger_name,
                           age=age,
                           gender=gender,
                           email=email,
                           phone=phone,
                           subtotal=subtotal,
                           service_fee=service_fee,
                           total_price=total_price)


# 4. Booking payment
@booking_bp.route('/payment', methods=['POST'])
def booking_payment():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    schedule_id = request.form.get('schedule_id')
    travel_date = request.form.get('travel_date')
    seat_numbers = request.form.getlist('seat_numbers')
    passenger_name = request.form.get('passenger_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone = request.form.get('phone')
    total_price = request.form.get('total_price')

    schedule = Schedule.query.get_or_404(schedule_id)

    return render_template('user/payment.html',
                           schedule=schedule,
                           travel_date=travel_date,
                           seat_numbers=seat_numbers,
                           passenger_name=passenger_name,
                           age=age,
                           gender=gender,
                           email=email,
                           phone=phone,
                           total_price=total_price)


# 5. Confirm final booking and save to DB
@booking_bp.route('/confirm', methods=['POST'])
def confirm_final_booking():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    schedule_id = request.form.get('schedule_id')
    travel_date_str = request.form.get('travel_date')
    
    if not travel_date_str:
        flash('Travel date is missing.', 'danger')
        return redirect(url_for('user.home'))
        
    travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()
    seat_numbers = request.form.getlist('seat_numbers')
    
    passenger_name = request.form.get('passenger_name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    schedule = Schedule.query.get_or_404(schedule_id)
    unit_price = float(schedule.price) + 1.00  # តម្លៃសំបុត្រ + សេវា $1

    created_bookings = []

    try:
        # Loop រក្សាទុកកៅអីនីមួយៗចូលក្នុង Table Booking (Save each seat to database)
        for seat in seat_numbers:
            new_booking = Booking(
                user_id=user_id,
                schedule_id=schedule.id,
                travel_date=travel_date,
                seat_number=int(seat),
                passenger_count=1,
                ticket_price=schedule.price,
                service_fee=1.00,
                total_price=unit_price,
                booking_status='confirmed',
                passenger_name=passenger_name,
                age=int(age) if age else None,
                gender=gender,
                email=email,
                phone=phone
            )
            db.session.add(new_booking)
            created_bookings.append(new_booking)
        
        # រក្សាទុកទិន្នន័យចូល Database ជាផ្លូវការ (Commit to database)
        db.session.commit()
        
        if not created_bookings:
            flash('No seats selected.', 'danger')
            return redirect(url_for('user.home'))

        # បង្កើត Ticket Reference Code
        ticket_ref = f"TICK-{created_bookings[0].id}-{datetime.now().strftime('%M%S')}"

        # 📌 គណនាពិនិត្យមើលថាតើ travel_date ហួសថ្ងៃបច្ចុប្បន្នហើយឬยัง
        today_str = date.today().strftime('%Y-%m-%d')
        is_expired = travel_date_str < today_str if travel_date_str else False

        return render_template('user/eTicket.html',
                               bookings=created_bookings,
                               schedule=schedule,
                               travel_date=travel_date_str,
                               passenger_name=passenger_name,
                               phone=phone,
                               ticket_ref=ticket_ref,
                               is_expired=is_expired)  # <--- 📌 បញ្ជូន is_expired ទៅទីនេះ

    except Exception as e:
        db.session.rollback()
        print("===== BOOKING ERROR DEBUG =====")
        print(str(e))
        print("===============================")
        
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('user.home'))


# 6. View My Bookings grouped by session for my_bookings.html compatibility)
@booking_bp.route('/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    raw_bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()

    grouped_bookings = []
    seen_groups = set()
    today_str = date.today().strftime('%Y-%m-%d')  # យកថ្ងៃនេះជា String '2026-10-19'

    for b in raw_bookings:
        time_key = b.created_at.strftime('%Y-%m-%d %H:%M') if b.created_at else ''
        group_key = f"{b.schedule_id}_{b.travel_date}_{time_key}"

        if group_key not in seen_groups:
            seen_groups.add(group_key)
            
            related_seats = [
                item for item in raw_bookings 
                if f"{item.schedule_id}_{item.travel_date}_" + (item.created_at.strftime('%Y-%m-%d %H:%M') if item.created_at else '') == group_key
            ]
            
            seat_list = [str(item.seat_number) for item in related_seats]
            total_group_price = sum(float(item.total_price) for item in related_seats)
            first_booking = related_seats[0]

            # 📌 សម្រួលការ Check Expired ឱ្យស្រួល៖ ប្រែក្លាយ travel_date ទៅជា String YYYY-MM-DD
            t_date = str(first_booking.travel_date) if first_booking.travel_date else ''
            
            # បើ t_date (ឧ. '2026-10-18') < today_str ('2026-10-19') វានឹងចេញ True (Expired!)
            is_expired = t_date < today_str if t_date else False

            grouped_bookings.append({
                'main_booking': first_booking,
                'seats_display': ", ".join(seat_list),
                'total_seats_count': len(related_seats),
                'total_group_price': total_group_price,
                'booking_ids': [item.id for item in related_seats],
                'is_expired': is_expired  # <--- True/False ត្រឹមត្រូវ
            })

    return render_template('user/my_bookings.html', grouped_bookings=grouped_bookings)


# 7. View group eTicket
@booking_bp.route('/eticket_group/<group_ids>')
def view_group_eticket(group_ids):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    id_list = [int(i) for i in group_ids.split(',') if i.isdigit()]
    bookings = Booking.query.filter(Booking.id.in_(id_list), Booking.user_id == session['user_id']).all()

    if not bookings:
        flash('Booking not found.', 'danger')
        return redirect(url_for('booking.my_bookings'))

    first_b = bookings[0]
    schedule = first_b.schedule
    travel_date_str = first_b.travel_date.strftime('%Y-%m-%d') if first_b.travel_date else ''

    # 📌 គណនាមើលថាតើ travel_date ហួសថ្ងៃបច្ចុប្បន្នហើយឬยัง
    today_str = date.today().strftime('%Y-%m-%d')
    is_expired = travel_date_str < today_str if travel_date_str else False

    return render_template('user/eTicket.html',
                           bookings=bookings,
                           schedule=schedule,
                           travel_date=travel_date_str,
                           passenger_name=first_b.passenger_name,
                           phone=first_b.phone,
                           is_expired=is_expired)

# 8. Delete group booking
@booking_bp.route('/delete_group/<group_ids>', methods=['POST'])
def delete_group_booking(group_ids):
    if 'user_id' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('auth.login'))

    id_list = [int(i) for i in group_ids.split(',') if i.isdigit()]
    bookings = Booking.query.filter(Booking.id.in_(id_list), Booking.user_id == session['user_id']).all()

    try:
        for b in bookings:
            db.session.delete(b)
        db.session.commit()
        flash('Booking deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting booking.', 'danger')

    return redirect(url_for('booking.my_bookings'))