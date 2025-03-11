from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)  # Allow frontend to call API

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://AppointmentDoc_owner:npg_msJxbhi8jq9z@ep-young-shape-a8y2y3ci-pooler.eastus2.azure.neon.tech/AppointmentDoc?sslmode=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Email configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "sksk20634@gmail.com"  
app.config["MAIL_PASSWORD"] = "zwuxrjylataldqfa"    

db = SQLAlchemy(app)
mail = Mail(app)

# Define the Appointment model
class AppointmentDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

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
    doctor_email = "sksk20634@gmail.com"  # Replace with the doctor's email
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
    msg_patient = Message(subject, sender="sksk20634@gmail.com", recipients=[data["email"]])
    msg_patient.body = message_body
    mail.send(msg_patient)

    # Send email to doctor
    msg_doctor = Message(f"New Appointment - {data['name']}", sender="sksk20634@gmail.com", recipients=[doctor_email])
    msg_doctor.body = f"New appointment booked:\n\n{message_body}"
    mail.send(msg_doctor)

    return jsonify({"message": "Appointment booked successfully"}), 201

# New API to fetch all appointments
@app.route("/api/appointments", methods=["GET"])
def get_appointments():
    appointments = AppointmentDoc.query.all()
    appointment_list = [{
        "id": a.id,
        "name": a.name,
        "age":a.age,
        "email": a.email,
        "problem": a.problem,
        "date": a.date,
        "time": a.time
    } for a in appointments]
    
    return jsonify(appointment_list)

if __name__ == "__main__":
    app.run(debug=True)
