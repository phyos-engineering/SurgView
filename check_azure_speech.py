import azure_speech
import json

mic = azure_speech.SpeechEngine()

# Play with command SELECT X AND SEND TO Y
print("Check Activation Word - SAY ACTIVATION WORD: PHYPAD")
if mic.recognize_keyword():
    print("CHECK SUCCESSFUL")

print("Check Intent Recognition - SAY ACTIVATION WORD: PHYPAD")
if mic.recognize_keyword():
    print("Say: Press Button X")
    result = mic.recognize_intent()
    json_result = json.loads(result)
    print(json_result)
    print("CHECK SUCCESSFUL")

print("Check Transcription - SAY ACTIVATION WORD: PHYPAD")
if mic.recognize_keyword():
    print("Say: Press Button X ")
    result = mic.transcribe_speech()
    print(f"Parsed Text: {result}")
exit()
