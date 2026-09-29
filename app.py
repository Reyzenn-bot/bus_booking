from flask import Flask, render_template, request, redirect, url_for
from connect import connectDB
from routes.admin import admin_bp
from routes.user import user_bp
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.run(debug=True)