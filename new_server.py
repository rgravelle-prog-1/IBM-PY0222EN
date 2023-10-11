from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_predictor

app = Flask("Emotion Analyzer")


@app.route("/emotionDetector")
def sent_analyzer():
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_predictor(text_to_analyze)

    if not isinstance(response, dict):
        print(f"Invalid response format from emotion predictor: {response}")
        return "Invalid response format from emotion predictor"

    anger_score = response.get('anger', 0)
    disgust_score = response.get('disgust', 0)
    fear_score = response.get('fear', 0)
    joy_score = response.get('joy', 0)
    sadness_score = response.get('sadness', 0)

    emotion_score = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
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
