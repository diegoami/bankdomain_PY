import regex
REGEXES = [regex.compile('\b\d+\b'),regex.compile('\b\d+\.\b'), regex.compile('\b\d+\.\d+\b')]
POS_IGNORE = ["CONJ", "CCONJ", "DET", "NUM", "PRON", "PUNCT", "SYM", "PART",  ]

PUNKT_PREPROCESS = ["/", "<", ">", "*", "=", "–", "+", "·", "|",  "1", "2", "3", "t", "x", "4", "5", "…", "#", "[", "]", "_"]

possible_integrator = ["girokonto",  "konto", "einlagen", "behörden", "einstellung", "auszahlung", "verzeichnis","name", "namens", "bank","banken","prozess","verhältnisse","vereinbarungen", "checks", "check", "fristen", "beratung", "kunde", "kunden", "adresse", "daten", "informationen", "spanne", "sprachen", "sprache", "planung", "bescheid", "situation", "verwaltung", "amt", "schulden", "zahlung", "gefühle", "beratungsstelle", "stunden", "beschluss", "schaden", "pfändung", "versicherung", "vertrag", "abtretung", "anteil", "verfahren", "gesellschaft", "datum", "kosten", "kurs", "transaktion", "order" , "verbot", "freiheit", "nummer", "gremium", "kammer", "unabhängig", "system", "limit", "eingang", "ausgang", "gang", "verfahren", "posten", "vereinbarung", "form", "phase", "teile", "teil", "vollmacht", "zertifikat"]


GERMAN_SEPARABLE = ["an", "ab", "auf", "aus", "ein", "bei", "heim", "her", "heraus", "herein", "herauf", "hin", "hinauf", "hinaus", "hinein", "los", "mit", "nach", "vor", "weg", "zu", "zurück", "durch", "über", "um", "unter", "wider", "wieder"]
