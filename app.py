from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message # type: ignore
from config import Config

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Database and Mail
db = SQLAlchemy(app)
mail = Mail(app)

# Define Appointment Model
class AppointmentDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# CORS Preflight Handling
@app.route("/api/book-appointment", methods=["OPTIONS"])
def handle_options():
    response = jsonify({"message": "CORS preflight successful"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

# API: Book an Appointment
@app.route("/api/book-appointment", methods=["POST"])
def book_appointment():
    data = request.json
    new_appointment = AppointmentDoc(
        name=data["name"],
        age=data["age"],
        email=data["email"],
        problem=data["problem"],
        date=data["date"],
        time=data["time"]
    )
    db.session.add(new_appointment)
    db.session.commit()

    # Send email notification
    doctor_email = "sksk20634@gmail.com"  
    subject = "New Appointment Confirmation"

    message_body = f"""
    Hello {data["name"]},
    
    Your appointment has been booked successfully.
    
    Details:
    - Age: {data["age"]}
    - Problem: {data["problem"]}
    - Date: {data["date"]}
    - Time: {data["time"]}

    Regards,
    Clinic Team
    """

    # Send email to patient
    msg_patient = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=[data["email"]])
    msg_patient.body = message_body
    mail.send(msg_patient)

    # Send email to doctor
    msg_doctor = Message(f"New Appointment - {data['name']}", sender=app.config["MAIL_USERNAME"], recipients=[doctor_email])
    msg_doctor.body = f"New appointment booked:\n\n{message_body}"
    mail.send(msg_doctor)

    return jsonify({"message": "Appointment booked successfully"}), 201

# API: Fetch All Appointments
@app.route("/api/appointments", methods=["GET"])
def get_appointments():
    appointments = AppointmentDoc.query.all()
    appointment_list = [{
        "id": a.id,
        "name": a.name,
        "age": a.age,
        "email": a.email,
        "problem": a.problem,
        "date": a.date,
        "time": a.time
    } for a in appointments]
    
    return jsonify(appointment_list)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
