from transformers import pipeline

def detect_hate_speech(text, threshold):
    def analyze_with_pipeline(text):  
        pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")
        result = pipe(text)
        label = result[0]['label']
        score = result[0]['score']
        return label, score
    label, score = analyze_with_pipeline(text)
    is_hate_speech = label == 'hate' and score >= threshold
    if label != 'hate':
        is_hate_speech = False
    return is_hate_speech, score
