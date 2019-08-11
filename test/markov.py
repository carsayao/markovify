import markovify
import datetime
import random
import re
import nltk
import os.path
import sys
from pathlib import Path
try:
    import simplejson as json
except:
    import json

def main():

    # test
    def get_json():
        out = { 'key': 'value', 'key2': 'value2' }
        print(json.dumps(out))

    def clean_text(text):

        # Strip and replace special characters
        cleaned = text.replace('"', '')
        cleaned = cleaned.replace('”', '"')
        cleaned = cleaned.replace('“', '"')
        cleaned = cleaned.replace('’', "'")
        cleaned = cleaned.replace('‘', "'")
        cleaned = cleaned.replace('#', "'")
        cleaned = cleaned.lower()
        return cleaned

    def gen_model(person):
        # Get raw text as string.
        text = ''
        # onlyfiles = next(os.walk(inputDir+person+'/'))[2]

        # print('onlyfiles', onlyfiles)
        # print("inputDir+person+'/'",inputDir+person+'/')
        # print('onlyfiles',len(onlyfiles))
        for file in os.listdir(inputDir + person + '/'):
            with open(inputDir + person + '/' + file) as f:
                text += '\n' + f.read()
                # if len(onlyfiles) > 1:
                #     text += '\n' + f.read()
                # else:
                #     text = f.read()

        # Check what the text is
        with open(inputDir+person+'_cat.txt','w+') as test:
            test.write(text)
        # Clean transcript        
        cleaned = clean_text(text)
        with open(inputDir+person+'_cleancat.txt','w+') as fclean:
            fclean.write(cleaned)
        # Build the model, reject_reg rejects bracketed text
        text_model = markovify.Text(cleaned, state_size=2)#, reject_reg='\[.*?\][ \t\n]*')
        # Turn into json
        model_json = text_model.to_json()
        # Write model to json
        with open(outputDir + person + '_model.json', 'w+') as fpjson:
            json.dump(model_json, fpjson)
        
    def load_model(person, word):
        # Load model from json
        with open(outputDir + person + '_model.json') as fprecon:
            recon_json = json.load(fprecon)
        recon_model = markovify.Text.from_json(recon_json)

        # TODO: testing user input with init_state
        response = recon_model.make_sentence(init_state=(word,''), tries=10, test_output=True, mot=15) # response = recon_model.make_sentence() 
        if response is None:
            out = { 'text': "I don't know what to say to that..." }
        else:
            out = { 'text': response }

        print(json.dumps(out))
      
    def get_text(person, word):
        myfile = Path(outputDir + person + '_' + 'model.json')
        if myfile.is_file():
            # print('"' + person + '_model.json" exists')
            load_model(person, word)
            print('load')
        else:
            # print('"' + person + '_model.json" does not exist')
            gen_model(person)
            load_model(person, word)
            print('gen')
            print('load')
    
    def nouns(query):
        # https://stackoverflow.com/a/33587889
        # function to test if something is a noun
        # print('query',query)
        is_noun = lambda pos: pos[:2] == 'NN'
        # print('time', datetime.datetime.now())
        seed = str(datetime.datetime.now())[-6:]
        # print(seed)
        try:
            # do the nlp stuff
            tokenized = nltk.word_tokenize(query)
            nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
            random.seed(a=seed)
            word = random.choice(nouns)
            print('random word',word)
            return word
        except:
            # out = { 'text': "i don't know what to say to that..." }
            # print(json.dumps(out))
            return
      
    # Setup our input/output
    path = os.path.dirname(os.path.realpath(__file__))
    # print('path', path)
    # inputDir = path + '/../texts/'
    inputDir = path + '/texts/'
    # print('inputDir', inputDir)
    # outputDir = path + '/../models/'
    outputDir = path + '/models/'
    # print('outputDir', outputDir)
    person = 'iliza'
    # Get user input (as list)
    # query = sys.argv[1:]
    # if len(query) == 0:
    #     out = { 'text': 'anyone there? hello?' }
    #     print(json.dumps(out))
    # print(query)
    # word = ' '.join(nouns(query))
    # print(word)

    query = sys.argv[1]
    if len(query) == 0:
        out = { 'text': 'anyone there? hello?' }
        print(json.dumps(out))
        exit()
    print(query)
    # word = ' '.join(nouns(query))
    # Strip and replace special characters for nltk tokenizer
    query = query.replace("'", '')
    query = query.replace('"', '')
    query = query.replace('"', '')
    query = query.replace('”', '')
    query = query.replace('“', '')
    query = query.replace('’', "")
    query = query.replace('‘', "")
    query = query.replace('#', "")
    query = query.lower()
    print('cleaned query', query)
    word = nouns(query)
    print('chosen word',word)


    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    try:
        get_text(person, word)
    except Exception:
        print(json.dumps({ "text": "Sorry, I'm having trouble understanding you..." }))


if __name__ == '__main__':
    main()
