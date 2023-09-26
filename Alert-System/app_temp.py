from flask import Flask, render_template, request
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

app = Flask(__name__)

def send_email(to_email, subject, message):
    # Your Gmail account credentials
    gmail_user = 'moreniraj49@gmail.com'
    gmail_password = 'hjar blzz lbqv ovkg'

    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email message
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your Gmail account
        server.login(gmail_user, gmail_password)

        # Send the email
        server.sendmail(gmail_user, to_email, msg.as_string())

        # Close the SMTP server connection
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        message = request.form['message']
        to_email = request.form['email']

        try:
            # Add a delay to allow WhatsApp Web to load
            time.sleep(10)  # Adjust the delay time as needed

            # Send the WhatsApp message using pywhatkit
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            kit.sendwhatmsg(phone_number, message, int(current_time.split(":")[0]), int(current_time.split(":")[1]) + 1)

            # Send the email
            email_result = send_email(to_email, "WhatsApp Message", message)

            return f"Message sent successfully! {email_result}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
