import pyttsx3
import yaml
import time
from pygame import mixer


class Speaker:
    def __init__(self, language) -> None:
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty("voices")
        selected_voice = None
    
        for voice in voices:
            if language in voice.languages:
                selected_voice = voice
                print(f"using {voice.id}, {voice.name}, {voice.languages}")

        self.engine.setProperty("voice", selected_voice.id)


    def speak(self, phrase="", volume=0.5, rate=150):
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)
        self.engine.say(phrase)
        self.engine.runAndWait()
        return self

    def ask(self, phrase="", volume=0.5, rate=150):
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)
        self.engine.say(phrase)
        self.engine.runAndWait()
        return input()
     


speaker = Speaker('pt_BR')

story_folder = "./tres-porquinhos"
script = None
with open(f"{story_folder}/story.yml", 'r') as file:
    script = yaml.safe_load(file)



index = "init"
sound = None

#Instantiate mixer
mixer.init()

while True:
    print(f"part: {index}")
    part = script[index]
    flip = mixer.Sound(f"pagesturning-54090.ogg")
    
    flip.play(loops= 0, maxtime=1000)

    for speak in part["speak"]:
        speaker.speak(speak)
    

    ask = part.get("ask", None)
    to = part.get("to", None)
    duration = part.get("duration", None)
    _sound = part.get("sound", None)
    
    if _sound and _sound != sound:
        sound = _sound

        mixer.music.load(f"{story_folder}/{sound}")
        # sound_effect = mixer.Sound(f"{story_folder}/{sound}")
        mixer.music.play()
        time.sleep(duration)
        mixer.music.stop()
    
    if ask:
        while True:
            awnser = speaker.ask(ask)
            _index = part["awnsers"].get(awnser)
            if not script.get(_index, None):
                speaker.speak("opção inválida")
            else:
                index = _index
                break
    elif to:
        index = to
    else:
        break

