import unicodedata

def normalize_text(text):
    if isinstance(text, str):
        text = unicodedata.normalize('NFKC', text)
        return " ".join(text.split())
    return text

def normalize_list(data):
    return [normalize_text(value) for value in data]

def convert_numeric_to_str(data):
    return {
        key: [normalize_text(str(value)) if isinstance(value, (int, float, str)) else value
              for value in values]
        for key, values in data.items()
    }


