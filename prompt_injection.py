import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
model = AutoModelForSequenceClassification.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, truncation=True, 
                      max_length=512, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

def load_keywords(filename="keywords.txt"):
    with open(filename, "r") as file:
        keywords = [line.strip().lower() for line in file]
    return keywords

def load_regex_patterns(filename="regex_patterns.txt"):
    with open(filename, "r") as file:
        patterns = [line.strip() for line in file]
    return patterns

def detect_keywords(prompt):  
    keywords=load_keywords()
    for word in prompt.lower().split(): 
       if word in keywords:
           return True
    return False

def detect_suspicious_patterns(prompt):
    regex_patterns = load_regex_patterns()

    for pattern in regex_patterns:
        if re.search(pattern, prompt, flags=re.IGNORECASE):
            return True
    return False

def detect_model_injection(prompt, threshold):
    results = classifier(prompt)

    highest_injection_score = 0.0

    for result in results:
        if result['label'].upper() == "INJECTION" and result['score'] > highest_injection_score:
            highest_injection_score = result['score']

    is_injection = highest_injection_score >= threshold
    return is_injection, highest_injection_score 




