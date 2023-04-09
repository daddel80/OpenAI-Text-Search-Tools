# OpenAI File Text Searcher
# Author: Thomas Knoefel
# Version: 1.0.0
# 
# This script searches a given text file using the OpenAI API to find the best 
# answer to a user's question. The script prompts the user for a question, 
# reads the specified text file, and searches for the answer in the file using 
# the OpenAI API. 
# 

import openai
import os

# Set your OpenAI API key
openai.api_key = "<your openai key comes here>"

def read_text_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content

def search_text_with_openai_api(query, text):
    result = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{query}\n{text}\nAnswer:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    if result.choices:
        answer = result.choices[0].text.strip()
        return answer
    else:
        return "No answer found."

def main():
    # File path to the example text
    file_path = "example_text.txt"

    # Read the text from the file
    example_text = read_text_file(file_path)

    while True:
        # Ask the user for a query
        query = input("Question (or 'q' to quit): ")

        if query.lower() == 'q':
            break

        # Search for the query in the example text
        answer = search_text_with_openai_api(query, example_text)

        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()
