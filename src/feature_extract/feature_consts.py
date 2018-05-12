import regex
REGEXES = [regex.compile('\b\d+\b'),regex.compile('\b\d+\.\b'), regex.compile('\b\d+\.\d+\b')]
POS_IGNORE = ["CONJ", "CCONJ", "DET", "NUM", "PRON", "PUNCT", "SYM", "PART",  ]

possible_integrator = ["landsüberweisung", "überweisung", "girokonto", "kredit", "konto", "einlage", "behörde", "einstellung", "auszahlung", "verzeichnis", "name", "namen", "bank", "prozess","verhältnis", "vereinbarung", "check", "fristen", "beratung", "kunde",  "adresse", "daten", "datum", "informationen", "spanne",  "sprache", "planung", "bescheid", "situation", "verwaltung", "amt", "schulden",  "schuld", "zahlung", "gefühl", "beratungsstelle", "stunden", "stunde", "beschluss", "schaden", "pfändung", "versicherung", "vertrag", "abtretung", "anteil", "verfahren", "gesellschaft", "kosten", "kost", "kurs", "transaktion", "order" , "verbot", "freiheit", "nummer", "gremium", "kammer", "unabhängig", "system", "limit", "eingang", "ausgang", "gang", "verfahren", "posten", "vereinbarung", "form", "phase", "teil", "vollmacht", "zertifikat", "rückgabe", "auszug", "abrechnung", "pfändung", "standard", "zugangs-kanal", "geld", "fall", "antrag", "erklärung", "guthaben" ]


GERMAN_SEPARABLE = ["an", "ab", "auf", "aus", "ein", "bei", "heim", "her", "heraus", "herein", "herauf", "hin", "hinauf", "hinaus", "hinein", "los", "mit", "nach", "vor", "weg", "zu", "zurück", "durch", "über", "um", "unter", "wider", "wieder"]


month_names = ["Januar", "Februar", "März", "April",  "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
month_name = "Monatsname"
