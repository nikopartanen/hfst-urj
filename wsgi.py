import os
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from uralicNLP.cg3 import Cg3
from uralicNLP import tokenizer
from uralicNLP import uralicApi
import jinja2

env = jinja2.Environment()
env.globals.update(zip=zip)

#uralicApi.download("kpv")
#uralicApi.download("myv")

def process_sentence(sentence, language):

  tokens = tokenizer.words(sentence)
  cg = Cg3(language)

  result = []

  disambiguations = cg.disambiguate(tokens)
  for disambiguation in disambiguations:

      word = disambiguation[0]

      lemmas = []
      morphologies = []
      
      possible_words = disambiguation[1]

      for possible_word in possible_words:

          lemmas.append(possible_word.lemma)

          morphology = possible_word.morphology[:-1]
          morphologies.append('+'.join(morphology))

      result.append({'word' : word, 'lemmas' : '|'.join(list(set(lemmas))), 'analysis' : '|'.join(list(set(morphologies)))})
    
  return result

application = Flask(__name__)
Bootstrap(application)

@application.route('/', methods=['GET'])
def upload():
    return render_template('upload.html')

@application.route('/results', methods=['POST'])
def results():

    text_data = request.form['text']

    result = process_sentence(text_data, 'kpv')

    tokens = []
    lemmas = []
    analysis = []

    for r in result:

        tokens.append(r['word'])
        lemmas.append(r['lemmas'])
        analysis.append(r['analysis'])
    
    return render_template('results.html', 
                                   tokens=tokens, lemmas = lemmas, analysis = analysis, zip=zip)


if __name__ == '__main__':
    application.run(debug=True)