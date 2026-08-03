import re
from html import unescape

#Data cleanup functions for datasets, likely every source will be a little different

## This function is used to clean HTML content from the Wahapedia data. It unescapes HTML entities, removes HTML tags, and normalizes whitespace.
def clean_html_waha(text):
    if not isinstance(text, str):
        return text
    text = unescape(text)
    
    text = re.sub(r'<[^>]+>', ' ', text)

    text = text.replace('\u2019', "'")  # right single quote
    text = text.replace('\u2018', "'")  # left single quote
    text = text.replace('\u201c', '"')  # left double quote
    text = text.replace('\u201d', '"')  # right double quote
    text = text.replace('\u2013', '-')  # en dash
    text = text.replace('\u2014', '-')  # em dash
    text = text.replace('\u00fb', 'u')  # û
    text = text.replace('\u2011', '-')  # non-breaking hyphen

    text = re.sub(r'\s+', ' ', text).strip()

    return text