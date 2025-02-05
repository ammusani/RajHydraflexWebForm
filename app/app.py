import os
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time 

app = Flask(__name__)

# Setup for SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'  # Database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder to store uploaded photos
app.config['SECRET_KEY'] = 'rajHydroFlex'
db = SQLAlchemy(app)

app.app_context().push()

# Define the database model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    photo1 = db.Column(db.String(100))
    photo2 = db.Column(db.String(100))
    photo3 = db.Column(db.String(100))
    company_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(200))
    designation = db.Column(db.String(100))
    whatsapp_number = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.String(500))
    additional_info = db.Column(db.String(500))

    # def __repr__(self):
    #     return f'<Entry {self.serial_number} {self.date} {}>'



# Initialize database
db.create_all()

@app.route('/form')
def home():
    # Generate auto serial number (timestamp)
    serial_number = str(datetime.now().strftime("%m%d%H%M%S%f"))
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('form.html', serial_number=serial_number, date=date)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':         
        # Get form fields
        id = db.Column(db.Integer, primary_key=True)
        serial_number = request.form['serial_number']
        date = request.form['date']
        company_name = request.form['company_name']
        contact_person = request.form['contact_person']
        designation = request.form['designation']
        whatsapp_number = request.form['whatsapp_number']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        additional_info = request.form['additional_info']

        photo1_filename = None
        photo2_filename = None
        photo3_filename = None

        # Handle photo uploads if present
        if 'photo1' in request.files:
            photo1 = request.files['photo1']
            print(photo1)
            if photo1:  # Make sure the file is valid
                photo1_filename = serial_number + '_photo1'
                photo1.save(os.path.join(app.config['UPLOAD_FOLDER'], photo1_filename))

        if 'photo2' in request.files:
            photo2 = request.files['photo2']
            if photo2:  # Make sure the file is valid
                photo2_filename = serial_number + '_photo2'
                photo2.save(os.path.join(app.config['UPLOAD_FOLDER'], photo2_filename))

        if 'photo3' in request.files:
            photo3 = request.files['photo3']
            if photo3:  # Make sure the file is valid
                photo3_filename = serial_number + '_photo3'
                photo3.save(os.path.join(app.config['UPLOAD_FOLDER'], photo3_filename))

        # Save data in the database
        new_entry = Entry(
            serial_number=serial_number,
            date=date,
            photo1=photo1_filename,
            photo2=photo2_filename,
            photo3=photo3_filename,
            company_name=company_name,
            contact_person=contact_person,
            designation=designation,
            whatsapp_number=whatsapp_number,
            phone_number=phone_number,
            email=email,
            address=address,
            additional_info=additional_info
        )

        db.session.add(new_entry)
        db.session.commit()
        return Response("OK", status=200)

@app.route('/view_entries')
def view_entries():
    entries = Entry.query.all()
    return render_template('view_entries.html', entries=entries)

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
