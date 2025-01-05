from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
from flask_cors import CORS  # Import CORS from flask_cors

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    try:
        # Get the JSON data from the request body
        data = request.get_json()
        
        # Extract minutes and seconds from the received JSON data
        minutes = int(data['minutes'])
        seconds = int(data['seconds'])
        
        # Calculate duration in milliseconds
        duration_ms = (minutes * 60 + seconds) * 1000
        
        # Get the current time for endTimestamp
        end_timestamp = datetime.utcnow().isoformat() + "Z"  # ISO format with 'Z' for UTC time
        
        # Prepare the GraphQL mutation request body (AddUsageOverhead)
        graphql_body = {
            "operationName": "AddUsageOverhead",
            "variables": {
                "messages": [{
                    "id": "85a3b7eb-538e-4d85-a503-a24214462ea1",  # Example ID
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                    "learningContext": "0b1dcc54dba29230766844be8f1f228c",  # Example learning context ID
                    "durationMs": duration_ms,
                    "endTimestamp": end_timestamp
                }]
            },
            "query": """
                mutation AddUsageOverhead($messages: [UsageOverheadMessage!]!) {
                    usageOverhead(messages: $messages)
                }
            """
        }

        # Define headers for the request
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7,fr;q=0.6",
            "authorization": "Bearer 81b643ef-514e-4c66-bdbc-ed70d08944c4",  # Example Bearer token
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

        # Send the POST request (AddUsageOverhead)
        url = "https://gaia-server.rosettastone.com/graphql"
        response = requests.post(url, json=graphql_body, headers=headers)

        # Process and return the response
        return jsonify({
            "status_1": response.status_code,
            "response_1": response.json(),
        })

    except Exception as e:
        # If there's an error, return a response with the error message
        return jsonify({
            "status_1": "Error",
            "response_1": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
