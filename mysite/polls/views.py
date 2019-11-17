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
        return render(request, 'polls/demo.html', {'origin': cumle, 'sentence': sentence, 'obje': "/museum_imgs/"+name+".jpg"})
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

def nlp(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    main_obj_token = main_object(doc)
    obj = match_features(extract_features(doc, main_obj_token), main_obj_token)
    return obj


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
            sentence, target_language = "en")
        translated = result['translatedText']
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
    context = {'origin': sentence, 'text': translated, 'error': text}
    return context


class Object:
    def __init__(self, name, color="black", size=1, number=1, location="random"):
        self.name = name
        self.color = color
        self.size = size
        self.number = number
        self.location = location
        self.strokeArray = []

    def print(self):
        print("Name: ", self.name, "\tColor:", self.color, " Size:", self.size, " Number:", self.number, " Location:",
              self.location)

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


def main_object(doc):
    obj = doc[0]
    for token in doc:
        if(token.tag_ == "NN" and obj.tag_ !="NN"):
            obj = token
        if(token.dep_ == "attr"):
            return token
    return obj

# Extract the relevant information of the main object
# Implement better ->
def extract_features(doc, main_obj_token):
  # Object of interest, dependency tag = "attr"
  # obj = [token for token in doc if (token.dep_ == "attr")]
  # print(type(obj))

    stack = []
    feature_lst = []
    stack=([child for child in main_obj_token.children])

    while stack:
        token = stack.pop()
        feature_lst.append(token.lemma_)
        if(token.pos_ != "NOUN"):
            stack+=[child for child in token.children]
    return feature_lst


# Creates an "Object" based on the given information
def match_features(feature_lst,main_obj_token):
    ob = Object(name = main_obj_token.text)
    for feature in feature_lst:
        if(isColor(feature)):
            ob.color = feature
        elif(isNumber(feature)):
            number = w2n.word_to_num(feature)
            ob.number = number
    return ob


def sentence_processing(sentence):
    doc = nlp(sentence)
    main_obj_token = main_object(doc)
    obj = match_features(extract_features(doc, main_obj_token), main_obj_token)
    return obj.to_json()