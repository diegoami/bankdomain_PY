REMOVE_WORDS = ["Falle", "Fallen"]

def remove_words(nlp):
    component = change_pos_component
    nlp.add_pipe(component, name='print_length', after='tagger')


def change_pos_component(doc):

    def get_pos_custom(token):
        if token.text in REMOVE_WORDS:
            return "VERB"
        else:
            return token.lemma_

    def get_tag_custom(token):
        if token.tag_ in REMOVE_WORDS:
            return "VVFIN"
        else:
            return token.lemma_

    doc.user_token_hooks['lemma_'] = get_pos_custom
    doc.user_token_hooks['tag_'] = get_tag_custom
    return doc
