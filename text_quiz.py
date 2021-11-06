import nltk
import spacy
import random
import string

# input
#input_text = """The United States of America is the world's third largest country in size and nearly the third largest in terms of population. Located in North America, the United States is bordered on the west by the Pacific Ocean and to the east by the Atlantic Ocean. Along the northern border is Canada and the southern border is Mexico. There are 50 states and the District of Columbia."""
#input_text = input('Input text: ')
#print(input_text)

def get_annotation_nltk(text):
    # clean text and get words

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)

    # get part-of-speech tag for each word
    pos = nltk.pos_tag(words)

    for word in pos:
        print(f'{word[0]} {word[1]}')
    print()

    return pos

#https://stackabuse.com/python-for-nlp-parts-of-speech-tagging-and-named-entity-recognition/
def get_annotation_spacy(text):
    # python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    pos = []
    for word in doc:
        print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
        pos.append((word.text,word.tag_))
    # spacy.displacy.render(doc,jupyter=True,style='ent')
    # TODO: swremoval, stemming, coref res
    print()

    return pos

# get nouns
def get_nouns_eng(sent_text):
    nouns = []
    for sent in sent_text:
        sent_anno = get_annotation_nltk(sent)
        for word in sent_anno:
            if word[1].startswith("N") and len(word[0]) > 1:
                nouns.append(word[0])
    return nouns

def get_nouns_deu(sent_text):
    nouns = []
    nlp = spacy.load('de_core_news_sm')  # Use the  German model
    for sent in sent_text:
        sent_anno = nlp(sent)
        for word in sent_anno:
            if word.pos_.startswith('N') and len(word.text) > 1:
                nouns.append(word.text)

    return nouns

# generate gap questions and answers
def get_question_answers(sent_text,nouns):
    nr_answers = 4
    question_answers = []
    if len(nouns) >= nr_answers:
        sent_nr = 1
        for sent in sent_text:
            generated = False
            # random gap
            for noun in nouns:
                if noun in sent and generated == False:
                    question = sent.replace(noun, "_______")
                    print(question)
                    answers = set()
                    answers.add(noun)
                    while len(answers) < nr_answers:
                        try:
                            answers.add(nouns[random.randint(0,len(nouns))])
                        except:
                            pass
                    print(answers)
                    print()
                    #question_answers.append((question,answers))
                    answers = list(answers)
                    alphabet = list(string.ascii_lowercase)
                    answer = ""
                    for i in range(len(answers)):
                        answer += alphabet[i] + ") " + answers[i] + " "
                    question_answers.append(question + " " + answer)
                    generated = True
            sent_nr += 1
        return question_answers
    else:
        print('Not enough nouns found to generate ' + str(nr_answers) + " answers for each question")
        return None

def generate_question_answers(input_text,language):

    # split sentences
    sent_text = nltk.sent_tokenize(input_text)
    if language == 'English':
        nouns = get_nouns_eng(sent_text)
    elif language == 'Deutsch':
        nouns = get_nouns_deu(sent_text)
    else:
        print('No valid language selected')
    question_answers = get_question_answers(sent_text,nouns)

    return question_answers

print()