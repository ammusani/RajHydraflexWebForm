import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Setup for SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'  # Database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder to store uploaded photos

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

# Initialize database
db.create_all()

@app.route('/')
def home():
    # Generate auto serial number (timestamp)
    serial_number = str(datetime.now().timestamp())
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('form.html', serial_number=serial_number, date=date)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        

        # Get form fields
        company_name = request.form['company_name']
        contact_person = request.form['contact_person']
        designation = request.form['designation']
        whatsapp_number = request.form['whatsapp_number']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        additional_info = request.form['additional_info']

        # Handle photo uploads
        photo1 = request.files['photo1']
        photo2 = request.files['photo2']
        photo3 = request.files['photo3']

        photo1_filename = photo1.filename
        photo2_filename = photo2.filename
        photo3_filename = photo3.filename

        photo1.save(os.path.join(app.config['UPLOAD_FOLDER'], photo1_filename))
        photo2.save(os.path.join(app.config['UPLOAD_FOLDER'], photo2_filename))
        photo3.save(os.path.join(app.config['UPLOAD_FOLDER'], photo3_filename))

        # Save data in the database
        new_entry = Entry(
            serial_number=serial_number,
            date=date,
            photo1=photo1_filename,
            photo2=photo2_filename,
            photo3=photo3_filename,
            name=name,
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

        return redirect(url_for('view_entries'))

@app.route('/view_entries')
def view_entries():
    entries = Entry.query.all()
    return render_template('view_entries.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8092)
