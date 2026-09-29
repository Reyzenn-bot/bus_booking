from flask import Blueprint, render_template

route_bp = Blueprint('route', __name__)

@route_bp.route('/buses')
def list_buses():
    return render_template('admin/routes.html')