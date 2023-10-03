import requests
import json


def emotion_predictor(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=myobj, headers=header)

    return response.text

    if status_code == 200:
        formatted_output = {'anger': None,
                            'disgust': None,
                            'fear': None,
                            'joy': None,
                            'sadness': None,
                            'dominant_emotion': None}

    else:
        res = json.loads(response.text)
        formatted_output = res['emotionPredictions'][0]['emotion']
        dominant_emotion = max(formatted_response, key=lambda x: formatted_response[x])
        formatted_response['dominant_dictionary'] = dominant_emotion

    return formatted_response

