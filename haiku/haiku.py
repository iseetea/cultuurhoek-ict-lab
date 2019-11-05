from gpiozero import Button
from time import sleep
import subprocess

def read_text(data):
    from gtts import gTTS    
    tts = gTTS(text=data, lang='nl')
    tts.save("good.mp3")
    os.system("mpg321 good.mp3")

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    response = client.annotate_image({'image': {'source': {'image_uri': path}}, 'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION, 'max_results':2}] })

    labels = response.annotations
    print('Labels:')

    labelList = [translate_label(label.description) for label in labels]
    return ' '.join(labelList)


def translate_label(label):
    from googletrans import Translator
    translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.nl',
    ])
    translation = translator.translate(label, dest='nl')
    print(translation.text)
    return translation.text

import os 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/haiku/gvision-key.json"
#print(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) 

pir = Button(2)

while True:
        if pir.is_pressed:
                print "taking photo..."
                subprocess.call("./photo.sh")
                print "analyzing..."
                read_text(detect_labels('photo.jpg'))
        else:
                print("No movement")
        sleep(1)