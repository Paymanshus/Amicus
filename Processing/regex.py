# ----------------------------
# Importing Standard Packages
# ----------------------------
import numpy as np
import pandas as pd
import re
import string


# ----------------------------------
# Returning Citations for Every Case
# ----------------------------------
def getCitations(caseFile):
    # Removing All The Escape Sequences In The Text
    text = re.sub('\n', '', caseFile)

    # Finding All the Places v. occurs in the case file
    cites = re.finditer("v[.]", text)

    citations = []
    for cite in cites:
        # Getting Position Of v.
        start = cite.start()
        end = cite.end()

        # Approximating a Range For The Rest of the citations with 'v.' in the centre
        temp = text[start - 75 : end + 350]

        # Finding Quotation - almost always inside paranthesis
        start = temp.find('(')
        end = temp.find('.)')
        temp = temp[start + 1 : end + 1]
        
        # Handling Multiple Quotations inside single paranthesis separated by ';'
        temp = temp.split(';')
        for j in temp:
            # Only Adding The Citation if Each Part Of the Separated Citation is a citation itself
            if re.search('[ ]+[v]+[.]+', j):
                citations.append(j.strip())

    # Removing Redundant Values From Printing   
    citations = list(set(citations))
    # For Printing Uncomment Next 2 Lines
    # for citation in citations:
    #     print(f'{citation} \n-----')

    return citations


# --------------------------------------------
# 🛑🛑🛑 Returning Sections Referred To In Every Case Incomplete 🛑🛑🛑
# --------------------------------------------
def getSections(caseFile):
    # Removing Escape Sequences For Easier Processing
    text = re.sub('\n', '', caseFile)

    # Making List For All Relevant Extractions
    rulesOfCourt = []
    w = re.findall("[s|S]+ection [\d]+.[\d]*[(]*[\w]*[)]* [[of the]+ [\w]* [\w]*]*", text)
    x = re.findall("[s|S]+ection\s[\d]+.[\d]*[(]?[\w]*[)]?", text)

    # Extracting Rules of Court
    rulesOfCourt = re.findall("Cal. Rules of Court, rule [\d]+.[\d]+", text)
    z = re.findall("rule [\d]+.[\d]+", text)
    j = re.findall('[[\w.]* [c|C]ode.]? § [\d]+.[\d]*[(]*[\w]*[)]*', text)     #for section symbol press ALT + 0167 to get §
    k = re.findall('§ [\d]+.[\d]*[(]*[\w]*[)]*[)]? ',text)

    # Removing Redundant Values from The Findings
    x = list(set(x))
    rulesOfCourt = list(set(rulesOfCourt)) 
    z = list(set(z))
    w = list(set(w))

    # For Printing uncomment the two below lines
    # print('For Case {}: \nSections: {} \nSections: {} \nSection symbol: {} \nRules: {} \nRules: {}\n'.format(i, x, w, j+k, y, z))
    #   print('For case {}: \n Section: {}\n'.format(i, j+k))
    return w, x, z, rulesOfCourt, j, k