import pyttsx3
#import speech_recognition as sr

# Initialize the text-to-speech object
engine = pyttsx3.init()
# Initialize the speech-to-text object
# r = sr.Recognizer()

def speak_text(text):
    # engine.setProperty('rate', 1000)
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[2].id) # female
    engine.say(text)
    engine.runAndWait()


# while(True):
#     try:
#         # use the microphone as source for input.
#         with sr.Microphone() as source2:
            
#             print("Adjusting to ambient sound...")
#             # wait for a second to let the recognizer
#             # adjust the energy threshold based on
#             # the surrounding noise level
#             r.adjust_for_ambient_noise(source2, duration=2)
                
#             #listens for the user's input
#             audio2 = r.listen(source2, timeout=50, phrase_time_limit=5.0)
#             print("Listening. Please speak.")

#             # Using google to recognize audio
#             MyText = r.recognize_google(audio2)
#             MyText = MyText.lower()
#             print("Did you say ", MyText)
#             engine.say(MyText)
#             engine.runAndWait()

#             # print("Did you say ", MyText)
#             # SpeakText(MyText)
            
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))

#     except sr.UnknownValueError:
#         print("unknown error occurred")