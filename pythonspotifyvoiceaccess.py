import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify OAuth bilgilerinizi buraya girin
scope = "user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="http://localhost:8888",
    scope=scope
))

# Ses tanıma ve metin okuma nesnelerini oluşturma
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def listen():
    with sr.Microphone() as source:
        print("Dinliyorum...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='tr-TR')
            print("Sen: {}".format(text))
            return text
        except sr.UnknownValueError:
            print("Anlayamadım.")
        except sr.RequestError as e:
            print("Yanıt alınamadı; {0}".format(e))

# Spotify'ı kontrol etme fonksiyonları
def play_song(query):
    results = sp.search(q=query, limit=1)
    if results['tracks']['items']:
        uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[uri])
        print("Şarkı çalıyor:", uri)
    else:
        print("Şarkı bulunamadı.")

# Ana döngü
while True:
    command = listen()
    if command == "çıkış":
        break
    elif "çal" in command:
        song = command.replace("çal", "")
        play_song(song)
