import streamlit as st
import st_state_patch
import question_generator as qg
import dancing_technique
import random
import json

# # LOAD CACHE
# with open("cache.json", 'r') as f:
#     cache = json.load(f)

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

    def display_question_options(figure_names_techniques):

        figure_name = figure_names_techniques[0][0]
        figure_technique = figure_names_techniques[0][1]
        st.write(figure_name + ", " + figure_technique[0] + ": \n")
        number_of_steps = figure_technique[1].__len__()
        for step_nr in range(number_of_steps):
            #try:
            #    correct = figure_technique[step_nr]
            #except:
            #    correct = figure_technique[1][str(step_nr)]
            options = [figure_names_techniques[0][1][1][str(step_nr + 1)]]
            pool = [list(technique[1][1].items())[1:] for technique in figure_names_techniques[1:4]]
            for entry in pool:
                select_step = random.randint(0, entry.__len__() - 1)
                options.append(entry[select_step][1])
            random.shuffle(options)
            #options2 = ['Select']
            #options2.extend(options)
            #options = options2

            # write
            choice = "a) " + options[0] + " b) " + options[1] + " c) " + options[2] + " d) " + options[3]
            st.write("Step " + str(step_nr+1) + ": " + choice)
            #answer = st.text_input("Step " + str(step_nr))
            # st.write("Step " + str(step_nr+1) + ": " + " | ".join(options))

            # selectbox
            #answer = st.selectbox("Step " + str(step_nr + 1), options)
            #answer = st.text_input()
            #if answer == correct:
            #    st.write('Correct!')
            #    #st.success('Yes!')

    # MULTIPLE CHOICE
    #figure_names_techniques = dancing_technique.get_random_multiple_choice_dance_figure_question()
    #display_question_options(figure_names_techniques)

    #answer = st.text_input('Answer')
    #if answer == 'a)':#solution:
        #st.success('Yes!')
    #elif answer != '':
        #st.warning('No!')

    # TEXT LINES
    figure_name_technique = dancing_technique.get_random_text_line_dance_figure_question()
    figure_name = figure_name_technique[0]
    figure_technique = figure_name_technique[1]
    figure_technique_lines = list(figure_technique[1].values())

    solution = ''
    for line in figure_technique_lines:
        solution += line + ", "
    solution = solution[:-2]
    st.write(figure_name + ", " + figure_technique[0])

    # STATE PATCH (AND CACHE)
    # https://discuss.streamlit.io/t/part-of-page-is-getting-refreshed-on-dropdown-selection/3336/4
    state = st.State()
    if not state:
        state.pressed_first_button = False
    if st.button("Show solution") or state.pressed_first_button:
        state.pressed_first_button = True # preserve the info that you hit a button between runs
        st.write(solution)

# # SAVE CACHE
# cache = figure_names_techniques
# with open("cache.json", 'w') as f:
#     json.dump(cache,f)