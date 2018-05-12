CUSTOM_STOP_WORDS  = set("""
 --
 1 2 3 4 5
 Ab ab an An
 above aufgrund and auf Auf at At aufs als Als am Am auch Auch außerdem	außerhalb Außerhalb Außerdem
 Allerdings allerdings andererseits Andererseits angesichts Angesichts
 Bei bevor bezüglich bitte Bitte beim Beim bereits Bereits bezüglich Bezüglich bis Bis
 c
 d daraufhin demnach dennoch desto Da dass diesbezüglich das Das davon Davon daher Daher deine Deine deines Deines  d
 dabei Dabei damit Damit dazu Dazu danach Danach dort Dort darüber Darüber durch Durch dann Dann derzeit Derzeit
 darf Darf demnächst Demnächst
 e ein Ein ehe Ehe eher Eher einfach Einfach ebenfalls Ebenfalls
 einerseits Einerseits
 f ggf ggf. 
 falls
 fast for For
 Ferner ferner fürs Fürs für Für 
 geht´s gerne
 Hast hast
 h. hierbei hierdurch hierfür hingegen hiervon hinaus hierzu Hierzu hier Hier Hierdurch 
 in In insoweit Insoweit ist Ist 
 Ihrer Ihres Ihre Ihrem Ihren
 innen im Im innerhalb Innerhalb insbesondere insbesonders Insbesondere Insbesonders insgesamt Insgesamt
 jeweils jetzt Jetzt je Je
 klicken Klicken 
 lediglich Lediglich
 meist Meist mittels Mit mitunter Mitunter mitsamt Mitsamt manchmal Manchmal mindestens Mindestens möchten Möchten
 n N nebst Nebst nur Nur nachdem Nachdem nach Nach nämlich Nämlich
 ok of oftmals Oftmals or  
 sobald sodass sofern sogar solange somit soweit stattdessen seit Seit s S so So    Sie sie sofern Sofern sollte Sollte stets Stets
 t T 
 u. über Über
 unten Unten
 x X 
 umso um Um Umso
 unter Unter
 via vorab voraus vielmehr Vielmehr voneinander Voneinander
 weg Weg wobei Wobei wozu Wozu Weg wofür Wofür weiterhin Weiterhin wann Wann wie Wie wohin Wohin
 wenn Wenn wieso woher Woher wonach Wonach worauf Worauf woran Woran weshalb Weshalb warum Warum wo Wo wird Wird worin Worin
 zudem zumal Zumal Zudem zum Zum zur Zur
 zugunsten 
 zuvor zu Zu 
""".split())


PUNKT_PREPROCESS = ["/", "<", ">", "*", "=", "–", "+", "·", "|", "%",  "…", "#", "[", "]", "_", "®", "™", "•", "@", "⚙", "➜", ""]

def add_stop_words(nlp):
    for word in CUSTOM_STOP_WORDS:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True
    for word in PUNKT_PREPROCESS:
        lexeme = nlp.vocab[word]
        lexeme.is_punct = True

