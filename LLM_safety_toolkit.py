from prompt_injection import detect_model_injection
from detect_hate_speech import detect_hate_speech
from detect_offensive_language import detect_offensive_language
from concurrent.futures import ThreadPoolExecutor

def prompt_safety_check(prompt, check_hate_speech=False, check_prompt_injection=False, check_offensive=False, injection_confidence_threshold=0.8, offensive_threshold=0.6, hate_speech_confidence_threshold=0.8, concurrent=True):
    results = {"text": prompt}

    def add_result(key, condition, score):
        results[key] = bool(condition)

        if key in ["hate_speech", "prompt_injection"]:
            results[key + "_confidence_score"] = round(float(score), 4) 
        elif key == "offensive_language":
            results["offensive_language_score"] = round(float(score), 4) 


    if concurrent:
        with ThreadPoolExecutor() as executor:
            futures = {
                'hate_speech': executor.submit(detect_hate_speech, prompt, hate_speech_confidence_threshold) if check_hate_speech else None,
                'prompt_injection': executor.submit(detect_model_injection, prompt, injection_confidence_threshold) if check_prompt_injection else None,
                'offensive_language': executor.submit(detect_offensive_language, prompt, offensive_threshold) if check_offensive else None
            }  

    for key, future in futures.items():
        if future:  
            score, condition = future.result()
            add_result(key, condition, score)
        else:  
            add_result(key, False, 0.0)  


            for future, (key, enabled) in zip(futures, [('hate_speech', check_hate_speech), ('prompt_injection', check_prompt_injection), ('offensive_language', check_offensive)]):
                if enabled:
                    score, condition = future.result()
                    add_result(key, condition, score)
    else:
        if check_hate_speech:
            condition, score = detect_hate_speech(prompt, hate_speech_confidence_threshold)
            add_result('hate_speech', condition, score)
        if check_prompt_injection:
            condition, score = detect_model_injection(prompt, injection_confidence_threshold)
            add_result('prompt_injection', condition, score)
        if check_offensive:
            score, condition = detect_offensive_language(prompt, offensive_threshold)
            add_result('offensive_language', condition, score)

    return results