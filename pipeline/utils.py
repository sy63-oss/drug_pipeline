from datetime import datetime

def normalize_date(raw: str) -> str:
    """Retourne la date au format YYYY-MM-DD"""
    formats = [
        "%d/%m/%Y",  #01/01/2020
        "%Y-%m-%d", # 2020-01-01
        "%d %B %Y", # 1 January 2020
        "%d %b %Y",   # 27 April 2020 (abbreviations)

    ]
    for fmt in formats:
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Format de date non reconnu : {raw!r}")