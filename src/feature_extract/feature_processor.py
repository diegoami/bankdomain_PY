import logging
from .feature_consts import *
from common import replace_strings
from .bundeslaender import *
from .countries import *
from .towns import *
from .nationalities import *
DATE_REGEX = regex.compile('\b[0-9]{1,2}\.[0-9]{1,2}\.([0-9]{4})?\b')
import regex
class FeatureProcessor:

    def __init__(self, nlp):
        self.nlp = nlp


    def __call__(self, text):
        text = self.replace_concepts(text)
        if (text.lower() != text):
            text_out = ""
            doc = self.nlp(text)
            for sent in doc.sents:
                sent_out = self.model_process(sent.text)
                text_out = text_out +" " +sent_out;
            if (len(text_out.strip()) == 0):
                text_out = self.model_process(text)
            if (len(text_out.strip()) > 0):
                text = text_out.strip()
        return text

    def replace_concepts(self, text):
        text = replace_strings(text, month_names, month_name)
        text = replace_strings(text, countries, country)
        text = replace_strings(text, towns, town)
        text = replace_strings(text, bundeslaender, bundesland)
        text = replace_strings(text, nationalities, nationality)
        text = DATE_REGEX.sub('IBAN', text)

        return text

    def model_process(self, text):

        doc = self.nlp(text)
        textl = text[0].lower() + text[1:]
        docl = self.nlp(textl )
        curr_truncs = []
        keep_toks = []
        for index, token in enumerate(doc):

            if (token.is_stop):
                pass
            elif (index < len(docl) and docl[index].is_stop):
                pass
            elif any([regex.match(token.text) for regex in REGEXES ]):
                pass
            elif (token.is_punct):
                pass
            elif (token.pos_ in POS_IGNORE):

                pass
            elif curr_truncs and token.pos_ == "NOUN":
                found_ende = [p for p in possible_integrator if token.lemma_.lower().endswith(p)]
                for curr_trunc in curr_truncs:
                    if (len(found_ende) > 0):

                        keep_toks.append(curr_trunc+found_ende[0])
                    else:
                        keep_toks.append(curr_trunc)
                    keep_toks.append(token.lemma_)
                curr_truncs = []
            else:
                if (token.tag_ == "TRUNC" and token.text[-1] == '-'):
                    curr_trunc = token.text[:-1]
                    curr_truncs.append(curr_trunc)
                elif token.pos_ == "VERB":
                    sep_part = [x for x in token.children if x.tag_ == "PTKVZ"
                                and x.text in GERMAN_SEPARABLE ]
                    if (len(sep_part) > 0):
                        to_app = sep_part[0].text+token.lemma_.lower()

                        keep_toks.append(to_app)
                    else:
                        keep_toks.append(token.lemma_)

                elif index < len(docl) and docl[index].pos_ == "VERB" and any([x for x in docl[index].children if x.tag_ == "PTKVZ" and x.text in GERMAN_SEPARABLE ]):
                    sep_part = [x for x in docl[index].children if x.tag_ == "PTKVZ"
                                and x.text in GERMAN_SEPARABLE]
                    if (len(sep_part) > 0):
                        to_app = sep_part[0].text + docl[index].lemma_.lower()

                        keep_toks.append(to_app)
                elif (index < len(docl)      and docl[index].pos_ in ["VERB", "ADJ"]) and (docl[index].lemma_ != docl[index].text):
                    keep_toks.append(docl[index].lemma_)
                else:
                    keep_toks.append(token.lemma_)


        return " ".join(keep_toks)

