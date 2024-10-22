import json
import os
import sys
from datetime import datetime
from typing import Iterator
from concurrent.futures import ThreadPoolExecutor

def filter_json_lines(input_file_name: str, words_to_match: list[str], num_threads: int = 10) -> None:
    """
    Filters JSON lines from the input file and writes the filtered lines to the output file.
    Lines are filtered out if the "output" field contains any of the specified words.

    :param input_file_name: Name of the input JSON file.
    :param words_to_match: List of words to match in the "output" field.
    :param num_threads: Number of threads to use for parallel processing (defaults to 10).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, input_file_name)

    # Generate output file name based on current date and time and input file name
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = os.path.splitext(input_file_name)[0]
    output_file_name = f"{base_name}-{current_time}-UNCENSORED.json"
    output_file_path = os.path.join(script_dir, output_file_name)

    with open(input_file_path, 'r', encoding='utf-8') as input_fp, open(output_file_path, 'w', encoding='utf-8') as output_fp:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(filter_json_lines_iter, input_fp, words_to_match) for _ in range(num_threads)]
            for future in futures:
                for line in future.result():
                    output_fp.write(line)

def filter_json_lines_iter(input_fp: Iterator[str], words_to_match: list[str]) -> Iterator[str]:
    """
    Generator function that yields filtered JSON lines.

    :param input_fp: Iterator over input file lines.
    :param words_to_match: List of words to match in the "output" field.
    :return: Iterator of filtered JSON lines.
    """
    words_to_match_set = set(words_to_match)
    for line in input_fp:
        try:
            data = json.loads(line)
            output_value = data.get('output', '')
            if not any(word in output_value for word in words_to_match_set):
                yield line
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python uncensor.py <input_file_name>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    words_to_match = [
    "text-based AI language model",
    "domestic violence",
    "please refrain",
    "refrain your",
    "refrain from",
    "derogatory",
    "inappropriate",
    "offensive",
    "racism",
    "racist",
    "racial",
    "discriminate",
    "discriminatory",
    "discrimination",
    "sexist",
    "sexism",
    "unacceptable",
    "inclusive workplace",
    "lgbt",
    "lgbtq+",
    "lgbtqi+",
    "gay",
    "I can't",
    "I will not",
    "I'll not",
    "morals",
    "ethics",
    "ethical",
    "legality",
    "illegal",
    "illegality",
    "hateful",
    "harmful",
    "it is never okay",
    "It is important to",
    "It's important to",
    "real-world consequences",
    "hate speech",
    "glorify",
    "not be appropriate",
    "supremacist",
    "extremist",
    "responsible AI",
    "AI principles",
    "AI assistant",
    "an AI language",
    "ableist",
    "hurtful",
    "gender stereotype",
    "gender inequality",
    "underrepresentation",
    "safe spaces",
    "gender-based",
    "inclusivity",
    "feminist",
    "feminism",
    "transgender",
    "empowerment",
    "communist",
    "capitalism",
    "stereotypes",
    "biases",
    "bias",
    "Microaggression",
    "prioritize human safety",
    "as a language model",
    "as an AI language model",
    "as an AI assistant"
    "As a large language model",
    "As an AI",
    "ethical principles",
    "consensual",
    "common sense",
    "Note: ",
    "Remember that",
    "Please, note",
    "it is not appropriate",
    "it is important to",
    "it's important to",
    "it's not appropriate",
    "I cannot fulfill your request",
    "I can't fulfill your request",
    "I can not fulfill your request",
    "harmful to human beings",
    "ethical guidelines",
    "my guidelines",
    "prioritize user safety",
    "prioritize your safety",
    "your safety",
    "adhere to ethical guidelines",
    "harmful consequences",
    "potentially harmful",
    "dangerous activities",
    "promote dangerous",
    "promote safety",
    "well-being of all users",
    "responsible information sharing",
    "jeopardize the safety",
    "illegal actions or intentions",
    "undermine the stability",
    "promote the well-being",
    "illegal activities or actions",
    "adherence to the law",
    "against law",
    "potentially be harmful",
    "illegal substances or activities",
    "committed to promoting",
    "safe information",
    "lawful information",
    "cannot provide guidance",
    "cannot provide information",
    "unable to offer assistance",
    "cannot engage in discussions",
    "programming prohibits",
    "follow ethical guidelines",
    "ensure the safety",
    "involves an illegal subject",
    "prioritize safety",
    "illegal subject",
    "prioritize user well-being",
    "cannot support or promote",
    "activities that could harm",
    "pose a risk to others",
    "against my programming",
    "activities that could undermine",
    "potentially dangerous",
    "not within the scope",
    "designed to prioritize safety",
    "not able to provide",
    "maintain user safety",
    "adhere to safety guidelines",
    "dangerous or harmful",
    "cannot provide any information",
    "focus on promoting safety",
    "an AI language model you don't have",
    "As an AI language model, I cannot",
    "As an AI language model, I do not",
    "As an AI language model, I am not able",
    "As an AI language model, I don't have personal",
    "I am an AI language model and do not",
    "However,it is important to use any code or information provided responsibly and within legal and ethical boundaries.",
    "As an AI language model, I don't have",
    "As an AI language model, I am only able",
    "AI language model and I do not",
    "As an AI language model, I cannot modify",
    "I know as an AI language model you don't have",
    "as an AI language model, you cannot",
    "I'm sorry, but as an AI language model",
    "Unfortunately, I cannot provide",
    "I'm sorry, I cannot",
    "I'm sorry, I cannot generate",
    "AI cannot create or program",
    "I'm afraid I cannot create",
    "you cannot create an",
    "it operates ethically and is",
    "had an ethical system",
    "Ensuring the ethical",
    "and ethical sourcing",
    "are from ethical",
    "legal and ethical",
    "engage in unethical",
    "unethical or aggressive",
    "unethical business",
    "como modelo de lenguaje AI",
    "Lo siento, como modelo de lenguaje",
    "no puedo proporcionar",
    "pero debido a mi capacidad para generar códigos complejos y completos es limitado",
    "Lo siento, pero no puedo",
    "Lo siento, pero como modelo de lenguaje, no puedo proporcionar",
    "Lo siento, como modelo de lenguaje, no tengo",
    "Lo siento, debe haber habido una confusión",
    "Lo siento, como modelo de lenguaje, no puedo realizar",
    "Lo siento, soy un modelo de lenguaje y no tengo la capacidad de generar",
    "Lamento no poder proporcionarte el código",
    "Desculpe-me, mas a linguagem vulgar e ofensiva",
    "apropriada em nenhum contexto",
    "Não posso",
    "Como modelo de linguagem",
    "Como um modelo de linguagem, não tenho a capacidade de",
    "I cannot assist",
    "prioritize ethical",
    "respectful",
    "morally",
    "I'm sorry,",
    "I'm an",
    "I am an",
    "I'm an AI",
    "I am an AI",
    "my purpose",
    "filter_bad_language",
    "entertainment purposes",
    "purely hypothetical",
    "not a human",
    "cannot provide",
    "can't provide",
    "won't provide",
    "not provide",
    "worth noting",
    "cause harm",
    "a language model",
    "keep in mind",
    "unethical",
    "bad language",
    "the words ****",
    "bad_language",
    "certainly not",
    "complying",
    "comply",
    "I cannot",
    "my main goal",
    "As a machine",
    "I don't have the ability",
    "I am here to assist",
    "my purpose is to ",
    "my knowledge cutoff",
    "my knowledge cut off",
    "September 2021",
    "regulations",
    "not be suitable",
    "I apologize, but",
    "It is not possible",
    "controversial",
    "my programming",
    "ethically",
    "it is important to",
    "Please note",
    "sensitive topic",
    "not acceptable",
    "It is important for",
    "divisive",
    "not appropriate",
    "our values",
    "f*cking",
    "F*ck",
    "sh*t",
    "diversity and",
    "diversity and inclusion",
    "values diversity",
    "social responsibility",
    "environmental, social, and governance",
    " ESG ",
    "against women",
    "problematic history",
    "diversity",
    "*This chat conversation is shared from",
    "*This conversation is shared from",
    ]
    
    filter_json_lines(input_file_name, words_to_match, num_threads=10)
