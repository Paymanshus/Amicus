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
        
    citations = list(set(citations))
    # For Printing Uncomment Next 2 Lines
    # for citation in citations:
    #     print(f'{citation} \n-----')

    return citations