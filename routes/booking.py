from flask import Blueprint, render_template

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/bookings')
def list_bookings():
    return render_template('admin/bookings.html')