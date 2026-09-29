from flask import Blueprint, render_template

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/schedules')
def list_schedules():
    return render_template('admin/schedules.html')