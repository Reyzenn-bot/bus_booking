from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#1. Users table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'user' or 'admin'
    bookings = db.relationship('Booking', backref='user', lazy=True)  # Relationship to Booking

#2. Buses table
class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'AC', 'Non-AC'
    image = db.Column(db.String(255), nullable=True)  # Path to bus image
    logo = db.Column(db.String(255), nullable=True)  # Path to bus logo
    amenities = db.Column(db.String(50), nullable=True)  # Comma-separated list of amenities
    seat = db.Column(db.Integer, nullable=False)  # Total number of seats
    schedules = db.relationship('Schedule', backref='bus', lazy=True)  # Relationship to Schedule

#3. Routes table
class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Integer, nullable=True)  # Distance between origin and destination
    schedules = db.relationship('Schedule', backref='route', lazy=True)  # Relationship to Schedule

#4. Schedules table
class Schedule(db.Model):
    __tablename__='schedules'
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)  # Foreign key to Bus
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    departure_time = db.Column(db.Time, nullable=False)  # e.g., '2023-10-01 10:00:00'
    arrival_time = db.Column(db.Time, nullable=False)  # e.g., '2023-10-01 14:00:00'
    price = db.Column(db.Decimal(10, 2), nullable=False)  # Price for the schedule

#5. Bookings table
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)  # Foreign key to Schedule
    travel_date = db.Column(db.Date, nullable=False)  # Date of travel
    seat_number = db.Column(db.Integer, nullable=False)  # Seat number booked
    passenger_count = db.Column(db.Integer, nullable=False)  # Number of passengers
    ticket_price = db.Column(db.Decimal(10, 2), nullable=False)  # Total ticket price
    service_price = db.Column(db.Decimal(10, 2), nullable=False)  # Service price
    total_price = db.Column(db.Decimal(10, 2), nullable=False)  # Total price (ticket + service)
    booking_status = db.Column(db.String(50), nullable=False, default='confirmed')  # e.g., 'pending', 'confirmed', 'cancelled'
