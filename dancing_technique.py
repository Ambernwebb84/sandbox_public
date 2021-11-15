import os
import random

data_path = "data/dancing_figures/Latin/"

# Scan data folder for dance figure files
figures = []
excluded_files = ["Mistakes.txt"]
for file_name in os.listdir(data_path):
    if file_name.endswith(".csv"):
        infos = file_name.strip(".csv").split("_")
        figures.append(infos)

# Select random figure
figure_number = random.randrange(0,len(figures),1)
dance = figures[figure_number][0]
figure = figures[figure_number][1]
gender = figures[figure_number][2]

dance_figure_file = dance + "_" + figure + "_" + gender + ".csv"

# open file
with open(data_path + dance_figure_file,"r",encoding="utf8") as f:
    lines = f.readlines()

# csv to dict

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
dance_figure_dict_technique = {}
for step in dance_figure_dict_steps.items():
    for technique in step[1].items():
        try:
            dance_figure_dict_technique[technique[0]][step[0]] = technique[1]
        except:
            dance_figure_dict_technique[technique[0]] = {}
            dance_figure_dict_technique[technique[0]][step[0]] = technique[1]

# # query by steps
# for step in dance_figure_dict.items():
#     print("Schritt: " + step[0])
#     for technique in step[1].items():
#         input()
#         if technique[0] != '﻿Schritt':
#             print(technique[0] + ": ")
#             input("?")
#             print(technique[1])

mistakes = 0
total = 0
mistake_lines = []
# query by technique
print(dance_figure_file.strip(".csv") + "...")
for technique in dance_figure_dict_technique.items():
    input()
    if not 'StepNo' in technique[0]:
        print("Technique: " + technique[0])
        for step in technique[1].items():
            print(step[0] + ": ")
            answer = input("?")
            print(step[1])
            total += 1
            # check if answer correct (case insensitively)
            if answer.lower()==step[1].lower():
                print("yes! :)")
            else:
                print("no! :(")
                mistakes += 1
                mistake_lines.append(dance_figure_file.strip(".csv")
                                     + ", " + technique[0]
                                     + ", " + step[0]
                                     + ", " + answer
                                     + " != " + step[1]
                                     + "\n")

print("Mistakes: " + str(mistakes) + "/" + str(total) + " = " + str(round(mistakes/total,2)*100) + "%")

# save mistake lines
with open(data_path + "Mistakes.txt","r") as f:
    lines = f.readlines()
    lines.append("\n")
    lines.extend(mistake_lines)
with open(data_path + "Mistakes.txt", "w") as f:
    f.writelines(lines)

print("end")