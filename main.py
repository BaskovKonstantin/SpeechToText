import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import argparse



def microphone_recognition(lang = 'en-US' ):
    r = sr.Recognizer()

    # use microphone as source
    with sr.Microphone() as source:
        print("Speak something:")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language=lang)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
    except sr.RequestError as e:
        print(f"Request error: {e}")


def audio_file_recognition(lang = 'en-US', filename = "Ruzvelt.mp3"):
    r = sr.Recognizer()
    audio_file = AudioSegment.from_file(filename, format="mp3")

    # split audio into chunks of 10 seconds
    chunk_length_ms = 10000
    chunks = make_chunks(audio_file, chunk_length_ms)

    # process each chunk
    for i, chunk in enumerate(chunks):

        #Надо установить ffmpeg и добавить в системные переменные
        print(f"Processing chunk {i + 1}/{len(chunks)}")

        # export chunk to temporary WAV file
        chunk.export("temp.wav", format="wav")

        # read temporary WAV file
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)

        # recognize speech using Google Speech Recognition
        try:
            text = r.recognize_google(audio, language=lang)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, help='Имя аудифайла для захвата', default='stalin.mp3')
    parser.add_argument('--lang', type=str, help='язык для распознавания', default='ru-RU')
    parser.add_argument('--type', type=int, help='Выбор источника звука файл или микрофон', default='file')
    args = parser.parse_args()


    try:
        if (args.type == 'file'):
            audio_file_recognition(args.lang, args.filename)
        else:
            microphone_recognition(args.lang)
    except:
        print('что-то пошло не так')
