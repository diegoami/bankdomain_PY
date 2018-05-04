CUSTOM_STOP_WORDS  = set("""
 above aufgrund and auf Auf at At
 Bei bevor bezüglich
 c
 d daraufhin demnach dennoch desto Da dass diesbezüglich
 e ein Ein ehe Ehe
 f
 falls
 fast
 Ferner ferner
 
 h. hierbei hierdurch hierfür hingegen hiervon
 in In
 innen im Im 
 jeweils
 meist Meist mittels Mit
 n
 ok of oftmals Oftmals or
 sobald sodass sofern sogar solange somit soweit
 t
 u.
 unten Unten
 x
 unter Unter
 via vorab voraus
 weg wobei Wobei wozo Wozu
 wenn Wenn wieso woher Woher
 zudem
 zugunsten
 zuvor
""".split())

def add_stop_words(nlp):
    for word in CUSTOM_STOP_WORDS:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True
