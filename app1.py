from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

# Helper function to calculate delta time in milliseconds
def get_current_timestamp_ms():
    return int(time.time() * 1000)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    # Get data from form
    minutes_1 = int(request.form.get('minutes_1', 0))  # Get minutes
    seconds_1 = int(request.form.get('seconds_1', 0))  # Get seconds

    # Convert to delta_time in milliseconds
    delta_time = (minutes_1 * 60 + seconds_1) * 1000  # Convert to milliseconds

    # Construct XML body based on the data received
    xml_body_1 = f"""
    <path_score>
        <course>SK-FRA-L2-NA-PE-NA-NA-Y-3</course>
        <unit_index>0</unit_index>
        <lesson_index>3</lesson_index>
        <path_type>reading</path_type>
        <occurrence>1</occurrence>
        <complete>false</complete>
        <score_correct>13</score_correct>
        <score_incorrect>1</score_incorrect>
        <score_skipped type="fmcp">0</score_skipped>
        <number_of_challenges>42</number_of_challenges>
        <delta_time>{delta_time}</delta_time>
        <version>184931</version>
        <updated_at>{get_current_timestamp_ms()}</updated_at>
        <is_lagged_review_path>false</is_lagged_review_path>
    </path_score>
    """

    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7,fr;q=0.6",
        "cache-control": "no-cache",
        "content-type": "text/xml",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-rosettastone-app-version": "ZoomCourse/11.11.3",
        "x-rosettastone-protocol-version": "8",
        "x-rosettastone-session-token": "4abce46da621291851ea966b8441e46721e1ab513c541c53a66a5a71df2757ecc67a235df36df7f6"
    }

    url_1 = "https://tracking.rosettastone.com/ee/ce/01dadc90-d74e-4d4f-828c-80af708bd402/users/4306391/path_scores?course=SK-FRA-L2-NA-PE-NA-NA-Y-3&unit_index=0&lesson_index=3&path_type=reading&occurrence=1&_method=put"

    # Send request
    response_1 = requests.post(url_1, headers=headers, data=xml_body_1)

    # Return responses
    return jsonify({
        "response_1_status": response_1.status_code,
        "response_1_text": response_1.text,
    })

if __name__ == '__main__':
    app.run(debug=True)
