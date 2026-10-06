from flask import Flask, render_template, request, redirect, url_for
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.bus import bus_bp
from routes.route import route_bp
from routes.schedule import schedule_bp
from routes.booking import booking_bp
from routes.user import user_bp
from models import db
import webbrowser
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bus_booking_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bus_bp)
app.register_blueprint(route_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(user_bp)

@app.route('/')
def root():
    return redirect(url_for('user.home'))

with app.app_context():
    db.create_all()  # Create tables if they don't exist

if __name__ == "__main__":
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True, port=5000)  