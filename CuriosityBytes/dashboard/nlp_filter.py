import spacy

nlp = spacy.load('en_core_web_sm')

def is_educational(text):
    doc = nlp(text.lower())
    
    education_keywords = ['tutorial', 'lesson', 'course', 'education', 'learning', 'study', 'guide', 'career']

    for token in doc:
        if token.text in education_keywords:
            return True
    return False
