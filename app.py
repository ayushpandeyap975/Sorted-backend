from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__, static_url_path="/assets", static_folder="assets")
CORS(app)

# Email configuration
app.config["MAIL_SERVER"] = "smtp.ethereal.email"  # "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("EMAIL_USER")

mail = Mail(app)


@app.route("/submit-contact", methods=["POST"])
def send_email():
    try:
        data = request.json

        # Extract form data
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        school = data.get("school")
        message = data.get("message")

        # Create email message
        msg = Message(
            subject=f"Contact Form Submission from {name}",
            sender=os.getenv("EMAIL_USER"),
            recipients=[os.getenv("RECIPIENT_EMAIL")],
            html=render_template(
                "contact_email.html",
                name=name,
                email=email,
                phone=phone,
                school=school,
                message=message,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        # Send email
        mail.send(msg)

        return jsonify(
            {"status": "success", "message": "Email sent successfully!"}
        ), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/portfolio_details")
def portfolio_details():
    return render_template("portfolio-details.html")


@app.route("/product_details")
def product_details():
    return render_template("product-details.html")


if __name__ == "__main__":
    app.run(debug=True)
