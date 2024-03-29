"""
This is a Flask application for emotion analysis.

Author: Robert Gravelle
Date: Ongoing
"""
import json
import logging
import requests

from flask import Flask, render_template, request

# Configure the logging level as needed for pylint I set it to info
logging.basicConfig(level=logging.INFO)

app = Flask("Emotion Analyzer")


def compare_scores(score):
    """
    Compare scores and return the score if not None, else return negative infinity.
    """
    return score if score is not None else float('-inf')


def emotion_detector(text_to_analyze):
    """
    This function performs emotion detection .
    """
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = ('https://sn-watson-emotion.labs.skills.network/'
           'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict')
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    try:
        res = response.json()
        formatted_response = res['emotionPredictions'][0]['emotion']
        dominant_emotion = max(formatted_response, key=lambda x: formatted_response[x])
        formatted_response['dominant_emotion'] = dominant_emotion
    except (json.JSONDecodeError, KeyError) as e:
        print(f"JSON parsing error: {e}")
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    return formatted_response


@app.route("/emotionDetector")
def sent_analyzer():
    """
    Analyzes the input text for emotion.

    Returns: formatted string containing emotion analysis results.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)

    if not isinstance(response, dict):
        logging.info("Invalid response format from emotion predictor: %s", response)
        return "Invalid response format from emotion predictor"

    status_code = response.get('status_code', None)

    if status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    anger_score = response.get('anger', None)
    disgust_score = response.get('disgust', None)
    fear_score = response.get('fear', None)
    joy_score = response.get('joy', None)
    sadness_score = response.get('sadness', None)

    emotion_score = {
        'anger': compare_scores(anger_score),
        'disgust': compare_scores(disgust_score),
        'fear': compare_scores(fear_score),
        'joy': compare_scores(joy_score),
        'sadness': compare_scores(sadness_score)
    }

    dominant = max(emotion_score, key=emotion_score.get)

    if dominant is None:
        logging.info("Invalid text! Please try again.")
        return "Invalid text! Please try again."

    string1 = "Your statement is considered 'anger':"
    string2 = (
        f"{anger_score}, 'disgust' : {disgust_score}, "
        f"'fear': {fear_score}, 'joy': {joy_score}"
    )

    string3 = f"and 'sadness': {sadness_score}. The dominant emotion is {dominant}"

    return f"{string1} {string2} {string3}"


@app.route("/")
def render_index_page():
    """
    Renders the index.html page.

    Returns:Flask render_template in rendered HTML template.
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
