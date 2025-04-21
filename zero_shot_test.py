
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Your predefined legal categories 
labels = [
    "Contract dispute",
    "Criminal offense",
    "Loan default",
    "Cheque bounce case",
    "Property dispute",
    "Family law case",
    "Employment issue",
    "Tax-related case",
    "Bail application"
]

def classifycase(case_text):
    result = classifier(case_text, candidate_labels=labels)
    return result

