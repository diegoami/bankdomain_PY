CUSTOM_STOP_WORDS  = set("""
 --
 1 2 3 4 5
 Ab ab an An anstatt Anstatt A a
 above aufgrund and auf Auf at At aufs als Als am Am auch Auch außerdem	außerhalb Außerhalb Außerdem
 Allerdings allerdings andererseits Andererseits angesichts Angesichts
 Bei bevor bezüglich bitte Bitte beim Beim bereits Bereits bezüglich Bezüglich bis Bis bislang Bislang bestens Bestens
 c
 d daraufhin Daraufhin demnach dennoch Dennoch desto Da dass diesbezüglich das Das davon Davon daher Daher deine Deine deines Deines  d
 dabei Dabei damit Damit dazu Dazu danach Danach dort Dort darüber Darüber durch Durch dann Dann derzeit Derzeit daneben Daneben
 darf Darf demnächst Demnächst darin Darin
 e ein Ein ehe Ehe eher Eher einfach Einfach ebenfalls Ebenfalls
 einerseits Einerseits ebenso Ebenso erstmals Erstmals
 f ggf ggf. 
 falls
 fast for For
 Ferner ferner fürs Fürs für Für 
 geht´s gerne
 Hast hast
 h. hierbei hierdurch hierfür hingegen hiervon hinaus hierzu Hierzu hier Hier Hierdurch 
 in In insoweit Insoweit ist Ist 
 Ihrer Ihres Ihre Ihrem Ihren immer Immer
 innen im Im innerhalb Innerhalb insbesondere insbesonders Insbesondere Insbesonders insgesamt Insgesamt
 jeweils jetzt Jetzt je Je jedoch Jedoch ja Ja
 klicken Klicken 
 lediglich Lediglich
 meist Meist mittels Mit mitunter Mitunter mitsamt Mitsamt manchmal Manchmal mindestens Mindestens möchten Möchten
 n N nebst Nebst nur Nur nachdem Nachdem nach Nach nämlich Nämlich nun Nun nahezu Nahezu noch Noch nein Nein
 ok of oftmals Oftmals or ohnehin Ohnehin
 sobald sodass sofern sogar solange Solange somit soweit stattdessen seit Seit s S so So    Sie sie sofern Sofern sollte Sollte stets Stets
 soweit Soweit statt Statt
 r R
 t T 
 u. über Über
 unten Unten 
 x X 
 umso um Um Umso und Und
 unter Unter
 via vorab voraus vielmehr Vielmehr voneinander Voneinander vor Vor vielleicht Vielleicht
 weg Weg wobei Wobei wozu Wozu Weg wofür Wofür weiterhin Weiterhin wann Wann wie Wie wohin Wohin wodurch Wodurch wieso Wieso
 wenn Wenn wieso woher Woher wonach Wonach worauf Worauf woran Woran weshalb Weshalb warum Warum wo Wo wird Wird worin Worin weil Weil wiederum Wiederum
 zudem zumal Zumal Zudem zum Zum zur Zur
 zugunsten 
 zuvor zu Zu zuletzt Zuletzt
""".split())


PUNKT_PREPROCESS = ["/", "<", ">", "*", "=", "–", "+", "·", "|", "%",  "…", "#", "[", "]", "_", "®", "™", "•", "@", "⚙", "➜", ""]

def add_stop_words(nlp):
    for word in CUSTOM_STOP_WORDS:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True
    for word in PUNKT_PREPROCESS:
        lexeme = nlp.vocab[word]
        lexeme.is_punct = True

