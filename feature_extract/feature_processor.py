from .feature_consts import *


class FeatureProcessor:

    def __init__(self, nlp):
        self.nlp = nlp

    def __call__(self, text):
        return self.model_process(text)

    def model_process(self, text):

        doc = self.nlp(text)
        docl = self.nlp(text.lower())
        curr_trunc = None
        keep_toks = []
        for index, token in enumerate(doc):
            if (token.is_stop):
                pass
            elif (index < len(docl) and docl[index].is_stop):
                pass
            elif any([regex.match(token.text) for regex in REGEXES ]):
                pass
            elif (token.text in PUNKT_PREPROCESS):
                pass
            elif (token.pos_ in POS_IGNORE):
                pass
            elif curr_trunc:
                found_ende = [p for p in possible_integrator if token.lemma_.lower().endswith(p)]
                if (len(found_ende) > 0):

                    keep_toks.append(curr_trunc+found_ende[0])
                else:
                    keep_toks.append(curr_trunc)
                keep_toks.append(token.lemma_)
                curr_trunc = None
            else:
                if (token.tag_ == "TRUNC" and token.text[-1] == '-'):
                    curr_trunc = token.text[:-1]
                elif token.pos_ == "VERB":
                    sep_part = [x for x in token.children if x.tag_ == "PTKVZ"
                                and x.text in GERMAN_SEPARABLE ]
                    if (len(sep_part) > 0):
                        to_app = sep_part[0].text+token.lemma_.lower()

                        keep_toks.append(to_app)
                    else:
                        keep_toks.append(token.lemma_)

                elif (index < len(docl) and docl[index].pos_ == "VERB") and any([x for x in docl[index].children if x.tag_ == "PTKVZ" and x.text in GERMAN_SEPARABLE ]):
                    sep_part = [x for x in docl[index].children if x.tag_ == "PTKVZ"
                                and x.text in GERMAN_SEPARABLE]
                    if (len(sep_part) > 0):
                        to_app = sep_part[0].text + docl[index].lemma_.lower()

                        keep_toks.append(to_app)
                elif (index < len(docl)      and docl[index].pos_ == "VERB") and (docl[index].lemma_ != docl[index].text):
                    keep_toks.append(docl[index].lemma_)
                else:
                    keep_toks.append(token.lemma_)


        return " ".join(keep_toks)

