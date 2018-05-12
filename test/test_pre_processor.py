from preprocess import Preprocessor

if __name__ == '__main__':
    preprocessor = Preprocessor()

    print(preprocessor(
        " Sollte Sie vorab Kontakt mit uns aufnehmen möchten, erreichen Sie uns über unseren telefonischen Kundenservice für Geschäftskunden unter ( 069 ) 910-10061."))
    print(preprocessor(
        "Sie können Ihre Buchungen telefonisch bei den Mitarbeitern unseres Call Center ( 0211-86 222 400 ) in Auftrag geben."))
    print(preprocessor(
        "Sie erreichen unsere Kundenberatung montags bis freitags in der Zeit von 8 bis 18 Uhr unter 069 719129-100"))
    print(preprocessor(
        "Die Schutzgemeinschaft für allgemeine Kreditsicherung  ( SCHUFA )  ist eine Gemeinschaftseinrichtung von Wirtschaftsunternehmen, die Ihren Kunden Geld- oder Warenkredite einräumen."))

    print(preprocessor(
        "Wo kann ich kostenlos Bargeld einzahlen, wenn ich mein Konto bei einer Direktbank habe?"))

    print(preprocessor(
        "Für die Klasse unseres Kindes soll ein Konto angelegt werden. Wie machen wir das am besten?"))

    print(preprocessor(
        "Verbindliche Erklärungen  ( z.B. die Unterzeichnung eines Kaufvertrages )  sollten Sie erst abgeben, wenn auch die Finanzierung steht. Sprechen Sie deshalb frühzeitig mit uns über Ihre Pläne. Denn schon bei der Suche nach dem Traumhaus können wir Ihnen mit unseren Immobilienberatern behilflich sein."))