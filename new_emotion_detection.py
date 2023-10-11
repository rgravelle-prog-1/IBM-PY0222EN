import json
import requests


def emotion_predictor(text_to_analyze):
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=myobj, headers=header)
        response.raise_for_status()  # Raises HTTPError for bad responses
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
