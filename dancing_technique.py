import os
import random

# Scan data folder for dance figure files
def get_dance_figures(data_path):
    figures = []
    for file_name in os.listdir(data_path):
        if file_name.endswith(".csv"):
            infos = file_name.strip(".csv").split("_")
            figures.append(infos)
    return figures

# Select random figure
def get_random_figure(figures):
    figure_number = random.randrange(0,len(figures),1)
    dance = figures[figure_number][0]
    name = figures[figure_number][1]
    gender = figures[figure_number][2]
    dance_figure = dance + "_" + name + "_" + gender
    return dance_figure

# Select random technique
def get_random_technique(figure,technique_number):
    technique = list(figure.items())[technique_number]
    return technique

# Create figure techniques dictionary
def get_figures_techniques_dict(data_path,figures):

    dance_figures_technique_dict = {}
    for figure in figures:
        dance = figure[0]
        name = figure[1]
        gender = figure[2]

        dance_figure_file = dance + "_" + name + "_" + gender + ".csv"

        # open file
        with open(data_path + dance_figure_file,"r",encoding="utf8") as f:
            lines = f.readlines()

        # sort by steps
        dance_figure_dict_steps = {}
        for line in lines:
            content = line.strip("\n").split(";")
            # get header
            #if content[0] == '﻿Schritt':
            if '﻿StepNo' in content[0]:
                header = content
            # extend dict
            else:
                dance_figure_dict_steps[content[0]] = {}
                caption_nr = 0
                for caption in header:
                    dance_figure_dict_steps[content[0]][caption] = content[caption_nr]
                    caption_nr += 1

        # sort by technique
        dance_figure_file = dance_figure_file.strip(".csv")
        dance_figures_technique_dict[dance_figure_file] = {}
        for step in dance_figure_dict_steps.items():
            for technique in step[1].items():
                try:
                    dance_figures_technique_dict[dance_figure_file][technique[0]][step[0]] = technique[1]
                except:
                    dance_figures_technique_dict[dance_figure_file][technique[0]] = {}
                    dance_figures_technique_dict[dance_figure_file][technique[0]][step[0]] = technique[1]

    return dance_figures_technique_dict

# Get random multiple choice dance figure question
def get_random_multiple_choice_dance_figure_question():

    data_path = "data/dancing_figures/Latin/"

    # Dance figures dict
    figures = get_dance_figures(data_path)
    dance_figures_dict = get_figures_techniques_dict(data_path,figures)

    # Get four random figure techniques for multiple-choice
    technique_numbers = list(dance_figures_dict.items())[0][1].__len__()
    technique_number = random.randrange(1, technique_numbers, 1)
    figure_names_techniques = []
    for i in range(4):
        figure_name = get_random_figure(figures)
        figure_techniques = dance_figures_dict[figure_name]
        figure_technique = get_random_technique(figure_techniques,technique_number)
        figure_names_techniques.append((figure_name,figure_technique))

    return figure_names_techniques

# Get random text line dance figure question
def get_random_text_line_dance_figure_question():

    data_path = "data/dancing_figures/Latin/"

    # Dance figures dict
    figures = get_dance_figures(data_path)
    dance_figures_dict = get_figures_techniques_dict(data_path,figures)

    # Get random figure technique
    technique_numbers = list(dance_figures_dict.items())[0][1].__len__()
    technique_number = random.randrange(1, technique_numbers, 1)
    figure_name = get_random_figure(figures)
    figure_techniques = dance_figures_dict[figure_name]
    figure_technique = get_random_technique(figure_techniques,technique_number)
    figure_name_technique = (figure_name,figure_technique)

    return figure_name_technique