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



def source_translation_prompt(source_text: str, commentaries: list, target_language: str = "English") -> str:
    """
    Builds a structured prompt for translating Tibetan text using multiple commentaries.

    Args:
        source_text (str): The Tibetan text to be translated.
        commentaries (list): A list of commentaries that explain the source text.
        target_language (str): The language to translate into (default: "English").

    Returns:
        str: A structured prompt ready for use with Gemini API.
    """

    if not commentaries:
        raise ValueError("At least one commentary is required for translation.")

    # Base structure
    prompt = f"""Translate the following Tibetan text into {target_language}.
Use the provided commentaries as reference for accurate meaning and interpretation.
Each commentary explains the same source text but is written in different languages.
Do not merge them; instead, consider all perspectives before providing the translation.

### Tibetan Source Text:
{source_text}

### Commentaries:
"""

    # Add each commentary separately with proper formatting
    for idx, text in enumerate(commentaries, 1):
        prompt += f"\n[Commentary {idx}]:\n{text}\n"

    # Expected output format
    prompt += f"""
### Expected Output:
Provide a {target_language} translation of the source text by incorporating relevant insights from all the commentaries.
Ensure the meaning is accurately conveyed, considering different interpretations where necessary.
I need the translation of source text only.
"""

    return prompt


def commentary_translation_prompt(commentaries: list, target_language: str = "English") -> str:
    """
    Builds a structured prompt for translating multiple commentaries into a target language.

    Args:
        commentaries (list): A list of commentaries written in different languages.
        target_language (str): The language to translate into (default: "English").

    Returns:
        str: A structured prompt ready for use with Gemini API.
    """

    if not commentaries:
        raise ValueError("At least one commentary is required for translation.")

    # Base structure
    prompt = f"""Translate the following Buddhist commentaries into {target_language}.
Each commentary is written in a different language and provides insights into the same Tibetan text.
Preserve the original meaning while ensuring readability in {target_language}.

### Commentaries:
"""

    # Add each commentary separately with proper formatting
    for idx, text in enumerate(commentaries, 1):
        prompt += f"\n[Commentary {idx}]:\n{text}\n"

    # Expected output format
    prompt += f"""
### Expected Output:
Translate each commentary into {target_language} while maintaining its original meaning.
Ensure clarity and readability in {target_language} without altering the intended message.
Provide translations for each commentary separately.
"""

    return prompt


def source_and_commentary_translation_prompt(source_text: str, commentaries: list, target_language: str = "English") -> str:
    """
    Builds a structured prompt for translating commentaries into a target language while considering the Tibetan source text.

    Args:
        source_text (str): The Tibetan text for context.
        commentaries (list): A list of commentaries written in different languages.
        target_language (str): The language to translate into (default: "English").

    Returns:
        str: A structured prompt ready for use with Gemini API.
    """

    if not commentaries:
        raise ValueError("At least one commentary is required for translation.")

    # Base structure
    prompt = f"""Translate the following Buddhist commentaries into {target_language}.
Each commentary explains the same Tibetan text but is written in different languages.
Preserve the original meaning while ensuring readability in {target_language}.
Do NOT translate the Tibetan text—translate ONLY the commentaries.

### Tibetan Source Text:
{source_text}

### Commentaries:
"""

    # Add each commentary separately with proper formatting
    for idx, text in enumerate(commentaries, 1):
        prompt += f"\n[Commentary {idx}]:\n{text}\n"

    # Expected output format
    prompt += f"""
### Expected Output:
Translate each commentary into {target_language} while maintaining its original meaning.
Ensure clarity and readability in {target_language} without altering the intended message.
Provide translations for each commentary separately.
"""

    return prompt


def multi_source_translation_prompt(
    tibetan_text: str,
    commentaries: list,
    target_language: str = "English",
    sanskrit_text: str = None,
    sanskrit_english_text: str = None
) -> str:
    """
    Builds a structured prompt for translating commentaries into a target language while considering 
    Tibetan source text, and optionally Sanskrit source text with its English equivalent.

    Args:
        tibetan_text (str): The Tibetan text for context.
        commentaries (list): A list of commentaries written in different languages.
        target_language (str): The language to translate into (default: "English").
        sanskrit_text (str, optional): The original Sanskrit text (if available).
        sanskrit_english_text (str, optional): The English translation of the Sanskrit text (if available).

    Returns:
        str: A structured prompt ready for use with Gemini API.
    """

    if not commentaries:
        raise ValueError("At least one commentary is required for translation.")

    # Base structure
    prompt = f"""Translate the following Buddhist commentaries into {target_language}.
Each commentary explains the same Buddhist text but is written in different languages.
Preserve the original meaning while ensuring readability in {target_language}.
Do NOT translate the Tibetan text—translate ONLY the commentaries.

"""

    # If Sanskrit source is available, add it to the prompt
    if sanskrit_text and sanskrit_english_text:
        prompt += f"""
### Sanskrit Source Text:
{sanskrit_text}

### Sanskrit-to-English Translation:
{sanskrit_english_text}
"""

    # Add Tibetan source text
    prompt += f"""

### Tibetan Source Text:
{tibetan_text}

### Commentaries:
"""

    # Add each commentary separately with proper formatting
    for idx, text in enumerate(commentaries, 1):
        prompt += f"\n[Commentary {idx}]:\n{text}\n"

    # Expected output format
    prompt += f"""
### Expected Output:
Translate each commentary into {target_language} while maintaining its original meaning.
Ensure clarity and readability in {target_language} without altering the intended message.
Provide translations for each commentary separately.
"""

    return prompt
