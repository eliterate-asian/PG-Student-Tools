import PyPDF2
import bs4
import os
import re


# INSTRUCTIONS
# Save an HTML only file of the Grades page of the given course (url will be something like "https://purdueglobal.brightspace.com/d2l/lms/grades/my_grades/main.d2l?ou=306065")
workingdir = os.path.dirname(os.path.realpath(__file__))
readydir = str(workingdir + "\\ready\\")


### 

# 

def form_extract(some_string, key):
    broken = re.split('>|<|;|&', some_string)
    assembled = []
    for i in broken:
        if key in i and i[0] == 'U' and key != i:
            assembled.append(i)
    return assembled

def carrot_extract(some_string, key):
    cleaned_string = ''
    index = some_string.find(key)

    # ex: '... >Unit 10<...'
    if some_string[index-1] == ">":
        ench = "<"

    elif some_string[index-1] == ";":
        ench = "&"
    else:
        ench = None
    
    if ench == None:
        return
    
    substring = some_string[index:]
    endex = substring.find(ench) + int(index)


    cleaned_string = some_string[index:endex]

    if len(cleaned_string) > 50:
        cleaned_string = None
     
    return cleaned_string
##############


UnitsAll = []
#Unit 1 has a space because otherwise it gets confused for Unit 10
calico = ["Unit 1 ", "Unit 2", "Unit 3", "Unit 4", "Unit 5", "Unit 6", "Unit 7", "Unit 8", "Unit 9", "Unit 10"]

# IMPORTANT. These are what tell the helper to NOT look for. you may need to change these based on how the teacher formats things
cleankeys = ["Reading", "Learning Activities", "Overview"] 

readyfiles = os.listdir(readydir)
coursefile = readyfiles[0]

with open(str(readydir + "\\" + coursefile), 'rb') as file:

    lines = file.readlines()

    file.close


for each in calico:
    unit = []
    for line in lines:
        if each in str(line):
            #option 1
            unit = form_extract(str(line), each)
            ###    

            #option 2
            # tabby = carrot_extract(str(line), each)
            # if tabby == each:
            #     continue
            # elif tabby not in unit:
            #     print("::: ", tabby)
            #     unit.append(tabby)
            ###
    UnitsAll.append(unit)

CleanUnits = []
Final = []
for each in UnitsAll:
    each = [i for i in each if i != calico[UnitsAll.index(each)]]
    each = [i for i in each if i != None]

    CleanUnits.append(each)

for item in CleanUnits:
    clean = []
    for ea in item:
        for k in cleankeys:
            if k in ea:
                clean.append(ea)
    res = [i for i in item if i not in clean]
    Final.append(res)


index = 0
for each in calico:
    
    if (calico.index(each) == 0):
        print(each[:-1])
    else:
        print(each)
    
    for i in Final[index]:
        print(i, "\n")
    
    print("\n")
    index += 1