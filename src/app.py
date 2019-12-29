from flask import Flask
from flask import request, jsonify
from flask import Response
from flask import json
from gevent.pywsgi import WSGIServer
import numpy as np
import wave
import sys
import spacy
import textacy
import os.path
from spacy.matcher import PhraseMatcher
from entity_relation import extract_currency_relations
nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)

app = Flask(__name__)

pattern = r'<VERB>?<ADV>*<VERB>+'

def extract_noun_phrase(text):
    doc = nlp(text)
    noun_phrases = []
    for np in doc.noun_chunks:
        noun_phrases.append(np.text)
    print(noun_phrases)
    return noun_phrases 
def extract_verb_phrase(text):
    doc = nlp(text)
    verb_phrases = []
    verb_chunks = textacy.extract.pos_regex_matches(doc, pattern)
    for vb in verb_chunks:
        verb_phrases.append(vb.text)
    print(verb_phrases)
    return verb_phrases  

@app.route('/extract-phrase', methods = ['POST'])
def extract_phrase():
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        nounPhrase = extract_noun_phrase(dataDict["text"])
        verbPhrase = extract_verb_phrase(dataDict["text"])
        phraseDic = {
            "noun": nounPhrase,
            "verb": verbPhrase
        }
        return jsonify(phraseDic)
    else:
        return Response()

@app.route('/extract-relation', methods = ['POST'])
def find_relation():
    if request.method == 'POST':
        data = request.get_data()
        dataDict = json.loads(data)
        doc = nlp(dataDict["text"])
        relations = extract_currency_relations(doc)
        output = {}
        for r1, r2 in relations:
            output[r1.text] = r2.text
        return jsonify(output)
    else:
        return "Invalid Request"

@app.route('/ping', methods = ['GET'])
def health():
    return "Ok"

if __name__ == '__main__':
    print("Starting the server...")
    port = 8050
    http_server = WSGIServer(('', port), app)
    print("Server started and listing on port: ", port)
    http_server.serve_forever()
