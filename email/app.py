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
        sender_name = request.form.get("sender_name", "FSDM Robotics Club")
        sender_email = request.form.get("sender_email", MAIL_USERNAME)
        recipient = request.form.get("recipient")
        cc_email = request.form.get("cc_email")  # Optional CC email
        subject = request.form.get("subject")
        content = request.form.get("content")
        no_reply = request.form.get("no_reply")
        batch_send = request.form.get("batch_send")  # Check if batch sending is selected

        # Validate fields
        if not recipient or not subject or not content:
            flash("All fields are required!", "danger")
            return redirect(url_for('index'))

        try:
            # Split recipient and CC emails
            recipients = [email.strip() for email in recipient.split(',')]
            cc_recipients = [email.strip() for email in cc_email.split(',')] if cc_email else []

            # Establish SMTP connection
            with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
                server.starttls()
                server.login(MAIL_USERNAME, MAIL_PASSWORD)

                if batch_send:
                    # Send all emails in a single batch
                    msg = MIMEMultipart()
                    msg['From'] = f"{sender_name} <{sender_email}>"
                    msg['To'] = ", ".join(recipients)
                    msg['Cc'] = ", ".join(cc_recipients)
                    msg['Subject'] = subject
                    msg.attach(MIMEText(content, 'html'))

                    # Add 'Reply-To' header if No Reply checkbox is checked
                    if no_reply:
                        msg['Reply-To'] = 'no-reply@gmail.com'

                    # Send batch email
                    server.sendmail(sender_email, recipients + cc_recipients, msg.as_string())
                else:
                    # Send emails individually
                    for recipient_email in recipients:
                        msg = MIMEMultipart()
                        msg['From'] = f"{sender_name} <{sender_email}>"
                        msg['To'] = recipient_email
                        msg['Subject'] = subject
                        msg.attach(MIMEText(content, 'html'))

                        if no_reply:
                            msg['Reply-To'] = 'no-reply@gmail.com'

                        server.sendmail(sender_email, [recipient_email] + cc_recipients, msg.as_string())

            # Save email data to JSON
            email_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subject": subject,
                "recipients": recipients,
                "cc_recipients": cc_recipients,
                "no_reply": True if no_reply else False,
                "batch_send": True if batch_send else False,
                "content": content,
            }
            append_to_json(email_data)

            flash("Emails sent successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
