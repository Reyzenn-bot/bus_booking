from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from models import db, User, Bus, Route, Schedule, Booking

user_bp = Blueprint('user', __name__, url_prefix='/user')

# home page
@user_bp.route('/')
def home():
    routes = Route.query.all()
    schedules = Schedule.query.all()

    selected_bus = None
    select_id = request.args.get('select_id')

    if select_id:
        selected_bus = Schedule.query.get(select_id)
    return render_template('user/index.html', routes=routes, schedules=schedules, selected_bus=selected_bus)

# search bus
@user_bp.route('/search', methods=['GET', 'POST'])
def search():
    routes = Route.query.all()

    origin = request.args.get('origin', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '').strip()

    query = Schedule.query.join(Route)

    if origin:
        query = query.filter(Route.origin == origin)
    if destination:
        query = query.filter(Route.destination == destination)    

    schedules = query.all()
    return render_template('user/search.html', routes=routes, schedules=schedules, origin=origin, destination=destination, date=date)

# user profile
@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('auth.login'))
    
    current_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')

        # បន្ថែមការត្រួតពិនិត្យ ប្រសិនបើ new_email មានតម្លៃ ទើបធ្វើការ Check ស្ទួន
        if new_email and new_email != current_user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                flash('Email is already in use. Please choose a different email.', 'danger')
                return redirect(url_for('user.profile'))
            current_user.email = new_email

        if new_name:
            current_user.name = new_name
        if new_phone:
            current_user.phone = new_phone

        # Update password only if a new password is provided
        new_password = request.form.get('password')
        if new_password:
            current_user.password = generate_password_hash(new_password)

        try:
            db.session.commit()
            session['user_name'] = current_user.name  # Update session new name
            flash('Profile updated successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')

        return redirect(url_for('user.profile'))

    return render_template('user/profile.html', current_user=current_user)