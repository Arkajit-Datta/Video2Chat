import re
import string

def response_cleaner(response):
    response = ''.join(char for char in response if char in string.printable)
    if response.startswith("```") and response.endswith("```"):
        response = "```".join(response.split("```")[1:-1])
        response = re.sub(r"\bjson\b", "", response) # removing anything with a json in the beginning
    elif response.startswith("```json") and response.endswith("```"):
        response = "```json".join(response.split("```")[1:-1])
        response = re.sub(r"\bjson\b", "", response) # removing anything with a json in the beginning
    return response