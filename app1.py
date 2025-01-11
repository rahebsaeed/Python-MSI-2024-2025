from flask import Flask, render_template, request, jsonify
import requests
import time
import uuid

app = Flask(__name__)

# Helper function to calculate current timestamp in milliseconds
def get_current_timestamp_ms():
    return int(time.time() * 1000)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    # Retrieve data from form
    complete_status = request.form.get('complete', 'false').lower() == 'true'
    score_correct = int(request.form.get('score_correct', 0))
    score_incorrect = int(request.form.get('score_incorrect', 0))
    delta_time = int(request.form.get('delta_time', 0))
    number_of_challenges = int(request.form.get('number_of_challenges', 0))
    path_step_media_id = request.form.get('path_step_media_id', 'PATHSTEP_161641920')
    speech_was_enabled = request.form.get('speech_was_enabled', 'true').lower() == 'true'
    user_id = request.form.get('user_id', '4306254')
    session_token = request.form.get(
        'session_token',
        '5592bd0b99199c0d27aff1520acd99c103038cf2f7421769f689cab0f4e5a2f811e67a344d141600'
    )
    lesson_index = int(request.form.get('lesson_index', 0))

    # Generate timestamps and request ID
    updated_at_time = get_current_timestamp_ms()
    request_id = uuid.uuid4()

    # Constant values
    course = "SK-ENG-L4-NA-PE-NA-NA-Y-3"
    unit_index = 0
    path_type = "vocabulary"
    occurrence = 1
    version = 185084

    # Construct XML body for path_step_score
    xml_body_1 = f"""
    <path_step_score>
        <course>{course}</course>
        <unit_index>{unit_index}</unit_index>
        <lesson_index>{lesson_index}</lesson_index>
        <path_type>{path_type}</path_type>
        <occurrence>{occurrence}</occurrence>
        <path_step_media_id>{path_step_media_id}</path_step_media_id>
        <complete>{str(complete_status).lower()}</complete>
        <score_correct>{score_correct}</score_correct>
        <score_incorrect>{score_incorrect}</score_incorrect>
        <score_skipped type="fmcp">0</score_skipped>
        <number_of_challenges>{number_of_challenges}</number_of_challenges>
        <speech_was_enabled>{str(speech_was_enabled).lower()}</speech_was_enabled>
        <version>{version}</version>
        <updated_at>{updated_at_time}</updated_at>
    </path_step_score>
    """

    # Construct XML body for path_score
    xml_body_2 = f"""
    <path_score>
        <course>{course}</course>
        <unit_index>{unit_index}</unit_index>
        <lesson_index>{lesson_index}</lesson_index>
        <path_type>{path_type}</path_type>
        <occurrence>{occurrence}</occurrence>
        <complete>{str(complete_status).lower()}</complete>
        <score_correct>{score_correct}</score_correct>
        <score_incorrect>{score_incorrect}</score_incorrect>
        <score_skipped type="fmcp">0</score_skipped>
        <number_of_challenges>31</number_of_challenges>
        <delta_time>{delta_time}</delta_time>
        <version>{version}</version>
        <updated_at>{updated_at_time}</updated_at>
        <is_lagged_review_path>false</is_lagged_review_path>
    </path_score>
    """

    # Headers
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
        "x-rosettastone-session-token": session_token,
        "x-request-id": str(request_id)
    }

    # URLs
    url_1 = f"https://tracking.rosettastone.com/ee/ce/01dadc90-d74e-4d4f-828c-80af708bd402/users/{user_id}/path_step_scores?course={course}&unit_index={unit_index}&lesson_index={lesson_index}&path_type={path_type}&occurrence={occurrence}&path_step_media_id={path_step_media_id}&_method=put"
    url_2 = f"https://tracking.rosettastone.com/ee/ce/01dadc90-d74e-4d4f-828c-80af708bd402/users/{user_id}/path_scores?course={course}&unit_index={unit_index}&lesson_index={lesson_index}&path_type={path_type}&occurrence={occurrence}&_method=put"

    # Send requests
    response_1 = requests.post(url_1, headers=headers, data=xml_body_1)
    response_2 = requests.post(url_2, headers=headers, data=xml_body_2)

    # Return responses
    return jsonify({
        "request_id": str(request_id),
        "response_1_status": response_1.status_code,
        "response_1_text": response_1.text,
        "response_2_status": response_2.status_code,
        "response_2_text": response_2.text,
    })

if __name__ == '__main__':
    app.run(debug=True)
