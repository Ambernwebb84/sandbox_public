import streamlit as st
import question_generator as qg
from dancing_technique import get_random_dance_figure_question
import random

# TITLE
st.title("Question generator")

# LANGUAGE
language = st.selectbox("Select Language", ["English", "Deutsch"])

# SUBJECT
if language == "English":
    subject = st.selectbox("Select subject", ["Physics", "General", "Trivia", "Dancing", "Language"])
elif language == "Deutsch":
    subject = st.selectbox("Wähle Fach", ["Allgemein"])

# CATEGORY, DIFFICULTY, TYPE
category = None
difficulty = None
type = None
if subject == "Trivia":
    
    # query category
    category = st.selectbox("Select category", ["General Knowledge", "Science & Nature", "Science: Computers"])
    # map category
    category = {"General Knowledge": 9, "Science & Nature": 17, "Science: Computers": 18}[category]
    
    # query difficulty
    difficulty = st.selectbox("Select difficulty", ["Easy", "Medium", "Hard"])
    # map difficulty
    difficulty = difficulty.lower()
    
    # query type
    type = st.selectbox("Select type", ["Multiple Choice", "True/False"])
    # map type
    type = {"Multiple Choice": "multiple", "True/False": "boolean"}[type]

# AMOUNT
if subject not in ["General","Allgemein","Dancing","Language"]:
    amount = st.slider("Amount of questions", 1, 10)
else:
    amount = 1

# CONCEPT AND TEXT
concept = ""
text = ""
if language == "English":
    subject_query_text = {"Physics": "concept name", "Trivia": "category", "General": "text", "Dancing": "dance area = Latin", "Language": "text"}
    query_text = "Enter " + subject_query_text[subject]
    if subject == "Physics":
        concept = st.text_input(query_text)
    elif subject == "General" or subject == "Language":
        text = st.text_input(query_text)
elif language == "Deutsch":
    query_text = "Gib Text ein"
    if subject == "Allgemein":
        text = st.text_input(query_text)

# GENERATION
if not (concept == "" and text == ""):
    questions = qg.get_questions(subject, category, concept, text, language, difficulty, type, amount)
    for question in questions:
        st.write(question)

if subject == "Dancing":
    figure_names_techniques = get_random_dance_figure_question()
    figure_name = figure_names_techniques[0][0]
    figure_technique = figure_names_techniques[0][1]
    st.write(figure_name + ", " + figure_technique[0] + ": \n")
    for step_nr in range(figure_technique[1].__len__()):
        try:
            correct = figure_technique[step_nr]
        except:
            correct = figure_technique[1][str(step_nr)]
        options = [figure_names_techniques[0][1][1][str(step_nr+1)]]
        pool = [list(technique[1][1].items())[1:] for technique in figure_names_techniques[1:4]]
        for entry in pool:
            select_step = random.randint(0,entry.__len__()-1)
            options.append(entry[select_step][1])
        answer = st.selectbox("Step " + str(step_nr+1), options)
        #if answer == correct:
        #    st.write('Correct!')