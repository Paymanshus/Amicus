# TODO: Imrpove NER
#   - Check return, ask for usable format of list
#   - Dealing with misfires
#   - Combining BERT generated NER #s
# TODO: Recreate for Respondent Counsel
#   - Create combined function?
# TODO: Recreate functions in .py file
import pandas as pd

import re
from pprint import pprint
import string

# huggingface
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# SpaCy
# import spacy
from spacy import displacy
# from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()


# Spacy NER
def spacy_ner(text):
    res = nlp(text)
    displacy.render(res, jupyter=True, style='ent')

    return res

# Transformers NER


def ner_predict(text, model, tokenizer):
    nlp = pipeline("ner", model=model, tokenizer=tokenizer,
                   grouped_entities=True)
    ner_results = nlp(text)

    entity_list = [(i['word'], i['entity_group']) for i in ner_results]

    return ner_results, entity_list


def extract_petitioners(row, fl=2, print_st=True):

    sentences = row['CaseFile'].split('\n')

    # Pre Post sentence check
    appellant_sub = 'for Defendant'
    # flag = 0
    appellant_sentence = []

    for idx, sentence in enumerate(sentences):

        if re.search(appellant_sub, sentence):
            # flag = fl

            # Printing next (flag) number of lines and appending
            for i in range(fl):
                if print_st:
                    print(idx+i, ':', sentences[idx+i])
                appellant_sentence.append(sentences[idx+i])

    if print_st:
        print('\n')
        print(f"Extracted Appellant Sentence: {appellant_sentence}")

    # Keyword Removal
    things_to_remove = ['for', 'counsel', 'Counsel', 'Appellant', 'and Appellant' 'Petitioner', 'Defendant', 'Defendant and', 'Respondent', 'Appeal', 'under appointment by the Court of',
                        # 'and',
                        ]

    for i in things_to_remove:
        appellant_sentence = [(sub.replace(i, ''))
                              for sub in appellant_sentence]

    appellant_sentence = ' '.join(appellant_sentence)

    if print_st:
        print(f"Removed Sentence: {appellant_sentence}")

    # Running NER function
    if print_st:
        print("\nRunning NER on sentence")

        # DisplaCy
        spacy_ner(appellant_sentence)

    preds, entity_list = ner_predict(
        appellant_sentence, model_base, tokenizer_base)

    if print_st:
        print(f"\nResult of NER using Transformer {entity_list}")

    # Counsel list creation and processing
    counsel_list = appellant_sentence.split(',')
    counsel_list = [x.strip().strip('.') for x in counsel_list if x.split()]
    counsel_list = [x.replace('and', '').strip()
                    for x in counsel_list if x.replace('and', '').strip()]

    if print_st:
        print("\nRunning NER on list items")
        ner_list = [spacy_ner(x) for x in counsel_list]
        print(ner_list)
    if print_st:
        # vs NER Extracted: {ner_list}")
        print(f"Punctuation Removed: {counsel_list}")

    if print_st:
        print(f"Counsel present in table: {row['PetitionerCounsel']}")

    return counsel_list, appellant_sentence


def extract_respondents(row, fl=2, print_st=True):

    sentences = row['CaseFile'].split('\n')

    # Pre Post sentence check
    appellant_sub = ['for Plaintiff and Respondent', 'for Respondent',
                     'for Plaintiff', 'for\nPlaintiff', 'for Plaintiff/Respondent']
    # flag = 0
    respondent_sentence = []

    for phrase in appellant_sub:
        for idx, sentence in enumerate(sentences):

            if re.search(appellant_sub, sentence):
                # flag = fl

                # Printing next (flag) number of lines and appending
                for i in range(fl):
                    if print_st:
                        print(idx+i, ':', sentences[idx+i])
                    respondent_sentence.append(sentences[idx+i])

    if print_st:
        print('\n')
        print(f"Extracted Respondent Sentence: {respondent_sentence}")

    # Keyword Removal
    things_to_remove = ['for', 'counsel', 'Respondent', 'Plaintiff', 'Defendant', 'petitioner', 'Appellant', 'under appointment by the Court of',
                        'and'
                        ]

    for i in things_to_remove:
        respondent_sentence = [(sub.replace(i, ''))
                               for sub in respondent_sentence]

    respondent_sentence = ' '.join(respondent_sentence)

    if print_st:
        print(f"Removed Sentence: {respondent_sentence}")

    # Running NER function
    if print_st:
        print("\nRunning NER on sentence")

        # DisplaCy
        spacy_ner(respondent_sentence)

    preds, entity_list = ner_predict(
        respondent_sentence, model_base, tokenizer_base)

    if print_st:
        print(f"\nResult of NER using Transformer {entity_list}")

    # Counsel list creation and processing
    counsel_list = respondent_sentence.split(',')
    counsel_list = [x.strip().strip('.') for x in counsel_list if x.split()]
    counsel_list = [x.replace('and', '').strip()
                    for x in counsel_list if x.replace('and', '').strip()]

    if print_st:
        print("\nRunning NER on list items")
        ner_list = [spacy_ner(x) for x in counsel_list]
        print(ner_list)
    if print_st:
        # vs NER Extracted: {ner_list}")
        print(f"Punctuation Removed: {counsel_list}")

    if print_st:
        print(f"Counsel present in table: {row['PetitionerCounsel']}")

    return counsel_list, respondent_sentence


if __name__ == '__main__':
    df = pd.read_csv("/content/MyDrive/MyDrive/Amicus/BulkDataCleaned.csv")

    # NER Models
    # BERT base
    tokenizer_base = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model_base = AutoModelForTokenClassification.from_pretrained(
        "dslim/bert-base-NER")

    # distilBERT-base-cased
    tokenizer_distil_con = AutoTokenizer.from_pretrained(
        "elastic/distilbert-base-cased-finetuned-conll03-english")
    model_distil_con = AutoModelForTokenClassification.from_pretrained(
        "elastic/distilbert-base-cased-finetuned-conll03-english")
