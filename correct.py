# correct.py

import openai

def read_api_key(file_path="credentials.txt"):
    try:
        with open(file_path, 'r') as file:
            return file.readline().strip()  # Read the API key directly
    except FileNotFoundError:
        print("Credentials file not found.")
        return None

def split_text(text, max_length=1024):
    """
    Splits text into chunks, each with a maximum length of max_length.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) > max_length:
            current_chunk.pop()  # Remove last word that exceeded the limit
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]  # Start a new chunk with the last word

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def correct_text(input_text, api_key):
    print("AI Correction is enabled. Processing text...")

    # Split the text into smaller parts
    parts = split_text(input_text)

    corrected_parts = []
    for part in parts:
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f"Correct the following text for grammar, oddities, or redundancies while maintaining the full sentiment. Do not include quotes around the text:\n\n{part}",
                max_tokens=1024,
                temperature=0.5,
                api_key=api_key
            )
            corrected_part = response.choices[0].text.strip()
            corrected_parts.append(corrected_part)
        except Exception as e:
            print(f"An error occurred: {e}")
            corrected_parts.append(part)  # Use the original part if there's an error

    # Concatenate the corrected parts
    return ' '.join(corrected_parts)
