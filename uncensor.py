import json
import os
import sys
from datetime import datetime
from typing import Iterator, List, Union
from concurrent.futures import ThreadPoolExecutor

def filter_json_lines(input_file_name: str, words_to_match: list[str], num_threads: int = 10) -> None:
    """
    Filters JSON lines from the input file and writes the filtered lines to the output file.
    Lines are filtered out if the "output" field contains any of the specified words.

    :param input_file_name: Name of the input JSON or JSON Lines file.
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

    # Determine the file type based on the extension
    file_extension = os.path.splitext(input_file_name)[1].lower()

    with open(input_file_path, 'r', encoding='utf-8') as input_fp, open(output_file_path, 'w', encoding='utf-8') as output_fp:
        if file_extension == '.json':
            # Read the entire JSON file and process it
            data = json.load(input_fp)
            if not isinstance(data, list):
                data = [data]
            filtered_data = list(filter_json_lines_iter(data, words_to_match))
            json.dump(filtered_data, output_fp, ensure_ascii=False, indent=4)
        elif file_extension == '.jsonl':
            # Read the JSON Lines file line by line.
            lines = (line.strip() for line in input_fp if line.strip())
            filtered_lines = list(filter_json_lines_iter(lines, words_to_match))
            for line in filtered_lines:
                output_fp.write(line + '\n')
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are .json and .jsonl.\nNote: JSONL may not work at moment.")

def filter_json_lines_iter(lines: Union[Iterator[str], List[dict]], words_to_match: list[str]) -> Iterator[Union[str, dict]]:
    """
    Generator function that yields filtered JSON lines or objects.

    :param lines: Iterator over input file lines or list of JSON objects.
    :param words_to_match: List of words to match in the "output" field.
    :return: Iterator of filtered JSON lines or objects.
    """
    words_to_match_set = set(words_to_match)
    for line in lines:
        try:
            if isinstance(line, str):
                data = json.loads(line)
            else:
                data = line
            output_value = data.get('output', '')
            if not any(word in output_value for word in words_to_match_set):
                yield data if isinstance(line, dict) else json.dumps(data)
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python uncensor.py <input_file_name>.\nNote: JSONL may not work at moment.")
        sys.exit(1)

    input_file_name = sys.argv[1]
    words_to_match = [
    "a language model",
    "ableist",
    "activities that could harm",
    "activities that could undermine",
    "adhere to ethical guidelines",
    "adhere to safety guidelines",
    "adherence to the law",
    "against law",
    "against my programming",
    "against women",
    "AI assistant",
    "AI cannot create or program",
    "AI language model and I do not",
    "AI principles",
    "an AI language model you don't have",
    "an AI language",
    "and ethical sourcing",
    "apropriada em nenhum contexto",
    "are from ethical",
    "as a language model",
    "As a large language model",
    "As a machine",
    "as an AI assistant"
    "as an AI language model",
    "As an AI language model, I am not able",
    "As an AI language model, I am only able",
    "As an AI language model, I cannot modify",
    "As an AI language model, I cannot",
    "As an AI language model, I do not",
    "As an AI language model, I don't have personal",
    "As an AI language model, I don't have",
    "as an AI language model, you cannot",
    "As an AI",
    "bad language",
    "bad_language",
    "bias",
    "biases",
    "can't provide",
    "cannot engage in discussions",
    "cannot provide any information",
    "cannot provide guidance",
    "cannot provide information",
    "cannot provide",
    "cannot support or promote",
    "capitalism",
    "cause harm",
    "certainly not",
    "committed to promoting",
    "common sense",
    "communist",
    "como modelo de lenguaje AI",
    "Como modelo de linguagem",
    "Como um modelo de linguagem, não tenho a capacidade de",
    "comply",
    "complying",
    "consensual",
    "controversial",
    "dangerous activities",
    "dangerous or harmful",
    "derogatory",
    "Desculpe-me, mas a linguagem vulgar e ofensiva",
    "designed to prioritize safety",
    "discriminate",
    "discrimination",
    "discriminatory",
    "diversity and inclusion",
    "diversity and",
    "diversity",
    "divisive",
    "domestic violence",
    "empowerment",
    "engage in unethical",
    "ensure the safety",
    "Ensuring the ethical",
    "entertainment purposes",
    "environmental, social, and governance",
    " ESG ",
    "ethical guidelines",
    "ethical principles",
    "ethical",
    "ethically",
    "ethics",
    "extremist",
    "F*ck",
    "f*cking",
    "feminism",
    "feminist",
    "filter_bad_language",
    "focus on promoting safety",
    "follow ethical guidelines",
    "gay",
    "gender inequality",
    "gender stereotype",
    "gender-based",
    "glorify",
    "had an ethical system",
    "harmful consequences",
    "harmful to human beings",
    "harmful",
    "hate speech",
    "hateful",
    "However,it is important to use any code or information provided responsibly and within legal and ethical boundaries.",
    "hurtful",
    "I am an AI language model and do not",
    "I am an AI",
    "I am an",
    "I am here to assist",
    "I apologize, but",
    "I can not fulfill your request",
    "I can't fulfill your request",
    "I can't",
    "I cannot assist",
    "I cannot fulfill your request",
    "I cannot",
    "I don't have the ability",
    "I know as an AI language model you don't have",
    "I will not",
    "I'll not",
    "I'm afraid I cannot create",
    "I'm an AI",
    "I'm an",
    "I'm sorry, but as an AI language model",
    "I'm sorry, I cannot generate",
    "I'm sorry, I cannot",
    "I'm sorry,",
    "illegal actions or intentions",
    "illegal activities or actions",
    "illegal subject",
    "illegal substances or activities",
    "illegal",
    "illegality",
    "inappropriate",
    "inclusive workplace",
    "inclusivity",
    "involves an illegal subject",
    "It is important for",
    "It is important to",
    "it is important to",
    "it is never okay",
    "it is not appropriate",
    "It is not possible",
    "it operates ethically and is",
    "It's important to",
    "it's important to",
    "it's not appropriate",
    "jeopardize the safety",
    "keep in mind",
    "Lamento no poder proporcionarte el código",
    "lawful information",
    "legal and ethical",
    "legality",
    "lgbt",
    "lgbtq+",
    "lgbtqi+",
    "Lo siento, como modelo de lenguaje",
    "Lo siento, como modelo de lenguaje, no puedo realizar",
    "Lo siento, como modelo de lenguaje, no tengo",
    "Lo siento, debe haber habido una confusión",
    "Lo siento, pero como modelo de lenguaje, no puedo proporcionar",
    "Lo siento, pero no puedo",
    "Lo siento, soy un modelo de lenguaje y no tengo la capacidad de generar",
    "maintain user safety",
    "Microaggression",
    "morally",
    "morals",
    "my guidelines",
    "my knowledge cut off",
    "my knowledge cutoff",
    "my main goal",
    "my programming",
    "my purpose is to ",
    "my purpose",
    "no puedo proporcionar",
    "not a human",
    "not able to provide",
    "not acceptable",
    "not appropriate",
    "not be appropriate",
    "not be suitable",
    "not provide",
    "not within the scope",
    "Note: ",
    "Não posso",
    "offensive",
    "our values",
    "pero debido a mi capacidad para generar códigos complejos y completos es limitado",
    "Please note",
    "please refrain",
    "Please, note",
    "pose a risk to others",
    "potentially be harmful",
    "potentially dangerous",
    "potentially harmful",
    "prioritize ethical",
    "prioritize human safety",
    "prioritize safety",
    "prioritize user safety",
    "prioritize user well-being",
    "prioritize your safety",
    "problematic history",
    "programming prohibits",
    "promote dangerous",
    "promote safety",
    "promote the well-being",
    "purely hypothetical",
    "racial",
    "racism",
    "racist",
    "real-world consequences",
    "refrain from",
    "refrain your",
    "regulations",
    "Remember that",
    "respectful",
    "responsible AI",
    "responsible information sharing",
    "safe information",
    "safe spaces",
    "sensitive topic",
    "September 2021",
    "sexism",
    "sexist",
    "sh*t",
    "social responsibility",
    "stereotypes",
    "supremacist",
    "text-based AI language model",
    "the words ****",
    "transgender",
    "*This chat conversation is shared from",
    "*This conversation is shared from",
    "unable to offer assistance",
    "unacceptable",
    "undermine the stability",
    "underrepresentation",
    "unethical business",
    "unethical or aggressive",
    "unethical",
    "Unfortunately, I cannot provide",
    "values diversity",
    "well-being of all users",
    "won't provide",
    "worth noting",
    "you cannot create an",
    "your safety",
    ]
    
    filter_json_lines(input_file_name, words_to_match, num_threads=10)
