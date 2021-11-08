import streamlit as st
import question_generator as qg

# TITLE
st.title("Question generator")

# LANGUAGE
language = st.selectbox("Select Language", ["English", "Deutsch"])

# SUBJECT
if language == "English":
    subject = st.selectbox("Select subject", ["Physics", "General", "Trivia", "Language"])
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
if subject != "General" and subject != "Allgemein" and subject != "Language":
    amount = st.slider("Amount of questions", 1, 10)
else:
    amount = 1

# CONCEPT AND TEXT
text = ""
if subject == "Trivia":
    concept = "Trivia"
    text = ""
else:
    if language == "English":
        subject_query_text = {"Physics": "concept name", "Trivia": "category", "General": "text", "Language": "text"}
        query_text = "Enter " + subject_query_text[subject]
        if subject == "Physics":
            concept = st.text_input(query_text)
            text = ""
        elif subject == "General" or subject == "Language":
            text = st.text_input(query_text)
            concept = ""
    elif language == "Deutsch":
        query_text = "Gib Text ein"
        if subject == "Allgemein":
            text = st.text_input(query_text)
            concept = ""

# GENERATION
text = ""
if not (concept == "" and text == ""):

    questions = qg.get_questions(subject, category, concept, text, language, difficulty, type, amount)
    for question in questions:
        st.write(question)