import regex
REGEXES = [regex.compile('\b\d+\b'),regex.compile('\b\d+\.\b'), regex.compile('\b\d+\.\d+\b')]
POS_IGNORE = ["CONJ", "CCONJ", "DET", "NUM", "PRON", "PUNCT", "SYM", "PART",  ]

possible_integrator = ["girokonto",  "konto", "einlagen", "behörden", "einstellung", "auszahlung", "verzeichnis","name", "namens", "bank","banken","prozess","verhältnisse","vereinbarungen", "checks", "check", "fristen", "beratung", "kunde", "kunden", "adresse", "daten", "informationen", "spanne", "sprachen", "sprache", "planung", "bescheid", "situation", "verwaltung", "amt", "schulden", "zahlung", "gefühle", "beratungsstelle", "stunden", "beschluss", "schaden", "pfändung", "versicherung", "vertrag", "abtretung", "anteil", "verfahren", "gesellschaft", "datum", "kosten", "kurs", "transaktion", "order" , "verbot", "freiheit", "nummer", "gremium", "kammer", "unabhängig", "system", "limit", "eingang", "ausgang", "gang", "verfahren", "posten", "vereinbarung", "form", "phase", "teile", "teil", "vollmacht", "zertifikat", "rückgabe", "auszug", "abrechnung", "pfändung", "standard", "zugangs-kanal", "überweisung"]


GERMAN_SEPARABLE = ["an", "ab", "auf", "aus", "ein", "bei", "heim", "her", "heraus", "herein", "herauf", "hin", "hinauf", "hinaus", "hinein", "los", "mit", "nach", "vor", "weg", "zu", "zurück", "durch", "über", "um", "unter", "wider", "wieder"]


month_names = ["Januar", "Februar", "März", "April",  "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
month_name = "Monatsname"
IBAN_REGEX = regex.compile('DE\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{2}|DE\d{20}')