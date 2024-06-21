import pyaudio
import vosk
import json

'''
Requires pyAudio and portAudio.
PortAudio needs to be installed to your system, the other can be installed with pip
'''

class SpeechRecognizer():

    def __init__(self):
        self.model = vosk.Model('vosk-models/vosk-model-en-us-0.22')
        self.rec = vosk.KaldiRecognizer(self.model, 16000)

    def listen(self, output_file_path, keyword="terminate"):
        # Open the microphone stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8192)
        
        # Open a text file in write mode using a 'with' block
        with open(output_file_path, "w") as output_file:
            print(f"Listening for speech. Say '{keyword}' to stop.")
            # Start streaming and recognize speech
            while True:
                data = stream.read(4096)#read in chunks of 4096 bytes
                if self.rec.AcceptWaveform(data):#accept waveform of input voice
                    # Parse the JSON result and get the recognized text
                    result = json.loads(self.rec.Result())
                    recognized_text = result['text']
                    
                    # Write recognized text to the file
                    output_file.write(recognized_text + "\n")
                    print(recognized_text)
                    
                    # Check for the termination keyword
                    if keyword.lower() in recognized_text.lower():
                        print("Termination keyword detected. Stopping...")
                        break

            # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Terminate the PyAudio object
        p.terminate()


    
