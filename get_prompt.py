import pandas as pd 

### **🔹 Individual Prompt Functions*
def generate_commentary_translation_prompt(row, target_language):
    """ Generates a prompt for translating multiple commentaries into English. """
    prompt = f"Translate the following Buddhist commentaries into {target_language}.\n"
    if pd.notna(row.get("Tibetan Source")):
        prompt += f"\n### Tibetan Source Text:\n{row['Tibetan Source']}"
    prompt += "\n\n### Commentaries:"
    for i in range(1, 5):  # 4 Commentaries
        col_name = f"Commentary {i}"
        if col_name in row and pd.notna(row[col_name]):
            prompt += f"\n[Commentary {i}]:\n{row[col_name]}"
    prompt += f"\n\n### Expected Output:\nTranslate each commentary into {target_language} while maintaining its original meaning."
    return prompt


def generate_combined_commentary_prompt(row, target_language):
    """ Generates a prompt for combining multiple commentaries into a single English translation. """
    prompt = f"Combine and translate the following Buddhist commentaries into {target_language}.\n"
    prompt += "\n\n### Commentaries:"
    for i in range(1, 6):  # Up to 5 Commentaries
        col_name = f"Commentary {i}"
        if col_name in row and pd.notna(row[col_name]):
            prompt += f"\n{row[col_name]}"
    prompt += f"\n\n### Expected Output:\nProvide a single, well-structured translation in {target_language} that preserves meaning."
    return prompt


def generate_plain_translation_prompt(row, target_language):
    """ Generates a simple translation prompt. """
    prompt = f"Translate the following Tibetan text into {target_language}:\n"
    if pd.notna(row.get("Tibetan Source")):
        prompt += f"\n{row['Tibetan Source']}"
    prompt += f"\n\n### Expected Output:\nA clear and concise translation in {target_language}."
    return prompt


def generate_sanskrit_translation_prompt(row, target_language):
    """ Generates a translation prompt for Sanskrit text into English. """
    prompt = f"Translate the following Sanskrit text into {target_language}:\n"
    if pd.notna(row.get("Sanskrit Source")):
        prompt += f"\n{row['Sanskrit Source']}"
    prompt += f"\n\n### Expected Output:\nAn accurate translation in {target_language}."
    return prompt


def generate_standardized_translation_prompt(row, target_language):
    """ Generates a standardized translation prompt for structured text. """
    prompt = f"Provide a standardized translation of the following Tibetan text into {target_language}:\n"
    if pd.notna(row.get("Tibetan Source")):
        prompt += f"\n{row['Tibetan Source']}"
    prompt += f"\n\n### Expected Output:\nA precise and well-structured translation in {target_language}."
    return prompt


def generate_word_by_word_translation_prompt(row, target_language):
    """ Generates a word-by-word translation prompt. """
    prompt = f"Provide a word-by-word translation of the following Tibetan text into {target_language}:\n"
    if pd.notna(row.get("Tibetan Source")):
        prompt += f"\n{row['Tibetan Source']}"
    prompt += f"\n\n### Expected Output:\nA detailed word-by-word breakdown in {target_language}."
    return prompt
