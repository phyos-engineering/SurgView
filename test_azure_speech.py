import azure_speech
import json


mic = azure_speech.SpeechEngine()
if mic.recognize_keyword():
    result = mic.recognize_intent()
    json_result = json.loads(result)
    print(json_result)
exit()
