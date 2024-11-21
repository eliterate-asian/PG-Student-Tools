import email
from bs4 import BeautifulSoup
import os
import re


# INSTRUCTIONS
# Save an HTML SINGLE PAGE file of the Discussions List page of the given course (url will be something like "https://purdueglobal.brightspace.com/d2l/le/314989/discussions/List")
workingdir = os.path.dirname(os.path.realpath(__file__))
readydir = str(workingdir + "\\ready\\")

readyfiles = os.listdir(readydir)
coursefile = readyfiles[0]


def reform_unit_block(some_data, key, keyphrase="Return to "):
    keymatch = str(keyphrase + key)
    indexes = []
    #print(keymatch)
    for index, match in enumerate(some_data):
        if keymatch in match:
            indexes.append(index)
    #print(indexes)
    if len(indexes) == 0:
        print("[ERROR] Failed to match keyphrase! Are we sure the data for this unit exists in the source?")
        return ["No data found."]

    return some_data[indexes[-2]:indexes[-1]]

def parse_mhtml(file_path):
    """Parses an MHTML file and extracts the HTML content."""

    with open(file_path, 'r') as fp:
        message = email.message_from_file(fp)

    for part in message.walk():
        if part.get_content_type() == 'text/html':
            soup = BeautifulSoup(part.get_payload(decode=True), 'html.parser')
            # Do something with the soup object, e.g., extract data
            return soup



########
if __name__ == '__main__':
    file_path = str(readydir + '\\' + coursefile)
    soup = parse_mhtml(file_path)
    div = soup.find_all('div')
    html_data = []

    for divi in div:
        inner_text = divi.text
        strings = inner_text.split("\n")

        html_data.extend([string for string in strings if string])

    units = ["Unit 1 ", "Unit 2", "Unit 3", "Unit 4", "Unit 5", "Unit 6", "Unit 7", "Unit 8", "Unit 9", "Unit 10"]

    html_data[:] = [x for x in html_data if len(x) >= 25 or "Unit" in x]
    for unit in units:

        print("\n\t",unit,"\n")
        print(" ".join(reform_unit_block(html_data, unit)[1:]))
        print("\n\n")
    #for i in html_data:
    #    print(i, "[LINE LINE]\n")


# with open(str(readydir + "\\" + coursefile), 'rb') as file:

#     lines = file.readlines()

#     file.close

# effort = 0

# print("\n\nBREAK BREAK BREAK\n")
# print(re.findall("<div class=3D\" d2l-discussions-topic-details-description\"=(.*?)</div>", str(lines))[1])
