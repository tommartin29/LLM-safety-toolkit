import torch
from scipy.special import softmax
import urllib.request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re
import csv

TASK = 'offensive'  
MODEL = f"cardiffnlp/twitter-roberta-base-{TASK}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

labels = []
with urllib.request.urlopen(f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{TASK}/mapping.txt") as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
    labels = [row[1] for row in csvreader if len(row) > 1]

def preprocess(text):
    # Lowercase
    text = text.lower()
    # Normalise URLs
    text = re.sub(r"https?://\S+", "http", text)
    return text 

def detect_offensive_language(text, threshold):
    preprocessed_text = preprocess(text)
    encoded_input = tokenizer(preprocessed_text, return_tensors='pt')

    with torch.no_grad():
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

    label_scores = {labels[i]: scores[i] for i in range(len(scores))}
    offensive_score = label_scores.get("offensive", 0)
    is_offensive = offensive_score >= threshold

    return offensive_score, is_offensive
