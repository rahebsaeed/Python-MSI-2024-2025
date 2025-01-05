from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime  # Import datetime module to capture timestamp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Email Configuration
MAIL_USERNAME = 'raheebareef@gmail.com'  # Replace with your email
MAIL_PASSWORD = 'euexweqlclsxiquq'  # Replace with your password
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587

def append_to_json(data, file_name='email_data.json'):
    """Append the given data to a JSON file."""
    try:
        # Read the existing data from the JSON file
        try:
            with open(file_name, 'r') as file:
                email_data = json.load(file)
        except FileNotFoundError:
            email_data = []  # If file doesn't exist, start with an empty list

        # Append the new email data with the timestamp
        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_data.append(data)

        # Write the updated list back to the JSON file
        with open(file_name, 'w') as file:
            json.dump(email_data, file, indent=4)

    except Exception as e:
        print(f"Error writing to file: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract form data from request
        sender_name = request.form.get("sender_name", "FSDM Robotics Club")  # Default to FSDM Robotics Club
        sender_email = request.form.get("sender_email", MAIL_USERNAME)  # Default to the configured email
        recipient = request.form.get("recipient")  # This should match the HTML form's name attribute
        subject = request.form.get("subject")  # This should match the HTML form's name attribute
        content = request.form.get("content")  # This should match the HTML form's name attribute
        no_reply = request.form.get("no_reply")  # Check if the No Reply checkbox is checked

        # Validate fields
        if not recipient or not subject or not content:
            flash("All fields are required!", "danger")
            return redirect(url_for('index'))  # Redirect back to the form

        try:
            # Split recipient emails if multiple
            recipients = [email.strip() for email in recipient.split(',')]

            # Establish the SMTP connection and send the email
            with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
                server.starttls()  # Secure the connection
                server.login(MAIL_USERNAME, MAIL_PASSWORD)  # Login to the email account

                for recipient_email in recipients:
                    # Create the email message
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{sender_email}>"
                    msg['To'] = recipient_email  # Set the To field to the current recipient's email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(content, 'html'))  # Attach the HTML content

                    # Add 'Reply-To' header if No Reply checkbox is checked
                    if no_reply:
                        msg['Reply-To'] = 'no-reply@example.com'  # Set an invalid email for no reply

                    # Send the email to the individual recipient
                    server.sendmail(sender_email, recipient_email, msg.as_string())  # Send email to each recipient separately

            # Prepare the data to be saved in JSON
            email_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "subject": subject,
                "recipients": recipients,
                "no_reply": True if no_reply else False,
                "content": content,
            }

            # Append the email data to the JSON file
            append_to_json(email_data)

            flash("Emails sent successfully to each recipient!", "success")
            return redirect(url_for('index'))  # Redirect back to the form
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('index'))  # Redirect back to the form

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
