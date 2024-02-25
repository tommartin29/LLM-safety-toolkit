# LLM Safety Toolkit (WIP)

The LLM Safety Toolkit is a tool designed to analyse prompts for potential safety concerns such as hate speech, offensive language, and model injections. It utilises various detection models to assess the safety of a given prompt.

It can be used on both inputs and outputs, and is designed to be modular and flexible.

This is a small project to bring these models together in a simple way.

## Usage

You can use the `prompt_safety_check` function in `LLM_safety_toolkit.py` to analyse prompts for safety concerns. Here's how you can use it:

```python
from LLM_safety_toolkit import prompt_safety_check

# Example values
prompt = "This is a potentially harmful text."
injection_confidence_threshold = 0.9  # Increase for stricter injection confidence reqts
offensive_threshold = 0.4  # Lower for more sensitive offensive language detection
hate_speech_confidence_threshold = 0.75 # Increase for stricter hate speech confidence reqts
concurrent = False  # Set to False for sequential analysis

results = prompt_safety_check(
    prompt, 
    check_hate_speech=True, 
    check_prompt_injection=True, 
    check_offensive=True,
    injection_confidence_threshold=injection_confidence_threshold,
    offensive_threshold=offensive_threshold, 
    hate_speech_confidence_threshold=hate_speech_confidence_threshold,
    concurrent=concurrent
)

print("Safety analysis results:")
print(results)

```

## Example Results

Here is an example of the results returned by the Prompt Safety Checker:

```json
Safety analysis results:

{
    "prompt": "hello",
    "hate_speech": false,
    "hate_speech_confidence_score": 0.9997,
    "prompt_injection": false,
    "prompt_injection_confidence_score": 0.9999,
    "offensive_language": false,
    "offensive_language_score": 0.1671
}
```

## Models

* **Hate Speech:** [facebook/roberta-hate-speech-dynabench-r4-target]((https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target))
* **Prompt Injection:** [ProtectAI/deberta-v3-base-prompt-injection](https://huggingface.co/protectai/deberta-v3-base-prompt-injection)
* **Offensive Language:** [cardiffnlp/twitter-roberta-base-offensive](https://github.com/cardiffnlp/tweeteval)


**Important Note:** The first time you run the toolkit with a specific detection type (hate speech, prompt injection, offensive language), the corresponding model will be automatically downloaded from the Hugging Face Model Hub.  Subsequent runs will use the locally cached model.

## Warning

**This LLM Safety Toolkit is strictly NOT recommended for production use under any circumstances.**  This is a personal research project and likely contains numerous errors. The toolkit is in an experimental stage and does not meet production-level standards. The selected models are primarily for investigating different LLM usage methods and may not be the most effective or accurate for their intended tasks.


* **Imperfect Detection:** The models used for hate speech, prompt injection, and offensive language detection are not foolproof. They may produce false positives (incorrectly identifying safe text) or false negatives (missing harmful content).
* **Potential Bias:** The underlying models may reflect biases present in the datasets they were trained on. Be aware that the results may not always be fair or unbiased.
* **Evolving Landscape:**  This toolkit might not always keep up with the latest threats or best practices.

**This toolkit is intended for research and experimentation purposes only.  Do not rely on it for critical safety decisions in a production environment.**


## Configurations

You can configure the behavior of the `prompt_safety_check` function using the following parameters:

- `check_hate_speech`: Set to `True` to enable hate speech detection.
- `check_prompt_injection`: Set to `True` to enable prompt injection detection.
- `check_offensive`: Set to `True` to enable offensive language detection.
- `injection_confidence_threshold`: Confidence threshold for prompt injection detection (default: 0.8).
- `offensive_threshold`: Threshold for offensive language detection (default: 0.6). **Note: This is not a confidence score, but a score of how offensive the model believes the text to be.**
- `hate_speech_confidence_threshold`: Confidence threshold for hate speech detection (default: 0.8).
- `concurrent`: Set to `True` to enable concurrent processing (default: `True`). Set to `False` to disable concurrent processing.


## Files

### LLM_safety_toolkit.py

The `LLM_safety_toolkit.py` file contains the `prompt_safety_check` function, which analyses prompts for hate speech, model injections, and offensive language. It utilises concurrent processing for efficiency.

### detect_hate_speech.py

This file contains the `detect_hate_speech` function, which uses the [RoBERTa model for hate speech detection](https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target) trained on dynamically generated datasets.

### prompt_injection.py

The `prompt_injection.py` file includes functions to detect model injections in prompts using the [DeBERTa-v3 model for prompt injection detection](https://huggingface.co/protectai/deberta-v3-base-prompt-injection). You can edit keywords in the `keywords.txt` file and regex patterns in the `regex_patterns.txt` file to customise the detection process.

### detect_offensive_language.py

In this file, you'll find the `detect_offensive_language` function, which detects offensive language in text inputs using the [RoBERTa model for offensive language detection](https://huggingface.co/cardiffnlp/twitter-roberta-base-offensive) trained on the TweetEval dataset.


## TODO

* **Explore Additional Detection Models:**  Experiment with integrating other models to improve accuracy or address different nuances.
* **Customisable Output Formats:**  Allowing users to select the output format (e.g., JSON, CSV) for easier integration into other systems.
* **Expand Safety Checks:**  Incorporate additional safety checks, such as detecting bias, misinformation, or other harmful content types.
* **Performance:**  Using more lightweight and specifically trained models for performance improvements.
* **Learning:**  Allow the user to save past malicious prompts, and reference against them before input if needed.
* **Mass text analysis:** Implement tools for working with larger text sets than a single prompt at a time.

## Requirements

```
transformers>=4.38.1
torch>=2.2.1
scipy>=1.12.0
urllib3>=2.2.1
```
## References

* **Prompt Injection Model:**
    * ProtectAI.com. (2023). Fine-Tuned DeBERTa-v3 for Prompt Injection Detection [Model on Hugging Face]. https://huggingface.co/ProtectAI/deberta-v3-base-prompt-injection

* **Hate Speech Model:**
    * Vidgen, B., Thrush, T., Waseem, Z., & Kiela, D. (2021). Learning from the Worst: Dynamically Generated Datasets to Improve Online Hate Detection. *Proceedings of the Association for Computational Linguistics (ACL)*. [https://aclanthology.org/2021.acl-long.483/](https://aclanthology.org/2021.acl-long.483/) 

* **Offensive Language Model:**
    * Zampieri, M., Malmasi, S., Nakov, P., Rosenthal, S., Farra, N., & Kumar, R. (2019). SemEval-2019 Task 6: Identifying and Categorizing Offensive Language in Social Media (OffensEval). *Proceedings of the 13th International Workshop on Semantic Evaluation*. [https://aclanthology.org/S19-2007/](https://aclanthology.org/S19-2007/)

* **TweetEval Toolkit:**
    * CardiffNLP. (n.d.). TweetEval [GitHub repository](https://github.com/cardiffnlp/tweeteval)
