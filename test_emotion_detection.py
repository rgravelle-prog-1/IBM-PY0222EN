import requests
import json
import unittest
from EmotionDetection.emotion_detection import emotion_predictor


def emotion_predictor(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}
    response = requests.post(url, json=myobj, headers=header)

    if response.status_code == 400:
        return 'unknown'  # Return 'unknown' for errors
    else:
        res = json.loads(response.text)
        emotions = res['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotions, key=emotions.get)
        return dominant_emotion


class TestEmotionDetection(unittest.TestCase):
    def test_joy_statement(self):
        text = "I am glad this happened"
        result = emotion_predictor(text)
        self.assertEqual(result, 'joy')

    def test_anger_statement(self):
        text = "I am really mad about this"
        result = emotion_predictor(text)
        self.assertEqual(result, 'anger')

    def test_disgust_statement(self):
        text = "I feel disgusted just hearing about this"
        result = emotion_predictor(text)
        self.assertEqual(result, 'disgust')

    def test_sadness_statement(self):
        text = "I am so sad about this"
        result = emotion_predictor(text)
        self.assertEqual(result, 'sadness')

    def test_fear_statement(self):
        text = "I am really afraid that this will happen"
        result = emotion_predictor(text)
        self.assertEqual(result, 'fear')


unittest.main()
