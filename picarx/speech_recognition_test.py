'''
Requires pyAudio, pocketsphinx and portAudio.
PortAudio needs to be installed to your system, the other two can be installed with pip
'''


import speech_recognition as sr
import pyaudio
import vosk
import json



if __name__ == '__main__':

    model = vosk.Model("/home/tom/Documents/Robotics/robotics/robotics/picarx/vosk-model-en-us-0.22")

    # r = sr.Recognizer()

    # with sr.Microphone() as source:
    #     print("Say something!")
    #     audio = r.listen(source, timeout=2, phrase_time_limit=5)

    # Create a recognizer
    rec = vosk.KaldiRecognizer(model, 16000)

    # Open the microphone stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    
    # Specify the path for the output text file
    output_file_path = "recognized_text.txt"
    
    # Open a text file in write mode using a 'with' block
    with open(output_file_path, "w") as output_file:
        print("Listening for speech. Say 'Terminate' to stop.")
        # Start streaming and recognize speech
        while True:
            data = stream.read(4096)#read in chunks of 4096 bytes
            if rec.AcceptWaveform(data):#accept waveform of input voice
                # Parse the JSON result and get the recognized text
                result = json.loads(rec.Result())
                recognized_text = result['text']
                
                # Write recognized text to the file
                output_file.write(recognized_text + "\n")
                print(recognized_text)
                
                # Check for the termination keyword
                if "terminate" in recognized_text.lower():
                    print("Termination keyword detected. Stopping...")
                    break

        # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()

    # with open("audio_file.wav", "wb") as file:
    #     file.write(audio.get_wav_data())

    

    # # recognize speech using Sphinx
    # try:
    #     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    # except sr.UnknownValueError:
    #     print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))

    # try:
    #     # for testing purposes, we're just using the default API key
    #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #     # instead of `r.recognize_google(audio)`
    #     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    # except sr.UnknownValueError:
    #     print("Google Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))