from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Analyzer")


def compare_scores(score):
    return score if score is not None else float('-inf')


@app.route("/emotionDetector")
def sent_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)

    if not isinstance(response, dict):
        app.logger.error(f"Invalid response format from emotion predictor: {response}")
        return "Invalid response format from emotion predictor"

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
        return "Invalid text! Please try again."

    string1 = f"Your statement is considered 'anger':"
    string2 = f"{anger_score}, 'disgust' : {disgust_score}, 'fear': {fear_score}, 'joy': {joy_score}"
    string3 = f"and 'sadness': {sadness_score}. The dominant emotion is {dominant}"

    return f"{string1} {string2} {string3}"


@app.route("/")
def render_index_page():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
