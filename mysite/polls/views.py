from typing import List, Any

from django.shortcuts import render
import speech_recognition as sr
from django.http import HttpResponse
import spacy
from spacy import displacy
from PIL import Image
import webcolors
from word2number import w2n
import re
import json
import random
from google.cloud import translate_v2 as translate

museum_items = ["ship", "carriage"]
obj_hist = []


def index(request):
    obj_hist.clear()
    return render(request, 'polls/index.html')


def create_new_canvas(request):
    return HttpResponse("Started recording")


def recordAndDraw(request):
    context = record()
    cumle = context["origin"]
    sentence = context["text"]
    obj = nlp(sentence)
    name = obj.name
    if name in museum_items:
        return render(request, 'polls/demo.html',
                      {'origin': cumle, 'sentence': sentence, 'obje': "/museum_imgs/" + name + ".jpg"})
    fileName = "/Users/apple/Downloads/filtered/" + name + ".ndjson"
    f = open(fileName, "r")
    qdImages = f.read()
    p = re.findall(r'{(.*?)}', qdImages)
    i = random.randrange(0, len(p), 1)
    y = json.loads("{" + p[i] + "}")
    obj.setStrokeArray(y["drawing"])
    obj_hist.append(obj.to_json())
    return render(request, 'polls/demo.html', {'origin': cumle, 'sentence': sentence, 'json': obj_hist})


def draw_objects(request):
    objects = request.GET.get('objects')
    if objects == None:
        return render(request, 'polls/demo.html')
    objects = objects.replace("'", "")
    list = objects.strip("][").split(', ')
    return render(request, 'polls/demo.html', {'object': list[0]})


def record():
    r = sr.Recognizer()
    text = ""
    translated = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        sentence = r.recognize_google(audio, language="tr-TR")
        translate_client = translate.Client()
        result = translate_client.translate(
            sentence, target_language="en")
        translated = result['translatedText']
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
    context = {'origin': sentence, 'text': translated, 'error': text}
    return context


def nlp(sentence):
    doc = nlp(sentence)
    main_lst_json = []
    main_lst = extract_main_object(doc)
    for main_object in main_lst:
        main_lst_json.append(match_features(extract_features(doc, main_object), main_object).to_json())
    return main_lst_json
    return obj


class Object:

    def __init__(self, name, color="black", size=1, number=1, location="random", action = None):
        self.name = name
        self.color = color
        self.size = size
        self.number = number
        self.location = location
        self.action = action
        self.strokeArray = []

    def print(self):
        print("Name: ", self.name, "\tColor:", self.color, " Size:", self.size, " Number:", self.number, " Location:",
              self.location, self.action)

    def to_json(self):
        return json.dumps(self.__dict__)

    def setStrokeArray(self, strokeArray):
        self.strokeArray = strokeArray


# Functions to identify what information a feature gives about the object
def isColor(feature):
    return feature in webcolors.CSS3_NAMES_TO_HEX


def isNumber(feature):
    try:
        w2n.word_to_num(feature)
        return True
    except:
        return False

action_map = [["fly"],["run"],["walk"]]
def isAction(feature):
    if(feature.lemma_ in action_map[0]):
      return "fly"
    elif(feature.lemma_ in action_map[1]):
      return "run"
    elif(feature.lemma_ in action_map[2]):
      return "walk"


def extract_main_object(doc):
    main_lst = [chunk.root for chunk in doc.noun_chunks if chunk.root.dep_ == "ROOT" or chunk.root.dep_ == "nsubj"]
    conj_lst = list([main.conjuncts for main in main_lst][0])
    return main_lst + conj_lst

def get_chunks(doc, main_obj_token):
  for chunk in doc.noun_chunks:
    if(chunk.root == main_obj_token):
      return [token for token in chunk if token != main_obj_token]

# Extract the relevant information of the main object
# Implement better ->
def extract_features(doc, main_obj_token):
    feature_lst = []
    stack = [ancestor for ancestor in main_obj_token.ancestors]
    while stack:
        print(stack)
        current = stack.pop()
        if (current.pos_ != "NOUN"):
            feature_lst.append(current)
            stack += [ancestor for ancestor in current.children]
    feature_lst += (get_chunks(doc, main_obj_token))
    return feature_lst


# Creates an "Object" based on the given information
def match_features(feature_lst, main_obj_token):
    ob = Object(name=main_obj_token.lemma_)
    for feature in feature_lst:
        feature_txt = feature.lemma_
        size = isSize(feature_txt)
        if (size):
            ob.size = size

        elif (isColor(feature_txt)):
            ob.color = feature_txt

        elif (isNumber(feature_txt)):
            number = w2n.word_to_num(feature_txt)
            ob.number = number

        elif (main_obj_token.tag_ == "NNS"):
            ob.number = random.randint(2, 5)

        elif (isPreposition(feature)):
            location = [child.lemma_ for child in feature.children if (child.tag_ == "NN")][0]
            ob.location = {"Preposition": feature.lemma_,
                            "Location": location}

        elif (isAction(feature)):
            ob.action = feature.text

    return ob