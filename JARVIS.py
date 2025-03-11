import io 
from pydub import AudioSegment
import speech_recognition as sr
import whisper  
import tempfile
import os
import pyttsx3
import pywhatkit

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')


listener = sr.Recognizer()
engine = pyttsx3.init()  
voices = engine.getProperty('voices')
engine.setProperty('rate', 145)
engine.setProperty('voice', voices[2].id)

def talk(text):
    """Convierte texto en voz."""
    engine.say(text)
    engine.runAndWait()
    
def listen():
    """Captura audio desde el micrófono y lo guarda en un archivo .wav"""
    try:
        with sr.Microphone() as source: 
            print('Di algo...')
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format='wav') 
            return save_path  # ⬅
    except Exception as e:
        print(f"Error al escuchar: {e}")
        return None

def recognize_audio(audio_path):
    """Convierte audio en texto usando Whisper."""
    if audio_path is None:
        return "No se pudo capturar el audio."
    
    audio_model = whisper.load_model("base")  
    transcription = audio_model.transcribe(audio_path, language='spanish', fp16=False)
    return transcription['text']

def main():
    """Ejecuta el asistente de voz."""
    try: 
        response =  recognize_audio(listen()).lower()
        if 'reproduce' in response:
            song = response.replace('reproduce', '')
            talk(f'Reproduciendo {song}')
            pywhatkit.playonyt(song)
    except Exception as e:
        talk(f"Error : {e}")
        
        print(e)

if __name__ == '__main__':
    main()
