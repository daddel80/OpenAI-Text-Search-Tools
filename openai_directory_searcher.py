# OpenAI Directory Text Searcher
# Author: Thomas Knoefel
# Version: 1.0.0
#
# This script searches through all text and PDF files in a specified directory 
# and uses the OpenAI API to find the best answer to a user's question. 
# It splits the input text into sections of 4000 tokens and iterates through 
# them to find the answer with the highest score.
#

import openai
import os
import PyPDF2
import sys
from tqdm import tqdm

# Set your OpenAI API key
openai.api_key = "<your openai key comes here>"

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    elif file_extension == ".pdf":
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text()
    else:
        content = ""

    return content

def read_files_from_directory(directory_path):
    all_texts = ""
    file_names = os.listdir(directory_path)
    
    # Add progress bar
    for file_name in tqdm(file_names, desc="Reading files", unit="file"):
        file_path = os.path.join(directory_path, file_name)
        all_texts += read_file(file_path) + "\n"

    return all_texts

def search_text_with_openai_api(query, text):
    # Split the read text into sections of 4000 tokens
    text_sections = [text[i:i + 4000] for i in range(0, len(text), 4000)]

    best_answer = None
    best_score = -1

    # Add progress bar for the loop
    for section in tqdm(text_sections, desc="Searching text sections", leave=False):
        result = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{query}\n{section}\nAnswer:",
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5,
            logprobs=5,
        )

        if result.choices:
            answer = result.choices[0].text.strip()
            logprobs_list = result.choices[0].logprobs.token_logprobs
            score = sum(logprobs_list[:5])
            
            # For debugging
            # print(f"Answer: {answer}")
            # print(f"Score: {score}")
            
            # Choose the answer with the highest score
            if score > best_score:
                best_answer = answer
                best_score = score
                

    return best_answer if best_answer else "No answer found."


def main():
    # Path to the directory containing all text and PDF files
    directory_path = "all_files"

    # Read the text from the files in the directory
    all_texts = read_files_from_directory(directory_path)

    while True:
        # Ask a question interactively
        query = input("Please enter a question (or 'exit' to quit): ")
        
        if query == "exit":
            break
        
        answer = search_text_with_openai_api(query, all_texts)

        print(f"Question: {query}")
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
