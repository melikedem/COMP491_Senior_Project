from django.shortcuts import render
import speech_recognition as sr
from googletrans import Translator
# Create your views here.
from django.http import HttpResponse
from django.template import loader
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict
from quickdraw import QuickDrawData
from PIL import Image
from io import StringIO


def index(request):
    return render(request, 'polls/index.html')


def create_new_canvas(request):
    return HttpResponse("Started recording")


def request_page(request):
    text = "test"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        sentence = r.recognize_google(audio, language="tr-TR")
        text = "You said: " + sentence
        translator = Translator()
        translation = translator.translate(sentence)
        tokenizer = RegexpTokenizer(r'\w+')
        pos_tagged_sentence = nltk.pos_tag(tokenizer.tokenize(translation.text))
        obj_lst = []
        for tagged_word in pos_tagged_sentence:
            if tagged_word[1] == "NN":
                obj_lst.append(tagged_word[0])
        context = {'origin': translation.origin, 'text': translation.text, 'objects': obj_lst}
        text = translation.origin, ' -> ', translation.text
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results from Google Speech Recognition service; {0}".format(e)
    return render(request, 'polls/readyToDraw.html', context)


def draw_objects(request):
    qd = QuickDrawData()
    objects = request.GET.get('objects')
    objects = objects.replace("'", "")
    list = objects.strip("][").split(', ')
    return render(request, 'polls/drawing.html', {'object': list[0]})


