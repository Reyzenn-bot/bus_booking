from flask import Blueprint, render_template

bus_bp = Blueprint('bus', __name__)

@bus_bp.route('/buses')
def list_buses():
    return render_template('admin/buses.html')