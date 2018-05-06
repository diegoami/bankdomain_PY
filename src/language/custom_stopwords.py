CUSTOM_STOP_WORDS  = set("""
 --
 1 2 3 4 5
 above aufgrund and auf Auf at At aufs als Als
 Bei bevor bezüglich bitte Bitte
 c
 d daraufhin demnach dennoch desto Da dass diesbezüglich das Das    
 e ein Ein ehe Ehe eher Eher
 f
 falls
 fast for For
 Ferner ferner fürs Fürs
 
 h. hierbei hierdurch hierfür hingegen hiervon hinaus hierzu Hierzu
 in In insoweit Insoweit
 innen im Im 
 jeweils
 meist Meist mittels Mit mitunter Mitunter mitsamt Mitsamt manchmal Manchmal
 n
 ok of oftmals Oftmals or
 sobald sodass sofern sogar solange somit soweit stattdessen seit Seit
 t
 u.
 unten Unten
 x
 umso 
 unter Unter
 via vorab voraus
 weg Weg wobei Wobei wozu Wozu Weg wofür Wofür weiterhin Weiterhin
 wenn Wenn wieso woher Woher wonach Wonach worauf Worauf woran Woran
 zudem
 zugunsten
 zuvor
""".split())


PUNKT_PREPROCESS = ["/", "<", ">", "*", "=", "–", "+", "·", "|", "%",  "…", "#", "[", "]", "_", "®", "™", "•", "@"]

def add_stop_words(nlp):
    for word in CUSTOM_STOP_WORDS:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True
    for word in PUNKT_PREPROCESS:
        lexeme = nlp.vocab[word]
        lexeme.is_punct = True

