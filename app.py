from flask import Flask, render_template, request, redirect, url_for
from connect import connectDB
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.bus import bus_bp
from routes.route import route_bp
from routes.schedule import schedule_bp
from routes.booking import booking_bp
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bus_bp)
app.register_blueprint(route_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(booking_bp)


if __name__ == "__main__":
    app.run(debug=True)