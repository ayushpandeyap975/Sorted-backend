from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        
        # Extract form data
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        school = data.get('school')
        message = data.get('message')
        
        # Create email message
        msg = Message(
            subject=f"Contact Form Submission from {name}",
            sender=os.getenv('EMAIL_USER'),
            recipients=[os.getenv('RECIPIENT_EMAIL')],
            body=f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            School: {school}
            
            Message:
            {message}
            """
        )
        
        # Send email
        mail.send(msg)
        
        return jsonify({
            'status': 'success',
            'message': 'Email sent successfully!'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 