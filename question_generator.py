import requests
import itertools
#from text_quiz import generate_question_answers

def get_response(url):
    """
    Get response from API
    """

    response = requests.get(url)
    response = response.json()

    return response

def get_questions(subject, category, concept, text, language, difficulty, type, amount):
    """
    Generate questions
    """

    questions = []

    if subject == "Physics":

        # Generate questions from PhysWikiQuiz API
        for _ in itertools.repeat(None, amount):
            url = "https://physwikiquiz.wmflabs.org/api/v1?name={}".format(concept)
            questions.append(get_response(url))

    elif subject == "Trivia":

        #Generate questions from the Open Trivia Database
        url = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}&type={}".format(amount, category, difficulty, type)
        for question in list(get_response(url)['results']):
            if type == "multiple":
                questions.append(question['question'] + " a) " + question['correct_answer'] + " b) " + question['incorrect_answers'][0] + " c) " + question['incorrect_answers'][1] + " d) " + question['incorrect_answers'][2])
            elif type == "boolean":
                questions.append(question['question'] + " a) " + question['correct_answer'] + " b) " + question['incorrect_answers'][0])
            
    elif subject == "General" or subject == "Allgemein":
        questions = []
        #questions = generate_question_answers(text, language)

    return questions