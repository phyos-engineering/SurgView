#include <iostream> 
#include <speechapi_cxx.h>
#include <string>
#include "pybind11/pybind11.h"

namespace py = pybind11;
using namespace std;
using namespace Microsoft::CognitiveServices::Speech;
using namespace Microsoft::CognitiveServices::Speech::Audio;
using namespace Microsoft::CognitiveServices::Speech::Intent;

/*
 * USAGE IN PYTHON3+: 
 *
 * import azure_speech
 *
 * # Initialize Object 
 * mic = azure_speech.SpeechEngine()
 * 
 * # Calling Class Methods: 
 *
 * boolean_value = mic.recognize_keyword() -> bool
 * azure_result = mic.recognize_intent() -> string
 *
 * #########################################
 *
 * LISTENING LOOP:
 *
 * while still_listening:
 *  # Only fire recognize_intent() if recognize_keyword() returns true
 *  if mic.recognize_keyword():
 *    
 *    # Capture Response
 *    azure_result = mic.recognize_intent()
 *
 *    # Transform JSON string into JSON object for processing
 *    json_azure = json.loads(azure_result)
 *
 *
 *
 *
*/ 

class SpeechEngine 
{
  private:
    std::shared_ptr<SpeechConfig> config;
    std::shared_ptr<SpeechConfig> speechToTextConfig;
    std::shared_ptr<IntentRecognizer> intentRecognizer;
    std::shared_ptr<SpeechRecognizer> speechToTextRecognizer;
    std::shared_ptr<KeywordRecognizer> keywordRecognizer;
    std::shared_ptr<KeywordRecognitionModel> keywordModel;
    std::shared_ptr<LanguageUnderstandingModel> model;

  public:

    // Constructor
    SpeechEngine()
    {
      // LUIS.ai Configuration
      config = SpeechConfig::FromSubscription("196cbdf23a2545d587ad15c9319a8445", "westus");
      auto audioConfig = AudioConfig::FromDefaultMicrophoneInput();
      intentRecognizer = IntentRecognizer::FromConfig(config, audioConfig);
      model = LanguageUnderstandingModel::FromAppId("87daaaad-ecf4-4a6c-8691-ec820953e4b2");
      intentRecognizer-> AddAllIntents(model);

      // Speech To Text
      speechToTextConfig = SpeechConfig::FromSubscription("961343d2f0e441029e60bbd1e3cfc669", "centralus");
      speechToTextRecognizer = SpeechRecognizer::FromConfig(speechToTextConfig, audioConfig);

      // Keyword Configuration
      keywordModel = KeywordRecognitionModel::FromFile("1bccce7e-f4de-475b-ba2f-9eb9abaa1e08.table");
      auto keywordAudioConfig = AudioConfig::FromDefaultMicrophoneInput();
      keywordRecognizer = KeywordRecognizer::FromConfig(keywordAudioConfig);
    }

    std::string transcribeSpeech(){
      std::shared_ptr<SpeechRecognitionResult> result;
      cout << "Say something...\n";

      result = speechToTextRecognizer->RecognizeOnceAsync().get();
      if (result->Reason == ResultReason::RecognizedSpeech)
      {
        string transcriptionResult = std::string(result->Text);
        return transcriptionResult;
      }
      else if (result->Reason == ResultReason::NoMatch)
      {
          cout << "NOMATCH: Speech could not be recognized...\n";
          return std::string(" ");
      }
      else if (result->Reason == ResultReason::Canceled)
      {
          auto cancellation = CancellationDetails::FromResult(result);
          cout << "CANCELED: Reason=" << (int)cancellation->Reason << std::endl;
          if (cancellation->Reason == CancellationReason::Error)
          {
              cout << "CANCELED: ErrorCode=" << (int)cancellation->ErrorCode << std::endl;
              cout << "CANCELED: ErrorDetails=" << cancellation->ErrorDetails << std::endl;
              cout << "CANCELED: Did you update the subscription info?" << std::endl;
              return "";
          }
          else {
            return "";
          }
      }
      return "";
    }

    /*
     * Captures LUIS.ai response after voice command is given and is transformed to string. Exposed in Python as recognize_intent()
    */
    std::string recognizeIntent()
    {

      cout << "Say something...\n";
      std::shared_ptr<IntentRecognitionResult> result;
      result = intentRecognizer->RecognizeOnceAsync().get();

      if (result->Reason == ResultReason::RecognizedIntent)
      {
          // cout << "RECOGNIZED: Text=" << result->Text << std::endl;
          // cout << "  Intent Id: " << result->IntentId << std::endl;
          string intentResult = std::string(result->Properties.GetProperty(PropertyId::LanguageUnderstandingServiceResponse_JsonResult));
          return intentResult;
      }

      else if (result->Reason == ResultReason::RecognizedSpeech)
      {
          // cout << "RECOGNIZED: Text=" << result->Text << " (intent could not be recognized)" << std::endl;
          return "";
      }

      else if (result->Reason == ResultReason::NoMatch)
      {
          // cout << "NOMATCH: Speech could not be recognized." << std::endl;
          return "";
      }

      else if (result->Reason == ResultReason::Canceled)
      {
          auto cancellation = CancellationDetails::FromResult(result);
          cout << "CANCELED: Reason=" << (int)cancellation->Reason << std::endl;

          if (cancellation->Reason == CancellationReason::Error)
          {
              // cout << "CANCELED: ErrorCode=" << (int)cancellation->ErrorCode << std::endl;
              // cout << "CANCELED: ErrorDetails=" << cancellation->ErrorDetails << std::endl;
              // cout << "CANCELED: Did you update the subscription info?" << std::endl;
              return "";
          }

          string errorCode = std::to_string((int)cancellation->ErrorCode);
          return "CANCELLED: ErroCode=" + errorCode;
      }
      return "ProcessCancelled";
    }

    /*
     * Listen for activation word (Wake Up). Process won't conclude until activation word is heard. Exposed
     * in Python as recognize_intent(). Returns true if keyword is recognized.
    */
    bool recognizeKeyword()
    {

      auto resultFuture = keywordRecognizer->RecognizeOnceAsync(keywordModel);
      resultFuture.wait();
      auto result = resultFuture.get();
      if (result->Reason == ResultReason::RecognizedKeyword){
        cout << "KEYWORD DETECTED" << std::endl;
	return true;

      }
      return false;
    }
};

// // Creates the entry point that will be invoked when the Python interpreter imports an extension module.
PYBIND11_MODULE(azure_speech, handle) {
  handle.doc() = "Python Wrapper API for Azure Cognitive Speech Services Written in C++";

  py::class_<SpeechEngine>(handle, "SpeechEngine")
    .def(py::init())
    .def("recognize_intent", &SpeechEngine::recognizeIntent)
    .def("recognize_keyword", &SpeechEngine::recognizeKeyword)
    .def("transcribe_speech", &SpeechEngine::transcribeSpeech);
}

// int main(int argc, char **argv) 
// {
//   setlocale(LC_ALL, "");
//   SpeechEngine mic = SpeechEngine();

//   while(1){
//     if(mic.recognizeKeyword()){
//       auto  content = mic.transcribeSpeech();
//       cout << content << std::endl;
//     }
//   }
//   return 0;
// }
