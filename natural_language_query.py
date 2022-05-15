from typing import Union, Iterator, Generator, Any, List

import preshed
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

import thinc
from bs4 import BeautifulSoup
from bs4.element import ContentMetaAttributeValue
import spacy
from cymem import cymem
from spacy import Language
from spacy.tokens import Doc, Span
from spacy.matcher import Matcher

nlp: Language = spacy.load("en_core_web_sm")

"""
# Real-estate investment analysis
Enter information about price, size, and rent in the area of possible property.

"""


def get_listing(url):
    return BeautifulSoup(requests.get(url).content, "html.parser")


spacy_hashin = {
    preshed.maps.PreshMap: hash,
    cymem.Pool: hash,
    thinc.model.Model: hash,
    spacy.pipeline.tok2vec.Tok2VecListener: hash,
    spacy.tokens.doc.Doc: hash
}


@st.cache(hash_funcs=spacy_hashin)
def analyse(text: str) -> Union[Doc, Doc]:
    res: Union[Doc, Doc] = nlp(text)
    return res


with st.sidebar:
    st.header("Inputs")
    st.subheader("Real-estate investment analysis")

    url = st.text_input("Link to property")
    if url:
        r = get_listing(url)
    details = r.find_all("li", {"class": "details-component"})
    doc = analyse(r.text)
    # st.code(entities.ents)
    #
    # for component in details:
    #     st.code(component.text)
    # st.code(details)

    price = r.find("span", {"class": "price"})
    price = r.find("span", {"class": "price"})
    currency = r.find("span", {"class": "currency-left"})
    st.write(f"Price: {price.text} {currency.text}")


# st.code(r.prettify())
# import spacy_streamlit

# spacy_streamlit.visualize(['en_core_web_sm'], r.text)
#
# for token in doc:
#     st.write(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)


# for token in doc:
#     st.write(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])


# for match_id, start, end in matches:
#     span = doc[start:end]
#
#     st.write(span.text)
# def extract(doc, type, label, lefts=[], rights=[]):
#     matcher = Matcher(nlp.vocab)
#     matcher.add(label, [[{'ENT_TYPE': type}]])
#     matches = matcher(doc, as_spans=True)
#     print("Matches:")
#     for span in matches:
#         print('match:\t', span, span. span.label_, [left for left in span.lefts], [right for right in span.rights])
#         if span.label_ == label:
#             if len(lefts) > 0 and any([left in [span_left.text for span_left in span.lefts] for left in lefts]):
#                 return span
#             if len(rights) > 0 and any([right in [span_right.text for span_right in span.rights] for right in rights]):
#                 return span
#             if len(lefts) == 0 and len(rights) == 0:
#                 return span


def extract(doc: Doc, label: str, features: List, predicates: List = [], strict: bool = True):
    matcher = Matcher(nlp.vocab)
    matcher.add(label, [features])
    matches = matcher(doc, as_spans=True)

    # print(f"Matches: {len(matches)}")

    for span in matches:
        if len(predicates) == 0:
            yield span
        if strict:
            if all(predicate(span) for predicate in predicates):
                # print('tight match:\t', span, [left for left in span.lefts], [right for right in span.rights])
                yield span
        else:
            if any(predicate(span) for predicate in predicates):
                # print('loose match:\t', span, [left for left in span.lefts], [right for right in span.rights])
                yield span


def left(text):
    return lambda span: text in [left.text for left in span.lefts]


for p in set(extract(doc, 'price', [{'ENT_TYPE': 'MONEY', 'POS': 'NUM'}])):
    st.write(p.label_, p, '€')

for p in set(extract(doc, 'land', [{'ENT_TYPE': 'CARDINAL', 'POS': 'NUM'}], [left('Land')])):
    st.write(p.label_, p)

for p in set(extract(doc, 'area', [{'ENT_TYPE': 'CARDINAL', 'DEP': 'NUMMOD', }])):
    st.write(p.label_, p)
# st.write('price', price)
# st.write('rooms', rooms)


st.json([{
    'text': token.text,
    'dep': token.dep_,
    'head.text': token.head.text,
    'head.pos': token.head.pos_,
    'children': [child for child in token.children],
    'lefts': [left for left in token.lefts],
    'rights': [right for right in token.rights],
    'ent_type': token.ent_type_,
    'emt_iob': token.ent_iob_,
} for token in doc])
