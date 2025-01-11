from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
from flask_cors import CORS
import json
import uuid

# Suppress the InsecureRequestWarning (Not for production)
requests.packages.urllib3.disable_warnings()

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

        # Extract duration from received JSON
        minutes = int(data.get('minutes', 0))
        seconds = int(data.get('seconds', 0))
        duration_ms = (minutes * 60 + seconds) * 1000

        # Generate unique UUIDs
        activity_attempt_id = str(uuid.uuid4())
        activity_step_attempt_id_1 = str(uuid.uuid4())
        activity_step_attempt_id_2 = str(uuid.uuid4())

        # Set the common timestamp
        end_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"

        # Define common headers
        headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7,fr;q=0.6",
            "authorization": "Bearer 352ffbe4-b455-439d-a28c-a089ab1df7de",
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

        # Prepare GraphQL request bodies
        graphql_body_1 = {
            "operationName": "AddProgress",
            "variables": {
                "userId": "a5c359e9-22fc-4507-a0e9-032f336c216b",
                "messages": [
                    {
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                        "courseId": "bc84c0820f1d9bde0b4f0293c1a6e1a5",
                        "sequenceId": "22e31574-cd98-46a7-8b5e-9185d4dc414d",
                        "version": 2,
                        "activityId": "aa48863dc7200b33f847a7b777a1d35c",
                        "activityAttemptId": activity_attempt_id,
                        "activityStepId": "2323a0bf-1a57-443b-b73a-feb7d3541f0d",
                        "activityStepAttemptId": activity_step_attempt_id_1,
                        "answers": [{"answer": "SS:d7031cad-5b09-4e3c-8ae3-621df90beac7:1:false", "correct": True}],
                        "score": 1,
                        "skip": False,
                        "durationMs": duration_ms,
                        "endTimestamp": end_timestamp
                    }
                ]
            },
            "query": """
                mutation AddProgress($userId: String, $messages: [ProgressMessage!]!) {
                  progress(userId: $userId, messages: $messages) {
                    id
                    __typename
                  }
                }
            """
        }

        graphql_body_2 = {
            "operationName": "AddProgress",
            "variables": {
                "userId": "a5c359e9-22fc-4507-a0e9-032f336c216b",
                "messages": [
                    {
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                        "courseId": "bc84c0820f1d9bde0b4f0293c1a6e1a5",
                        "sequenceId": "22e31574-cd98-46a7-8b5e-9185d4dc414d",
                        "version": 2,
                        "activityId": "aa48863dc7200b33f847a7b777a1d35c",
                        "activityAttemptId": activity_attempt_id,
                        "activityStepId": "2323a0bf-1a57-443b-b73a-feb7d3541f0d",
                        "activityStepAttemptId": activity_step_attempt_id_2,
                        "answers": [{"answer": "SS:14ef0e76-fbbf-4964-b20d-426ae8b1d3ad:1:false", "correct": True}],
                        "score": 0,
                        "skip": False,
                        "durationMs": 1,
                        "endTimestamp": end_timestamp
                    }
                ]
            },
            "query": """
                mutation AddProgress($userId: String, $messages: [ProgressMessage!]!) {
                  progress(userId: $userId, messages: $messages) {
                    id
                    __typename
                  }
                }
            """
        }

        # Send the POST requests
        url = "https://gaia-server.rosettastone.com/graphql"
        response_1 = requests.post(url, json=graphql_body_1, headers=headers, verify=False)
        response_2 = requests.post(url, json=graphql_body_2, headers=headers, verify=False)

        # Return the response
        return jsonify({
            "status_1": response_1.status_code,
            "response_1": response_1.json(),
            "status_2": response_2.status_code,
            "response_2": response_2.json()
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
