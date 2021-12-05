import streamlit as st
import dancing_technique
import json
import random

data_path = "data/dancing_figures/"

# # LOAD CACHE
with open("cache.json", 'r') as f:
    cache = json.load(f)
question = cache['question']
question_level = cache['question_level']
step_number = cache['step_number']

def get_technique_properties(question):
    figure_name = question[0]
    figure_technique = question[1]
    technique_name = figure_technique[0]
    technique_details = list(figure_technique[1].values())
    return figure_name,technique_name,technique_details

# hide streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header('Dancing Technique Quiz')

col1,col2 = st.columns(2)

# Question
col1.header('Question')
with col1:

    dancing_domain = st.selectbox("Select domain", ["Ballroom", "Latin"])
    figure_subset = st.selectbox("Select subset", ["All", "Exam"])
    only_exam = False
    if figure_subset == 'Exam':
        only_exam = True

    if st.button('Random figure'):
        question = dancing_technique.get_random_text_line_dance_figure_question(data_path,dancing_domain,only_exam)
        question_level = 'all_steps'
    figure_name, technique_name, technique_details = get_technique_properties(question)
    col1.write(figure_name + ", " + technique_name)
    if st.button('Random step'):
        step_number = random.randint(1,len(technique_details))
        question_level = 'single_step'
    if st.button('All steps'):
        question_level = 'all_steps'

    if question_level == 'single_step':
        step_string = 'Step ' + str(step_number)
        st.write(step_string)


# Answer
col2.header('Answer')
with col2:
    answer = st.text_area('Enter Answer')
    if st.button('Check'):
        figure_name, technique_name, technique_details = get_technique_properties(question)

        if question_level == 'all_steps':
            technique_detail_string = ', '.join(technique_details)
            question_detail_string = ", ".join([figure_name,technique_name])
        elif question_level == 'single_step':
            technique_detail_string = technique_details[step_number-1]
            step_string = 'Step ' + str(step_number)
            question_detail_string = ", ".join([figure_name,technique_name,step_string])

        if answer.lower() == technique_detail_string.lower():
            correction_prefix = 'Yes'
        else:
            correction_prefix = 'No'

        col2.write(correction_prefix + ', the correct answer for ')
        col2.write(question_detail_string)
        col2.write(' is ')
        col2.write(technique_detail_string)

# # SAVE CACHE
cache['question'] = question
cache['question_level'] = question_level
cache['step_number'] = step_number
with open("cache.json", 'w') as f:
    json.dump(cache,f)