from language import NlpWrapper
from feature_extract import FeatureProcessor

if __name__ == '__main__':
    nlp = NlpWrapper()
    feature_processor = FeatureProcessor(nlp)
    print(feature_processor(
        "Alle Unterlagen senden Sie uns vollständig ausgefüllt und unterschrieben retour."))
    print(feature_processor(
        "Unten Ein DepotPlus können Sie ausschließlich online unter dem unten genannten Link eröffnen."))
    print(feature_processor(
        "Bestätigen Sie diesen Auftrag im Anschluss mit einer iTAN oder mTAN"))

    print(feature_processor(
        "Fallen zusätzliche Kosten bei der Nutzung der Versicherungen meiner Karten an?"))

    print(feature_processor("Ferner bieten wir interessante und leistungsstarke Fonds sowie ein wachsendes Angebot attraktiver Fonds von führenden Investmentgesellschaften an."))
    print(feature_processor(
        "Was sollte ich tun, wenn ich glaube, dass auf mein Konto zugegriffen wurde?"))
    print(feature_processor(
        "Jedes Mal, wenn Sie auf Kontoinformationen in einem Ihrer sicheren Online-Bereiche zugreifen oder diese mitteilen, werden diese Informationen durch eine Technologie namens Secure Sockets Layer, häufig abgekürzt als SSL verschlüsselt."))
    print(feature_processor(
        "Das Tagesgeldkonto ist ein kostenfreies, sehr gut verzinstes Anlagekonto mit täglicher Verfügbarkeit."))
    print(feature_processor(
        "Die Regelung garantiert Sicht- und Spareinlagen sowie registrierte Schuldverschreibungen, Bankobligationen und Sparbriefe."))
    print(feature_processor(
        "Schutz für Giro- und Sparkonten (Tagesgeld- und Festgeldkonten)"))
    print(feature_processor(
        "Wichtig dabei ist, dass die Gutschrift von Ihrem Arbeitgeber korrekt als Lohn / Gehalt verschlüsselt wurde. Anderenfalls kann diese maschinell nicht als Lohn- / Gehaltseingang erkannt werden."))

    print(feature_processor(
        "Wenn Sie einen Computer benutzen, an dem auch andere arbeiten und Sie das ungute Gefühl haben, dass diese eventuell versteckte Seiten einsehen könnten, nachdem Sie die Station verlassen haben, beenden / verlassen Sie Ihre Browser-Software."))
    print(feature_processor(
        "Reichen Sie uns hierzu den Antrag der anderen Bank mit dem Hinweis auf Auszahlung der Niedrigzins-Garantie ein."))
    print(feature_processor(
        "Ein Dispo Antrag ist bei uns einfacher als bei vielen Filialbanken. Bonität vorausgesetzt, verläuft die Einrichtung Deines Disporahmens schnell und mit nur wenigen Angaben. Der Dispo hilft Dir, wenn Du Dein Konto kurzfristig überziehen möchtest."))
    



    print(feature_processor(
        "Häufig reicht es auch, eine längere Laufzeit zu wählen, und dadurch die monatliche Belastung zu reduzieren."))

    print(feature_processor(
        "Genossenschaftsbanken, Sparkassen und die Groß- und Privatbanken haben ein eigenes Online-Bezahlverfahren \"paydirekt\" entwickelt. Mit paydirekt können Sie mit Ihrem Girokonto im Internethandel direkt, sicher und einfach bezahlen."))

    print(feature_processor(
        "Sondertilgungen und vorzeitige Rückzahlungen von Teilbeträgen sind jederzeit kostenfrei möglich."))
    print(feature_processor(
        "Wann wird eine Entschädigung für Einlagen gezahlt?"))
    print(feature_processor(
        "Falls Du Deine Kreditkarte noch nicht bei 3D Secure registriert hast, empfehlen wir, dies vorab über die Website Deiner Bank durchzuführen"))
    print(feature_processor(
        "Sobald Du DidiPay auf dem neuen Smartphone  ( NFC-fähig, Android 4.4 oder höher )  installiert hast, kannst Du Dich mit Deinen existierenden Zugangsdaten einloggen."))

    print(feature_processor(
        "Bitte beachten Sie, dass das \"Verstecken\" die Sicherheit Ihrer vertraulichen Benutzer-ID oder Ihres Passworts in keiner Weise beeinflusst. Wenn Sie einen Computer an einem öffentlichen Ort verwenden, lesen Sie bitte den folgenden Absatz 'Was sollte ich tun, wenn ich einen \"öffentlichen\" Computer benutze?'"))
    print(feature_processor(
        "Bitte beachten Sie, dass das \"Verstecken\" die Sicherheit Ihrer vertraulichen Benutzer-ID oder Ihres Passworts in keiner Weise beeinflusst. Wenn Sie einen Computer an einem öffentlichen Ort verwenden, lesen Sie bitte den folgenden Absatz 'Was sollte ich tun, wenn ich einen \"öffentlichen\" Computer benutze?'"))
